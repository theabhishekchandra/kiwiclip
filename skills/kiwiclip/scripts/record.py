#!/usr/bin/env python3
"""Record a planned browser walkthrough for /kiwiclip.

Usage:
    python3 record.py <plan.json> <output-dir>

Reads a plan written by Step 2 (see references/step-2-plan.md), optionally
logs in (see references/auth.md), then executes each step through an
observe -> act -> verify loop, recording the whole thing with Playwright.

This script is deliberately mechanical: it does not call any LLM. The
orchestrating agent does the reasoning (writing the plan, picking element
hints); this script just executes it reliably and records the result.

Plan schema (JSON):
{
  "login": {                                   # optional
    "login_url": "https://app.example.com/login",
    "email_env": "KIWICLIP_EMAIL",              # default KIWICLIP_EMAIL
    "password_env": "KIWICLIP_PASSWORD",        # default KIWICLIP_PASSWORD
    "totp_secret_env": "KIWICLIP_TOTP_SECRET",  # optional
    "post_login_url_contains": "dashboard"      # optional, waited for after submit
  },
  "steps": [
    {"action": "goto", "url": "https://app.example.com/dashboard"},
    {"action": "click", "hint": "Create project", "role": "button"},
    {"action": "fill", "hint": "Project name", "value": "Demo"},
    {"action": "scroll", "y": 500},
    {"action": "wait", "ms": 1000}
  ]
}
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_url import SecurityError, validate_url_for_recording  # noqa: E402

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, sync_playwright

MASK_INIT_SCRIPT = """
(() => {
  const style = document.createElement('style');
  style.textContent = `
    input[type="password"],
    input[autocomplete="cc-number"],
    input[autocomplete="one-time-code"],
    input[name*="otp" i], input[name*="ssn" i], input[name*="card" i] {
      -webkit-text-security: disc !important;
      color: transparent !important;
      text-shadow: 0 0 8px rgba(0,0,0,0.5) !important;
    }
  `;
  (document.head || document.documentElement).appendChild(style);
})();
"""

COOKIE_BANNER_PATTERNS = ["Accept", "Got it", "I agree", "Allow all", "Accept all"]


class LocatorNotFoundError(Exception):
    pass


class SessionExpiredError(Exception):
    pass


def dismiss_cookie_banner(page: Page) -> None:
    for text in COOKIE_BANNER_PATTERNS:
        try:
            btn = page.get_by_role("button", name=re.compile(re.escape(text), re.I))
            if btn.count() > 0:
                btn.first.click(timeout=1500)
                page.wait_for_timeout(300)
                return
        except Exception:
            continue


def find_locator(page: Page, hint: str, role: str | None = None):
    pattern = re.compile(re.escape(hint), re.I) if hint else None
    strategies = []
    if role and pattern:
        strategies.append(lambda: page.get_by_role(role, name=pattern))
    if pattern:
        strategies += [
            lambda: page.get_by_role("button", name=pattern),
            lambda: page.get_by_role("link", name=pattern),
            lambda: page.get_by_label(pattern),
            lambda: page.get_by_placeholder(pattern),
            lambda: page.get_by_text(hint, exact=False),
        ]
    if hint:
        strategies.append(lambda: page.get_by_test_id(hint))

    for strategy in strategies:
        try:
            locator = strategy()
            if locator.count() > 0:
                return locator.first
        except Exception:
            continue
    raise LocatorNotFoundError(f"No element found for hint={hint!r} role={role!r}")


def human_move_and_click(page: Page, locator) -> None:
    box = locator.bounding_box()
    if box:
        target_x, target_y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        viewport = page.viewport_size or {"width": 1920, "height": 1080}
        start_x, start_y = viewport["width"] / 2, viewport["height"] / 2
        steps = 8
        for i in range(1, steps + 1):
            page.mouse.move(
                start_x + (target_x - start_x) * i / steps,
                start_y + (target_y - start_y) * i / steps,
            )
            page.wait_for_timeout(15)
    locator.click()


def observe_page_state(page: Page) -> dict:
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except PlaywrightTimeoutError:
        pass
    return {
        "url": page.url,
        "title": page.title(),
        "has_modal": page.is_visible("[role=dialog], .modal"),
        "has_error": page.is_visible(".error, [role=alert]"),
    }


def execute_step(page: Page, step: dict) -> None:
    action = step["action"]
    if action == "goto":
        url = validate_url_for_recording(step["url"])
        page.goto(url, wait_until="networkidle")
    elif action == "click":
        locator = find_locator(page, step.get("hint", ""), step.get("role"))
        human_move_and_click(page, locator)
    elif action == "fill":
        locator = find_locator(page, step.get("hint", ""), step.get("role"))
        locator.fill(step["value"])
    elif action == "scroll":
        page.evaluate("(y) => window.scrollBy(0, y)", step.get("y", 400))
    elif action == "wait":
        page.wait_for_timeout(step.get("ms", 1000))
    else:
        raise ValueError(f"Unknown action: {action}")


def execute_step_with_retry(page: Page, step: dict, steps_log: list, max_retries: int = 3) -> None:
    before = observe_page_state(page)
    last_error = None
    for attempt in range(max_retries):
        try:
            execute_step(page, step)
            after = observe_page_state(page)
            if after["has_error"]:
                raise RuntimeError(f"Page shows an error state after step: {step}")
            if "/login" in after["url"] and "/login" not in before["url"]:
                raise SessionExpiredError("Redirected to login mid-flow; session may have expired")
            steps_log.append({
                "step": step, "before": before, "after": after,
                "attempt": attempt + 1, "timestamp": time.time(),
            })
            return
        except (LocatorNotFoundError, PlaywrightTimeoutError, RuntimeError) as e:
            last_error = e
            dismiss_cookie_banner(page)
            if attempt < max_retries - 1:
                page.wait_for_timeout([500, 1500, 3000][attempt])
    raise RuntimeError(f"Step failed after {max_retries} attempts: {step}. Last error: {last_error}")


def login(page: Page, login_cfg: dict) -> None:
    email_env = login_cfg.get("email_env", "KIWICLIP_EMAIL")
    password_env = login_cfg.get("password_env", "KIWICLIP_PASSWORD")
    email = os.environ.get(email_env)
    password = os.environ.get(password_env)
    if not email or not password:
        raise SystemExit(
            f"Missing credentials: set ${email_env} and ${password_env} in the environment "
            "(or a local .kiwiclip/credentials.env). See references/auth.md. Never pass "
            "credentials as plan.json values or chat text."
        )

    login_url = validate_url_for_recording(login_cfg["login_url"])
    page.goto(login_url, wait_until="networkidle")
    dismiss_cookie_banner(page)

    page.locator('input[type="email"], input[name*="email" i], #email').first.fill(email)
    page.locator('input[type="password"], input[name*="password" i], #password').first.fill(password)
    page.locator('button[type="submit"], input[type="submit"], button:has-text("Log in"), button:has-text("Sign in")').first.click()

    totp_secret = os.environ.get(login_cfg.get("totp_secret_env", "KIWICLIP_TOTP_SECRET", ))
    if totp_secret:
        import pyotp

        otp_input = page.locator('input[name*="otp" i], input[placeholder*="code" i], #mfa-input')
        otp_input.first.wait_for(timeout=10000)
        code = pyotp.TOTP(totp_secret).now()
        otp_input.first.fill(code)
        page.locator('button[type="submit"]').first.click()

    post_login_contains = login_cfg.get("post_login_url_contains")
    if post_login_contains:
        page.wait_for_url(f"**{post_login_contains}**", timeout=15000)
    else:
        page.wait_for_load_state("networkidle")


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: record.py <plan.json> <output-dir>", file=sys.stderr)
        sys.exit(2)

    plan_path, output_dir = Path(sys.argv[1]), Path(sys.argv[2])
    plan = json.loads(plan_path.read_text())

    raw_dir = output_dir / "raw"
    session_dir = output_dir / ".session"
    raw_dir.mkdir(parents=True, exist_ok=True)
    session_dir.mkdir(parents=True, exist_ok=True)
    storage_state_path = session_dir / "state.json"

    steps_log: list = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context_kwargs = dict(
            record_video_dir=str(raw_dir),
            record_video_size={"width": 1920, "height": 1080},
            viewport={"width": 1920, "height": 1080},
        )
        if storage_state_path.exists():
            context_kwargs["storage_state"] = str(storage_state_path)

        context = browser.new_context(**context_kwargs)
        context.add_init_script(MASK_INIT_SCRIPT)
        page = context.new_page()

        try:
            if plan.get("login") and not storage_state_path.exists():
                login(page, plan["login"])
                context.storage_state(path=str(storage_state_path))

            for step in plan["steps"]:
                execute_step_with_retry(page, step, steps_log)

        except (SecurityError, LocatorNotFoundError, RuntimeError, SessionExpiredError) as e:
            failure_path = output_dir / "failure.png"
            try:
                page.screenshot(path=str(failure_path))
            except Exception:
                failure_path = None
            context.close()
            browser.close()
            print(json.dumps({
                "status": "failed", "error": str(e),
                "screenshot": str(failure_path) if failure_path else None,
                "steps_completed": len(steps_log),
            }))
            sys.exit(1)

        video = page.video
        context.close()
        browser.close()

        # Playwright writes the video directly into record_video_dir under an
        # auto-generated name as soon as the context closes -- video.path()
        # after close() just tells us where it landed; save_as() would need
        # the context still open, which it no longer is here.
        final_video = raw_dir / "recording.webm"
        if video is not None:
            actual_path = Path(video.path())
            if actual_path.exists() and actual_path != final_video:
                actual_path.rename(final_video)

    log_path = output_dir / "steps_log.json"
    log_path.write_text(json.dumps(steps_log, indent=2))

    print(json.dumps({
        "status": "ok",
        "video": str(final_video),
        "steps_log": str(log_path),
        "steps_completed": len(steps_log),
    }))


if __name__ == "__main__":
    main()
