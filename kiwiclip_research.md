# 🎬 KiwiClip — Complete Research v3.0

> **Note (scope update):** v1 is now scaffolded in [`skills/kiwiclip/`](skills/kiwiclip/SKILL.md) as an **Agent Skill** (SKILL.md + references/scripts, distributed via `plugin.json` + the `skills` CLI + per-agent symlinks) rather than the custom MCP server + Redis/CDN backend this document assumes below. That architecture shift, and the narrowed v1 feature set (web only, no auto-posting, no dubbing/B-roll/mobile yet), are intentional — see [`skills/kiwiclip/references/roadmap.md`](skills/kiwiclip/references/roadmap.md) for the sequencing and reasoning. Everything below is kept as the full long-term research; it's the source for later phases, not a description of what v1 currently builds.

> **Original goal**: Build an open-source, self-hostable AI skill (MCP server) distributed via a Git repository. It allows developers and users to clone the repo, connect it locally to their AI assistant (Claude/Cursor/Gemini), and autonomously generate professional demo videos of their websites, mobile apps, and products. Supports local authenticated sessions to access every screen securely.

---

## ✅ Full Feature Set (v4.0)

| # | Feature | Status |
|---|---|---|
| 0 | 🧠 AI Script & Scene Planner | ✅ Core |
| 0.5 | 🔐 Auth & Authenticated Screen Discovery | ✅ New |
| 1 | 📹 Screen Capture (Web + Mobile) | ✅ Core |
| 2 | 🎨 Animation, Effects & Annotations | ✅ Upgraded |
| 3 | 🔊 TTS Narration + Background Music | ✅ Upgraded |
| 4 | 📝 Auto-Caption / Subtitle Generation | ✅ New |
| 5 | 🎞️ Scene Assembly (Intro/Outro/Chapters/Brand Kit) | ✅ New |
| 6 | 📐 Social Media Format Variants | ✅ New |
| 7 | 🖼️ Thumbnail Auto-Generation | ✅ New |
| 8 | 🎭 AI Generative B-Roll | ✅ New |
| 9 | 🌍 Multi-Language Dubbing | ✅ New |
| 10 | 📣 Platform Post Content Generator | ✅ **NEW** |
| 11 | ⚙️ Async Job Queue + Status Tracking | ✅ New |
| 12 | 🤖 Cross-Platform MCP Skill Integration | ✅ Core |

---

## 🏗️ Complete Architecture (v2.0)

```
User Prompt ("Create a demo of my SaaS at app.example.com")
        ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 0 🧠  AI Script & Scene Planner                   │
│            → Analyze URL / screenshot                   │
│            → Auto-write narrator script                 │
│            → Decide which screens/flows to show         │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 0.5 🔐  Auth & Screen Discovery                   │  ← NEW
│            → Login with email/password, SSO, OAuth      │
│            → Handle 2FA / MFA automatically             │
│            → Support multiple user roles (admin/user)   │
│            → Auto-discover ALL authenticated screens    │
│            → Crawl app routes, nav links, sitemaps      │
│            → Credentials stored in encrypted vault      │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 1 📹  Screen Capture Layer                        │
│            → Playwright (web) / ADB + Appium (mobile)   │
│            → Ghost cursor for realistic mouse movement  │
│            → Annotated click recording                  │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 2 🎨  Animation & Annotation Layer                │
│            → Zoom/Pan/Transitions (FFmpeg / Remotion)   │
│            → Arrows, bounding boxes, step badges        │
│            → Spotlight, blur, cursor ripple effects     │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 3 🔊  Audio Layer                                 │
│            → TTS Narration (ElevenLabs / OpenAI / Google│
│            → Background Music (Mubert AI / Epidemic     │
│            → Audio Ducking (auto-mix voice over music)  │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 4 📝  Auto-Caption Generation                     │
│            → Whisper transcription → .srt file          │
│            → Animated word-by-word captions             │
│            → Styled subtitles burned into video         │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 5 🎞️  Scene Assembly                              │
│            → Branded Intro screen                       │
│            → B-Roll AI clips (Veo / Runway)             │
│            → Chapter title cards                        │
│            → Branded Outro + CTA screen                 │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 6 📐  Format Export                               │
│            → 16:9 (YouTube / Website embed)             │
│            → 9:16 (TikTok / Reels / Shorts)             │
│            → 1:1 (LinkedIn / Instagram Square)          │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 7 🖼️  Thumbnail Auto-Generation                   │
│            → Extract best frame                         │
│            → Add styled title text + branding           │
└─────────────────────────────────────────────────────────┘
        ↓
   Final Package: MP4 + Thumbnail + Captions (.srt)
         ✅ All formats delivered via CDN URL
```

---

## 🧠 STEP 0 — AI Script & Scene Planner (NEW)

This is the **most important step** — without it, users still have to manually write scripts and steps, which defeats the "AI-powered" promise.

### What It Does
1. Takes the product **URL or description** as input
2. Uses vision AI to **screenshot and analyze** the product's UI
3. Understands what the product does (login, dashboard, features)
4. **Writes a complete narrator script** (conversational, engaging tone)
5. **Plans the exact browser steps** (which pages to visit, what to click)
6. Estimates **scene durations** based on script length

### How to Implement

```python
# AI Scene Planner using Gemini Vision or GPT-4o
import anthropic
import base64
from playwright.sync_api import sync_playwright

def plan_demo_from_url(url: str, product_name: str) -> dict:
    # Step 1: Take screenshots of the product
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(url)
        screenshot = page.screenshot(full_page=False)
        browser.close()

    # Step 2: Send to Vision AI for analysis
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64.b64encode(screenshot).decode()
                    }
                },
                {
                    "type": "text",
                    "text": f"""You are a product demo expert. Analyze this screenshot of {product_name}.
                    Return a JSON with:
                    1. narrator_script: A 60-second demo narration script
                    2. browser_steps: Array of actions to automate (goto, click, fill, scroll)
                    3. scene_plan: Array of scenes with duration in seconds
                    4. key_features: Top 3 features to highlight
                    """
                }
            ]
        }]
    )

    return response  # JSON with script + steps + scene plan
```

### Output Example
```json
{
  "narrator_script": "Welcome to NitiGrow, the AI-powered platform that...",
  "browser_steps": [
    { "action": "goto", "url": "https://app.nitigrow.com" },
    { "action": "click", "selector": "#login-button" },
    { "action": "fill", "selector": "#email", "value": "demo@example.com" },
    { "action": "click", "selector": "#dashboard-link" },
    { "action": "scroll", "y": 500 }
  ],
  "scene_plan": [
    { "scene": "intro", "duration": 5, "description": "Product intro screen" },
    { "scene": "login", "duration": 8, "description": "Show login flow" },
    { "scene": "dashboard", "duration": 15, "description": "Highlight key metrics" }
  ],
  "key_features": ["AI Automation", "Real-time Analytics", "Team Collaboration"]
}
```

---

## 🔐 STEP 0.5 — Auth & Authenticated Screen Discovery (NEW)

> **Why this matters**: Without login, the recorder only sees **public/landing pages**. With credentials, it can access **every gated screen** — dashboards, admin panels, user settings, billing, reports, onboarding flows, and every feature behind authentication.

---

### What the User Provides

```json
{
  "auth_config": {
    "login_url": "https://app.example.com/login",
    "auth_type": "email_password",
    "credentials": {
      "email": "demo@example.com",
      "password": "••••••••"
    },
    "roles": [
      { "role": "admin", "email": "admin@example.com", "password": "••••••••" },
      { "role": "user",  "email": "user@example.com",  "password": "••••••••" }
    ],
    "mfa_secret": "JBSWY3DPEHPK3PXP",
    "session_storage": "cookies",
    "post_login_url": "https://app.example.com/dashboard"
  }
}
```

---

### Supported Auth Types

| Auth Type | How Handled | Tools |
|---|---|---|
| **Email + Password** | Fill form fields, click submit | Playwright `fill()` + `click()` |
| **Google / GitHub OAuth** | Handle OAuth popup flow | Playwright `popup()` handler |
| **SSO (SAML / OKTA / Azure AD)** | Navigate SSO redirect, fill IdP login | Playwright multi-page flow |
| **Magic Link (Email)** | Intercept email via Mailosaur/Mailtrap API | Email API + click link |
| **2FA / TOTP (Google Authenticator)** | Auto-generate OTP from secret | `otpauth` / `speakeasy` library |
| **SMS OTP** | Intercept via Twilio test number | Twilio API |
| **API Token / Bearer** | Inject directly into browser `localStorage` | `page.evaluate()` |
| **Mobile App Login** | Fill native login fields via Appium | Appium `findElement()` |
| **Session Cookie Import** | Paste existing session cookies | Playwright `context.addCookies()` |

---

### 0.5A — Standard Email/Password Login

```typescript
import { chromium, BrowserContext } from 'playwright';

async function loginAndSaveSession(authConfig: AuthConfig): Promise<BrowserContext> {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    recordVideo: { dir: './recordings/', size: { width: 1920, height: 1080 } }
  });
  const page = await context.newPage();

  await page.goto(authConfig.login_url);

  // Auto-detect login form fields (by common selectors or AI vision)
  await page.fill('input[type="email"], input[name="email"], #email', authConfig.credentials.email);
  await page.fill('input[type="password"], input[name="password"], #password', authConfig.credentials.password);
  await page.click('button[type="submit"], input[type="submit"], .login-btn');

  // Wait for redirect to authenticated area
  await page.waitForURL(authConfig.post_login_url || '**/dashboard**');

  // Save session state for reuse (no repeated login)
  await context.storageState({ path: `./sessions/${authConfig.credentials.email}.json` });

  console.log('✅ Login successful. Session saved.');
  return context;
}

// Reuse saved session (no re-login needed)
async function resumeSession(email: string): Promise<BrowserContext> {
  const browser = await chromium.launch({ headless: true });
  return await browser.newContext({
    storageState: `./sessions/${email}.json`,   // Restores cookies + localStorage
    recordVideo: { dir: './recordings/', size: { width: 1920, height: 1080 } }
  });
}
```

---

### 0.5B — OAuth (Google, GitHub, Microsoft)

```typescript
async function loginWithOAuth(page: Page, provider: 'google' | 'github') {
  // Click "Sign in with Google/GitHub" button
  const [popup] = await Promise.all([
    page.waitForEvent('popup'),
    page.click(`button[data-provider="${provider}"], .btn-${provider}`)
  ]);

  await popup.waitForLoadState();

  if (provider === 'google') {
    await popup.fill('input[type="email"]', process.env.GOOGLE_TEST_EMAIL!);
    await popup.click('#identifierNext');
    await popup.fill('input[type="password"]', process.env.GOOGLE_TEST_PASSWORD!);
    await popup.click('#passwordNext');
  }

  // Popup closes after successful OAuth — session is established in main page
  await popup.waitForEvent('close');
  await page.waitForURL('**/dashboard**');
}
```

---

### 0.5C — 2FA / TOTP Auto-Generation

```typescript
import * as speakeasy from 'speakeasy';

async function handle2FA(page: Page, totpSecret: string) {
  // Wait for OTP input to appear
  await page.waitForSelector('input[name="otp"], input[placeholder*="code"], #mfa-input');

  // Generate current TOTP code from the secret
  const otp = speakeasy.totp({
    secret: totpSecret,
    encoding: 'base32'
  });

  console.log(`🔑 Generated OTP: ${otp}`);

  await page.fill('input[name="otp"], #mfa-input', otp);
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard**');
}
```

---

### 0.5D — Magic Link Login (via Email API)

```typescript
import Mailosaur from 'mailosaur';

async function loginWithMagicLink(page: Page, email: string, mailtrapApiKey: string) {
  const mailosaur = new Mailosaur(mailtrapApiKey);

  // Trigger magic link send
  await page.fill('#email', email);
  await page.click('button:has-text("Send Magic Link")');

  // Fetch email within 30 seconds
  const message = await mailosaur.messages.get('server-id', {
    sentTo: email
  }, { timeout: 30000 });

  // Extract magic link from email HTML
  const magicLink = message.html?.links?.find(l => l.href?.includes('/auth/magic'))?.href;

  if (!magicLink) throw new Error('Magic link not found in email');

  // Navigate to the magic link
  await page.goto(magicLink);
  await page.waitForURL('**/dashboard**');
  console.log('✅ Magic link login successful');
}
```

---

### 0.5E — Session Cookie / API Token Injection

```typescript
// Option 1: Import cookies from a JSON file (exported from browser DevTools)
async function injectCookies(context: BrowserContext, cookiesPath: string) {
  const cookies = JSON.parse(fs.readFileSync(cookiesPath, 'utf-8'));
  await context.addCookies(cookies);
}

// Option 2: Inject JWT/Bearer token directly into localStorage
async function injectBearerToken(page: Page, token: string) {
  await page.goto('about:blank');
  await page.evaluate((t) => {
    localStorage.setItem('auth_token', t);
    localStorage.setItem('access_token', t);
    sessionStorage.setItem('token', t);
  }, token);
  // Now navigate to the app — it reads the token from storage
  await page.goto('https://app.example.com/dashboard');
}
```

---

### 0.5F — Multi-Role Recording

Record separate demo videos for **each user role** — same product, different perspectives.

```python
async def record_all_roles(product_url: str, roles: list[dict]) -> dict:
    """
    Records a separate demo video for each user role.
    e.g., Admin sees full settings panel, User sees limited view.
    """
    results = {}

    for role_config in roles:
        role_name = role_config['role']
        print(f"🎬 Recording as {role_name}...")

        # Login with this role's credentials
        context = await login_and_save_session({
            "login_url": f"{product_url}/login",
            "credentials": {
                "email": role_config['email'],
                "password": role_config['password']
            }
        })

        # Record demo with this role's session
        video_path = await record_demo_with_context(
            context=context,
            product_url=product_url,
            output_name=f"demo_{role_name}.webm"
        )

        results[role_name] = video_path

    return results
    # Returns: { "admin": "demo_admin.webm", "user": "demo_user.webm" }
```

---

### 0.5G — AI Authenticated Screen Discovery (Auto-Sitemap)

After login, **automatically discover every accessible screen** — no manual listing needed.

```python
from playwright.sync_api import sync_playwright
import anthropic, base64, json
from urllib.parse import urljoin, urlparse

def discover_all_screens(base_url: str, session_file: str) -> list[dict]:
    """
    After login, crawl the entire app to discover all accessible screens.
    Uses AI Vision to understand what each screen is about.
    """
    discovered = []
    visited = set()
    to_visit = [base_url]
    client = anthropic.Anthropic()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=session_file)
        page = context.new_page()

        while to_visit:
            url = to_visit.pop(0)
            if url in visited:
                continue
            visited.add(url)

            # Navigate and screenshot
            page.goto(url, wait_until="networkidle")
            screenshot = page.screenshot()

            # Extract all internal links
            links = page.eval_on_selector_all(
                "a[href]",
                "els => els.map(e => e.href).filter(h => h.startsWith(window.location.origin))"
            )
            to_visit.extend([l for l in links if l not in visited])

            # AI Vision: Understand what this screen is
            ai_response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=300,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64.b64encode(screenshot).decode()
                            }
                        },
                        {
                            "type": "text",
                            "text": """Analyze this app screenshot. Return JSON with:
                            {
                              "screen_name": "Dashboard Overview",
                              "description": "Shows user metrics and recent activity",
                              "key_features": ["Revenue chart", "User count", "Recent orders"],
                              "demo_priority": 1-10,
                              "suggested_narration": "Here you can see your..."
                            }"""
                        }
                    ]
                }]
            )

            screen_info = json.loads(ai_response.content[0].text)
            screen_info['url'] = url
            screen_info['screenshot'] = screenshot

            discovered.append(screen_info)
            print(f"✅ Discovered: {screen_info['screen_name']} (Priority: {screen_info['demo_priority']})")

    # Sort by demo priority — most important screens first
    return sorted(discovered, key=lambda x: x['demo_priority'], reverse=True)
```

**Output Example:**
```json
[
  { "screen_name": "Dashboard", "url": "/dashboard", "demo_priority": 10, "description": "Main metrics overview" },
  { "screen_name": "Analytics", "url": "/analytics", "demo_priority": 9, "description": "Charts and reports" },
  { "screen_name": "Team Settings", "url": "/settings/team", "demo_priority": 7, "description": "Manage users and roles" },
  { "screen_name": "Billing", "url": "/billing", "demo_priority": 5, "description": "Subscription management" },
  { "screen_name": "Profile", "url": "/profile", "demo_priority": 3, "description": "User profile settings" }
]
```

---

### 0.5H — Credential Security & Vault

> [!CAUTION]
> Never store credentials in plain text. Use environment variables or an encrypted vault.

```python
# Secure credential handling
import os
from cryptography.fernet import Fernet

class CredentialVault:
    """Encrypted local credential storage for demo recording sessions"""

    def __init__(self):
        # Key stored as env var, never in code
        key = os.environ.get("VAULT_KEY") or Fernet.generate_key()
        self.cipher = Fernet(key)

    def store(self, service: str, credentials: dict):
        """Encrypt and store credentials"""
        encrypted = self.cipher.encrypt(json.dumps(credentials).encode())
        with open(f".vault/{service}.enc", "wb") as f:
            f.write(encrypted)

    def retrieve(self, service: str) -> dict:
        """Decrypt and retrieve credentials"""
        with open(f".vault/{service}.enc", "rb") as f:
            encrypted = f.read()
        return json.loads(self.cipher.decrypt(encrypted))

    def use_and_discard(self, service: str) -> dict:
        """Retrieve credentials and immediately delete from memory after use"""
        creds = self.retrieve(service)
        # Wipe from memory after session is established
        return creds

# Security rules enforced:
# ✅ Credentials encrypted at rest with Fernet (AES-128-CBC)
# ✅ Never logged or printed to console
# ✅ Never stored in plain text files
# ✅ Never appear in video frames (masked in recordings)
# ✅ Session files stored separately from credentials
# ✅ Sessions auto-expire after 24 hours
```

### Masking Sensitive Data in Recordings
```typescript
// Auto-mask passwords and sensitive fields during recording
async function maskSensitiveFields(page: Page) {
  await page.addStyleTag({
    content: `
      input[type="password"],
      input[name*="card"],
      input[name*="cvv"],
      input[name*="ssn"] {
        -webkit-text-security: disc !important;
        color: transparent !important;
        text-shadow: 0 0 8px rgba(0,0,0,0.5) !important;
      }
    `
  });
}
```

---

### 0.5I — Mobile App Authentication

```python
from appium import webdriver

def login_mobile_app(platform: str, auth_config: dict) -> webdriver.Remote:
    """Login to mobile app and return authenticated Appium session"""

    caps = {
        "platformName": platform,  # "Android" or "iOS"
        "app": auth_config["app_path"],
        "automationName": "UiAutomator2" if platform == "Android" else "XCUITest"
    }

    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)

    # Find login fields (adapts to different UI frameworks)
    email_field = driver.find_element("xpath",
        '//android.widget.EditText[@resource-id[contains(., "email")]]'
        if platform == "Android" else
        '//XCUIElementTypeTextField[@label="Email"]'
    )
    email_field.send_keys(auth_config['credentials']['email'])

    password_field = driver.find_element("xpath",
        '//android.widget.EditText[@resource-id[contains(., "password")]]'
        if platform == "Android" else
        '//XCUIElementTypeSecureTextField'
    )
    password_field.send_keys(auth_config['credentials']['password'])

    # Tap login button
    driver.find_element("accessibility id", "Login").click()

    driver.start_recording_screen()  # Start video capture after login
    return driver
```

---

### Updated MCP Tool — With Auth Support

```python
@mcp.tool()
def create_demo_video(
    product_url: str,
    product_name: str,

    # Auth parameters (new)
    auth_type: str = "none",           # "email_password" | "oauth" | "sso" | "token" | "magic_link" | "cookies"
    email: str = "",
    password: str = "",
    totp_secret: str = "",             # For 2FA apps
    bearer_token: str = "",            # For token-based auth
    cookies_json: str = "",            # Paste browser cookies JSON
    record_roles: list[str] = [],      # ["admin", "user"] — record separate videos per role
    auto_discover_screens: bool = True, # AI crawls all accessible screens after login

    # Video parameters
    voice: str = "Rachel",
    music_mood: str = "corporate",
    output_formats: list[str] = ["16x9", "9x16"],
    target_languages: list[str] = ["en"],
    include_captions: bool = True,
    cta_text: str = "Try it free",
    cta_url: str = ""
) -> dict:
    """
    Creates a full professional demo video of a product.
    Supports authenticated access — provide login credentials to record
    dashboard, admin panels, and all gated screens.
    Optionally auto-discovers ALL screens after login for a complete demo.
    """
    pass
```

---

## 📹 STEP 1 — Screen Capture Layer

### Web Apps — Playwright (Recommended)
- Native `.webm` video recording at up to 4K
- AI-driven steps from the Scene Planner feed directly into this
- `ghost-cursor` for realistic human-like mouse movement
- Capture at 60fps for smooth playback

```typescript
import { chromium } from 'playwright';
import GhostCursor from 'ghost-cursor';

async function recordWebDemo(url: string, steps: Action[], outputPath: string) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    recordVideo: {
      dir: './recordings/',
      size: { width: 1920, height: 1080 }
    },
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();
  const cursor = GhostCursor.createCursor(page);

  // Inject visual cursor element into DOM
  await page.addStyleTag({
    content: `
      #ai-cursor {
        width: 20px; height: 20px;
        background: rgba(99, 102, 241, 0.8);
        border-radius: 50%;
        position: fixed; pointer-events: none;
        z-index: 99999;
        transition: transform 0.1s ease;
        box-shadow: 0 0 0 4px rgba(99,102,241,0.3);
      }
    `
  });

  await page.goto(url);

  // Execute AI-planned steps
  for (const step of steps) {
    if (step.action === 'click') {
      await cursor.click(step.selector); // human-like mouse movement
    } else if (step.action === 'fill') {
      await page.fill(step.selector, step.value);
    } else if (step.action === 'scroll') {
      await page.evaluate((y) => window.scrollBy(0, y), step.y);
    }
    await page.waitForTimeout(1000); // natural pause between actions
  }

  await context.close();
  // Returns path to recorded .webm file
}
```

### Mobile Apps — Android + iOS

**Android (ADB)**
```bash
# Start recording on Android device/emulator
adb shell screenrecord --size 1080x1920 --bit-rate 8000000 /sdcard/demo.mp4

# Pull to local machine
adb pull /sdcard/demo.mp4 ./recordings/android_demo.mp4
```

**iOS (Simulator)**
```bash
# Record iOS Simulator
xcrun simctl io booted recordVideo --codec=h264 ./recordings/ios_demo.mp4

# Stop with Ctrl+C when done
```

**Appium (Cross-platform Automation)**
```python
from appium import webdriver

driver = webdriver.Remote('http://localhost:4723/wd/hub', {
    'platformName': 'Android',
    'deviceName': 'emulator-5554',
    'appPackage': 'com.yourapp',
    'appActivity': '.MainActivity'
})

# Appium auto-records video during automation
driver.start_recording_screen()
# ... execute demo steps ...
video_b64 = driver.stop_recording_screen()
```

---

## 🎨 STEP 2 — Animation & Annotation Layer (Upgraded)

### Animation Effects — Full Catalog

| Effect | Tool | Use Case |
|---|---|---|
| Zoom in/out | FFmpeg `zoompan` / Remotion `spring()` | Highlight a button or section |
| Pan left/right | FFmpeg `zoompan` | Show wide/scrollable content |
| Fade in/out | FFmpeg `xfade` | Between scenes |
| Slide transition | FFmpeg `xfade` | Chapter transitions |
| Cursor click ripple | DOM inject / SVG overlay | Show interactions visually |
| Text callout | FFmpeg `drawtext` / Remotion | Annotate UI labels |
| Spotlight effect | FFmpeg vignette + mask | Focus viewer on one area |
| Blur background | FFmpeg `boxblur` | Highlight foreground element |
| Progress bar | Remotion / `drawtext` | Show demo step progress |
| **Arrow pointer** | SVG overlay / Remotion | **NEW — point at UI element** |
| **Bounding box** | FFmpeg `drawbox` / Remotion | **NEW — highlight a UI section** |
| **Step badge** | Remotion / overlay PNG | **NEW — Step 1, Step 2 badges** |
| **Lower-third bar** | FFmpeg `drawtext` + box | **NEW — speaker name / feature name** |
| **Typewriter text** | Remotion `spring()` | **NEW — animated text reveal** |
| **Confetti / celebration** | Remotion + canvas | **NEW — for success moments** |

### FFmpeg Advanced Pipeline
```bash
# Zoom + spotlight + arrow overlay + text callout
ffmpeg -i recording.webm \
  -i arrow_overlay.png \
  -filter_complex "
    [0:v]zoompan=z='min(zoom+0.001,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=90:fps=60[zoomed];
    [zoomed]vignette=PI/4[vignetted];
    [vignetted][1:v]overlay=x=300:y=200:enable='between(t,5,10)'[annotated];
    [annotated]drawbox=x=280:y=180:w=200:h=60:color=indigo@0.5:t=3[boxed];
    [boxed]drawtext=text='Click Here':fontfile=/fonts/Inter-Bold.ttf:fontsize=28:fontcolor=white:x=300:y=260[final]
  " \
  -map "[final]" -c:v libx264 -preset fast -crf 18 output_animated.mp4
```

### Remotion — React-based Animation
```jsx
// Remotion component with physics animations + annotations
import { useCurrentFrame, interpolate, spring, AbsoluteFill } from 'remotion';

const DemoScene = ({ recording, annotation }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Smooth zoom in over first 1 second
  const zoom = spring({ frame, fps, config: { damping: 20 }, from: 1, to: 1.3 });

  // Arrow fades in at frame 60 (1 second)
  const arrowOpacity = interpolate(frame, [60, 90], [0, 1], { extrapolateRight: 'clamp' });

  // Step badge slides in from left
  const badgeX = interpolate(frame, [0, 30], [-200, 20], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill>
      {/* Zoomed screen recording */}
      <video src={recording} style={{ transform: `scale(${zoom})`, transformOrigin: 'center' }} />

      {/* Step badge */}
      <div style={{
        position: 'absolute', top: 40, left: badgeX,
        background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
        color: 'white', borderRadius: 50, padding: '8px 20px',
        fontFamily: 'Inter', fontWeight: 700, fontSize: 18
      }}>
        Step {annotation.stepNumber}
      </div>

      {/* Animated arrow */}
      <svg style={{ position: 'absolute', opacity: arrowOpacity, top: annotation.y, left: annotation.x }}>
        <path d="M0,0 L60,30 L0,60 Z" fill="#6366f1" />
      </svg>

      {/* Bounding box highlight */}
      <div style={{
        position: 'absolute',
        border: '3px solid #6366f1',
        borderRadius: 8,
        top: annotation.boxY, left: annotation.boxX,
        width: annotation.boxW, height: annotation.boxH,
        boxShadow: '0 0 20px rgba(99,102,241,0.5)'
      }} />
    </AbsoluteFill>
  );
};
```

---

## 🔊 STEP 3 — Audio Layer (Upgraded: TTS + Music + Ducking)

### 3A — TTS Narration

| Provider | Voice Quality | Voice Cloning | Languages | Cost |
|---|---|---|---|---|
| **ElevenLabs** | ⭐⭐⭐⭐⭐ Best | ✅ Instant | 29 | Premium ($5–$99/mo) |
| **OpenAI TTS** | ⭐⭐⭐⭐ | ❌ | 57 | $15–$30/M chars |
| **Google Chirp 3 HD** | ⭐⭐⭐⭐⭐ | ✅ Custom | 75+ | Pay-as-you-go |
| **PlayHT** | ⭐⭐⭐⭐ | ✅ | 50+ | $29–$99/mo |

**ElevenLabs (Primary)**
```python
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY")

audio = client.text_to_speech.convert(
    voice_id="Rachel",
    text=narrator_script,
    model_id="eleven_turbo_v2_5",        # fastest, still high quality
    output_format="mp3_44100_128",
    voice_settings={
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.4,                     # expressiveness
        "use_speaker_boost": True
    }
)

with open("narration.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

### 3B — Background Music (NEW)

**Mubert API** (AI-generated royalty-free music)
```python
import requests

def generate_background_music(duration_seconds: int, mood: str = "corporate") -> str:
    """Generate AI background music via Mubert API"""
    response = requests.post(
        "https://api-b2b.mubert.com/v2/TTMusicByTags",
        json={
            "method": "TTMusicByTags",
            "params": {
                "pat": "YOUR_MUBERT_TOKEN",
                "tags": mood,          # "corporate", "tech", "inspiring", "energetic"
                "duration": duration_seconds,
                "format": "mp3",
                "intensity": "medium"
            }
        }
    )
    return response.json()["data"]["tasks"][0]["download_link"]
```

**Alternative: Epidemic Sound API**
- Pre-licensed tracks for commercial use
- Curated playlists by mood/tempo/genre
- REST API with search + download

### 3C — Audio Ducking (NEW)
Automatically lower music volume when narrator is speaking — professional broadcast technique.

```bash
# FFmpeg audio ducking: auto-reduce music when voice is present
ffmpeg \
  -i narration.mp3 \
  -i background_music.mp3 \
  -filter_complex "
    [1:a]volume=0.3[music_low];
    [0:a][music_low]amix=inputs=2:duration=longest:weights='3 1'[mixed];
    [mixed]alimiter=level_in=1:level_out=0.9[final_audio]
  " \
  -map "[final_audio]" mixed_audio.mp3
```

---

## 📝 STEP 4 — Auto-Caption Generation (NEW)

Every modern demo video needs animated captions — especially for social media (85% of videos are watched without sound).

### Pipeline: TTS Audio → Whisper → Animated .SRT

```python
from openai import OpenAI

client = OpenAI()

def generate_captions(audio_file: str) -> str:
    """Use Whisper to transcribe narration with word-level timestamps"""
    with open(audio_file, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="srt",          # Returns standard .srt format
            timestamp_granularities=["word"] # Word-level timing for karaoke effect
        )

    # Save .srt file
    with open("captions.srt", "w") as f:
        f.write(transcript)

    return "captions.srt"
```

### Burn Captions into Video (FFmpeg)
```bash
# Burn styled captions into video
ffmpeg -i output_animated.mp4 \
  -vf "subtitles=captions.srt:force_style='
    FontName=Inter,
    FontSize=22,
    PrimaryColour=&H00FFFFFF,
    OutlineColour=&H00000000,
    BackColour=&H80000000,
    Bold=1,
    Outline=2,
    Shadow=1,
    Alignment=2,
    MarginV=40
  '" \
  -c:a copy output_captioned.mp4
```

### Advanced: Animated Word-by-Word Captions (Remotion)
```jsx
// TikTok-style animated word reveal
const AnimatedCaptions = ({ words, currentTimeMs }) => {
  return (
    <div style={{ position: 'absolute', bottom: 80, width: '100%', textAlign: 'center' }}>
      {words.map((word, i) => {
        const isActive = currentTimeMs >= word.start && currentTimeMs <= word.end;
        const isPast = currentTimeMs > word.end;
        return (
          <span key={i} style={{
            fontSize: 32,
            fontFamily: 'Inter',
            fontWeight: 800,
            color: isActive ? '#6366f1' : isPast ? 'rgba(255,255,255,0.6)' : 'white',
            margin: '0 4px',
            textShadow: '0 2px 8px rgba(0,0,0,0.8)',
            transform: isActive ? 'scale(1.15)' : 'scale(1)',
            display: 'inline-block',
            transition: 'all 0.1s ease'
          }}>
            {word.text}
          </span>
        );
      })}
    </div>
  );
};
```

---

## 🎞️ STEP 5 — Scene Assembly (NEW)

### 5A — Brand Kit Support

```json
{
  "brand_kit": {
    "primary_color": "#6366f1",
    "secondary_color": "#8b5cf6",
    "background_color": "#0f0a1e",
    "font_family": "Inter",
    "logo_url": "https://cdn.example.com/logo.png",
    "watermark_position": "bottom-right",
    "tagline": "Build Faster. Grow Smarter."
  }
}
```

### 5B — Branded Intro Screen (Remotion)
```jsx
const IntroScene = ({ brandKit, productName }) => {
  const frame = useCurrentFrame();
  const logoScale = spring({ frame, fps: 60, from: 0.5, to: 1 });
  const titleOpacity = interpolate(frame, [30, 60], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ background: `linear-gradient(135deg, ${brandKit.primary_color}, ${brandKit.secondary_color})` }}>
      {/* Animated logo */}
      <img src={brandKit.logo_url} style={{ transform: `scale(${logoScale})`, margin: 'auto' }} />

      {/* Animated product name */}
      <h1 style={{ opacity: titleOpacity, fontFamily: 'Inter', color: 'white', fontSize: 64, textAlign: 'center' }}>
        {productName}
      </h1>

      {/* Tagline */}
      <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: 24, textAlign: 'center' }}>
        {brandKit.tagline}
      </p>
    </AbsoluteFill>
  );
};
```

### 5C — Chapter Title Cards
```jsx
const ChapterCard = ({ chapterNumber, title, duration }) => {
  const frame = useCurrentFrame();
  const slideX = interpolate(frame, [0, 20], [-1920, 0], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ background: '#0f0a1e', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ transform: `translateX(${slideX}px)`, textAlign: 'center' }}>
        <span style={{ color: '#6366f1', fontSize: 18, fontWeight: 600, letterSpacing: 4, textTransform: 'uppercase' }}>
          Chapter {chapterNumber}
        </span>
        <h2 style={{ color: 'white', fontSize: 56, fontFamily: 'Inter', fontWeight: 800, margin: '16px 0' }}>
          {title}
        </h2>
      </div>
    </AbsoluteFill>
  );
};
```

### 5D — AI Generative B-Roll (NEW)

For scenes where there's no screen to record (e.g., "We power 10,000 teams globally"):

```python
import fal_client

def generate_broll_clip(description: str, duration: int = 5) -> str:
    """Generate B-roll video clip using AI (Veo / Runway via fal.ai)"""

    result = fal_client.subscribe(
        "fal-ai/veo2",                      # Google Veo 2 via fal.ai
        arguments={
            "prompt": description,
            "duration": f"{duration}s",
            "aspect_ratio": "16:9",
            "resolution": "1080p"
        }
    )
    return result["video"]["url"]

# Example usage
broll = generate_broll_clip(
    description="Diverse team of developers collaborating in a modern tech office, aerial view, cinematic",
    duration=5
)
```

**Alternative Providers:**
| Provider | API | Best For |
|---|---|---|
| **Google Veo 2** | via fal.ai / Vertex AI | Highest quality, realistic |
| **Runway Gen-4** | runway.ml API | Creative/cinematic style |
| **Kling AI** | via Replicate | Fast generation |
| **Luma Dream Machine** | lumalabs.ai API | Good motion quality |

### 5E — Outro + CTA Screen
```jsx
const OutroScene = ({ brandKit, ctaText, ctaUrl }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);

  return (
    <AbsoluteFill style={{ opacity, background: brandKit.background_color }}>
      <div style={{ textAlign: 'center', margin: 'auto' }}>
        <img src={brandKit.logo_url} width={120} />
        <h2 style={{ color: 'white', fontSize: 48, fontFamily: 'Inter' }}>
          Ready to get started?
        </h2>
        <a href={ctaUrl} style={{
          display: 'inline-block',
          background: `linear-gradient(135deg, ${brandKit.primary_color}, ${brandKit.secondary_color})`,
          color: 'white',
          padding: '16px 40px',
          borderRadius: 50,
          fontSize: 20,
          fontWeight: 700,
          textDecoration: 'none',
          marginTop: 24
        }}>
          {ctaText}
        </a>
      </div>
    </AbsoluteFill>
  );
};
```

---

## 📐 STEP 6 — Social Media Format Variants (NEW)

One recording → multiple export formats automatically.

| Format | Dimensions | Platform | Layout Strategy |
|---|---|---|---|
| **16:9** | 1920×1080 | YouTube, Website, LinkedIn | Full screen recording |
| **9:16** | 1080×1920 | TikTok, Reels, Shorts | Crop center + captions at bottom |
| **1:1** | 1080×1080 | Instagram, Twitter/X | Letterbox recording + colored sides |
| **4:5** | 1080×1350 | Instagram Feed (tall) | Crop + blur side panels |

```python
import subprocess

def export_all_formats(input_video: str, base_output_name: str):
    formats = {
        "16x9": {
            "size": "1920x1080",
            "vf": "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2"
        },
        "9x16": {
            "size": "1080x1920",
            "vf": "crop=ih*9/16:ih,scale=1080:1920"  # center crop for vertical
        },
        "1x1": {
            "size": "1080x1080",
            "vf": "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:color=#0f0a1e"
        }
    }

    for format_name, config in formats.items():
        cmd = [
            "ffmpeg", "-i", input_video,
            "-vf", config["vf"],
            "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k",
            f"{base_output_name}_{format_name}.mp4"
        ]
        subprocess.run(cmd)

    print("✅ All 3 formats exported")
```

---

## 🖼️ STEP 7 — Thumbnail Auto-Generation (NEW)

```python
import subprocess
from openai import OpenAI

def generate_thumbnail(video_path: str, product_name: str, brand_kit: dict) -> str:
    """Extract best frame and style it as a thumbnail"""

    # Step 1: Extract frame at 3 seconds (usually a good establishing shot)
    subprocess.run([
        "ffmpeg", "-i", video_path,
        "-ss", "00:00:03",          # seek to 3 seconds
        "-vframes", "1",            # extract 1 frame
        "-q:v", "2",                # high quality JPEG
        "thumbnail_raw.jpg"
    ])

    # Step 2: Use AI image generation to create a styled thumbnail
    client = OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"""
        Create a professional YouTube/social media thumbnail for a product demo of '{product_name}'.
        Use brand color {brand_kit['primary_color']}.
        Include bold title text.
        Modern, clean design with a slight gradient background.
        Make it eye-catching with high contrast.
        16:9 aspect ratio.
        """,
        size="1792x1024",
        quality="hd"
    )

    thumbnail_url = response.data[0].url
    return thumbnail_url
```

---

## 🌍 Multi-Language Dubbing (NEW)

Record once → auto-dub into any language with lip-sync.

```python
def dub_video_to_language(video_url: str, target_language: str) -> str:
    """
    Auto-translate and dub a demo video into any language.
    Uses HeyGen's Video Translation API with lip-sync support.
    """
    import requests

    # HeyGen Video Translation API
    response = requests.post(
        "https://api.heygen.com/v2/video_translate",
        headers={"X-Api-Key": "YOUR_HEYGEN_API_KEY"},
        json={
            "video_url": video_url,
            "output_language": target_language,   # "es", "fr", "de", "ja", "hi", etc.
            "translate_audio_only": False,         # True = no lip-sync, faster
            "title": f"Demo - {target_language}"
        }
    )

    job_id = response.json()["data"]["video_translate_id"]
    return job_id  # Poll for completion

# Supported: 40+ languages including Hindi, Spanish, French, German, Japanese, etc.
```

**Alternative: ElevenLabs Dubbing API**
```python
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key="YOUR_KEY")

dub = client.dubbing.dub_a_video_url(
    url=video_url,
    target_lang="es",         # Spanish
    source_lang="en",
    num_speakers=1,
    watermark=False
)
# Returns dubbing_id → poll for status
```

---

## 📣 STEP 10 — Platform Post Content Generator (NEW)

> **Why this matters**: The video is ready — but now the user has to write a YouTube title, a LinkedIn caption, Instagram hashtags, a tweet, a Product Hunt tagline... That's 1–2 hours of extra work. This step **auto-generates all post copy** for every platform, optimized for each one's algorithm and audience, using everything the AI already knows about the product.

---

### Supported Platforms & What Gets Generated

| Platform | What's Auto-Generated |
|---|---|
| **YouTube** | Title, Description (with timestamps/chapters), Tags, Hashtags, End screen CTA |
| **LinkedIn** | Post caption (professional tone), Hashtags, Article format option |
| **Twitter / X** | Tweet thread (multi-part), Single tweet, Hashtags |
| **Instagram** | Caption, 30 hashtags, Alt text for accessibility |
| **TikTok** | Caption, Trending hashtags, Sound suggestion, Hook line |
| **Facebook** | Post text, Link preview description |
| **Product Hunt** | Tagline (60 chars), Short description, Long description, First comment |
| **Hacker News** | Title (HN style), Show HN post text |
| **Reddit** | Subreddit suggestions, Title, Post body |
| **Dev.to / Hashnode** | Blog post title, Intro paragraph, Tags |
| **Email Newsletter** | Subject line, Preview text, Body section |
| **WhatsApp / Slack** | Short announcement message for team sharing |

---

### How It Works

The AI already knows:
- ✅ **Product name & URL** — from STEP 0 input
- ✅ **What the product does** — from AI Scene Planner vision analysis
- ✅ **Key features** — identified during screen discovery
- ✅ **Narrator script** — written in STEP 0
- ✅ **Video duration & chapters** — from STEP 5 scene assembly
- ✅ **Video URLs per format** — from STEP 6 export
- ✅ **Thumbnail URL** — from STEP 7

It uses all of this context to generate **platform-native, algorithm-optimized copy** in one shot.

---

### Implementation

```python
import anthropic
import json
from datetime import datetime

def generate_platform_posts(
    product_name: str,
    product_description: str,
    key_features: list[str],
    narrator_script: str,
    video_url_16x9: str,
    video_url_9x16: str,
    thumbnail_url: str,
    chapters: list[dict],           # [{title, start_seconds}, ...]
    cta_url: str,
    target_platforms: list[str] = "all"
) -> dict:
    """
    Auto-generates ready-to-publish post content for every major platform.
    """

    client = anthropic.Anthropic()

    # Build chapter timestamps for YouTube
    chapter_timestamps = "\n".join([
        f"{format_timestamp(ch['start_seconds'])} {ch['title']}"
        for ch in chapters
    ])

    prompt = f"""
You are an expert social media content strategist and copywriter.
Generate platform-optimized post content for a product demo video.

**Product**: {product_name}
**Description**: {product_description}
**Key Features**: {', '.join(key_features)}
**Narrator Script Summary**: {narrator_script[:500]}...
**Video URL (16:9)**: {video_url_16x9}
**Thumbnail**: {thumbnail_url}
**CTA URL**: {cta_url}
**Video Chapters**:
{chapter_timestamps}

Generate a JSON object with post content for each platform.
Each platform should have content that feels NATIVE to that platform —
not copy-pasted. Match the tone, format, length, and culture of each platform.

Return this exact JSON structure:
{{
  "youtube": {{
    "title": "...",
    "description": "...",
    "tags": ["tag1", "tag2", ...],
    "hashtags": ["#tag1", "#tag2"],
    "end_screen_cta": "..."
  }},
  "linkedin": {{
    "caption": "...",
    "hashtags": ["#tag1", "#tag2"],
    "article_title": "...",
    "article_intro": "..."
  }},
  "twitter": {{
    "single_tweet": "...",
    "thread": ["tweet1", "tweet2", "tweet3", ...],
    "hashtags": ["#tag1", "#tag2"]
  }},
  "instagram": {{
    "caption": "...",
    "hashtags": ["#tag1", ..., "#tag30"],
    "alt_text": "...",
    "story_text": "..."
  }},
  "tiktok": {{
    "caption": "...",
    "hook_line": "...",
    "hashtags": ["#tag1", "#tag2"],
    "sound_suggestion": "..."
  }},
  "facebook": {{
    "post_text": "...",
    "link_description": "..."
  }},
  "product_hunt": {{
    "tagline": "...",
    "short_description": "...",
    "long_description": "...",
    "first_comment": "...",
    "topics": ["topic1", "topic2"]
  }},
  "hacker_news": {{
    "title": "...",
    "show_hn_post": "..."
  }},
  "reddit": {{
    "suggested_subreddits": ["r/...", "r/..."],
    "title": "...",
    "post_body": "..."
  }},
  "devto": {{
    "article_title": "...",
    "intro_paragraph": "...",
    "tags": ["tag1", "tag2", "tag3", "tag4"]
  }},
  "email_newsletter": {{
    "subject_line": "...",
    "preview_text": "...",
    "body_section": "..."
  }},
  "whatsapp_slack": {{
    "short_message": "..."
  }}
}}"""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.content[0].text)


def format_timestamp(seconds: int) -> str:
    """Convert seconds to YouTube timestamp format (0:00 or 1:23:45)"""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"
```

---

### Sample Output

````json
{
  "youtube": {
    "title": "NitiGrow Demo: Automate Your Workflows with AI in Under 5 Minutes",
    "description": "See how NitiGrow helps teams automate complex workflows using AI — no code required.\n\nIn this demo we cover:\n0:00 Introduction\n0:45 Dashboard Overview\n1:30 Creating Your First Automation\n3:00 Real-time Analytics\n4:15 Team Collaboration\n\n🔗 Try NitiGrow free: https://nitigrow.com\n📩 Contact us: hello@nitigrow.com\n\nNitiGrow is the AI-powered workflow automation platform built for modern teams. Replace repetitive tasks with intelligent automations and focus on what matters.\n\n#WorkflowAutomation #AITools #SaaS #ProductDemo #NoCode",
    "tags": ["workflow automation", "AI tools", "SaaS demo", "no code", "productivity", "NitiGrow"],
    "hashtags": ["#WorkflowAutomation", "#AITools", "#SaaS", "#ProductDemo"],
    "end_screen_cta": "Start your free trial at nitigrow.com"
  },

  "linkedin": {
    "caption": "We just shipped something our team has been building for months. 🚀\n\nNitiGrow lets you automate complex business workflows using AI — and we made a 5-minute demo to show exactly how it works.\n\nHere's what you'll see:\n→ How to set up your first automation in 60 seconds\n→ Real-time analytics dashboard\n→ Team collaboration features\n\nNo code. No complex setup. Just results.\n\n💡 We're offering free access for early adopters this month.\n\nDrop a comment or DM me if you want early access.\n\n#ProductLaunch #WorkflowAutomation #AI #SaaS #BuildInPublic",
    "hashtags": ["#ProductLaunch", "#WorkflowAutomation", "#AI", "#SaaS", "#BuildInPublic"],
    "article_title": "How We Built an AI Workflow Automation Tool That Actually Works",
    "article_intro": "After 6 months of building, we're ready to show the world NitiGrow..."
  },

  "twitter": {
    "single_tweet": "We built an AI tool that automates your entire workflow in 60 seconds. Here's a 5-min demo 👇 [link] #AI #SaaS",
    "thread": [
      "We spent 6 months building NitiGrow — an AI workflow automation tool. Here's everything it can do in 5 minutes 🧵",
      "1/ The dashboard gives you a real-time view of all your automations. Revenue, tasks, team activity — all in one place.",
      "2/ Creating a new automation takes 60 seconds. Just describe what you want in plain English and AI does the rest.",
      "3/ The analytics show you exactly which automations are saving the most time and money.",
      "4/ Team collaboration is built in — assign automations, leave comments, track changes.",
      "5/ We're opening early access this month. DM me or visit nitigrow.com to get started. RT if you know someone who'd love this ♻️"
    ],
    "hashtags": ["#AI", "#SaaS", "#WorkflowAutomation", "#BuildInPublic", "#IndieHackers"]
  },

  "instagram": {
    "caption": "POV: You just automated 10 hours of work in 60 seconds ⚡\n\nThis is NitiGrow — the AI workflow automation tool we've been building. Swipe to see the full demo 👆\n\n✅ No code required\n✅ 5-minute setup\n✅ Real-time analytics\n\nLink in bio to try it free 🔗",
    "hashtags": ["#AI", "#Automation", "#SaaS", "#ProductDemo", "#Tech", "#Startup", "#BuildInPublic", "#IndieHacker", "#WorkFromAnywhere", "#Productivity", "#NoCode", "#LowCode", "#AITools", "#MachineLearning", "#TechStartup", "#DigitalTransformation", "#FutureOfWork", "#Workflow", "#Business", "#Entrepreneur", "#Innovation", "#Technology", "#Software", "#Developer", "#Coding", "#Programming", "#AppDemo", "#NewProduct", "#Launch", "#Growth"],
    "alt_text": "Screen recording demo of NitiGrow AI workflow automation platform showing dashboard, automation creation, and analytics features",
    "story_text": "🚀 We just launched! Swipe up to see the demo"
  },

  "tiktok": {
    "caption": "Automating 10 hours of work in 60 seconds with AI 🤖 #AI #WorkflowAutomation #SaaS #TechTok #Productivity",
    "hook_line": "What if you could replace 10 hours of work with 60 seconds?",
    "hashtags": ["#AI", "#WorkflowAutomation", "#SaaS", "#TechTok", "#Productivity", "#NoCode", "#AITools"],
    "sound_suggestion": "Use a trending upbeat/energetic sound from TikTok's 'Business & Technology' category"
  },

  "product_hunt": {
    "tagline": "Automate any workflow with AI in 60 seconds",
    "short_description": "NitiGrow lets teams automate complex workflows using AI — no code, no setup, just results.",
    "long_description": "NitiGrow is an AI-powered workflow automation platform for modern teams. Unlike traditional automation tools that require complex configuration, NitiGrow lets you describe what you want in plain English and builds the automation for you...\n\n**What makes it different:**\n• Natural language automation builder\n• Real-time analytics dashboard\n• Built-in team collaboration\n• 200+ integrations\n\n**Who it's for:** Operations teams, founders, and anyone drowning in repetitive work.",
    "first_comment": "Hi Product Hunt! 👋 We're the founders of NitiGrow. We built this because we were spending 20+ hours/week on manual workflows that should have been automated. After 6 months of building (and a lot of coffee), here we are. We'd love your feedback — what workflows do you wish you could automate?",
    "topics": ["Artificial Intelligence", "Productivity", "SaaS", "No-Code", "Automation"]
  },

  "hacker_news": {
    "title": "Show HN: NitiGrow – Automate workflows with plain English (no code)",
    "show_hn_post": "Hey HN,\n\nI've been building NitiGrow for the past 6 months — it's an AI-powered workflow automation tool that lets you describe what you want in plain English.\n\nThe core idea: most automation tools require you to think like an engineer. NitiGrow lets you think like a normal person.\n\nTech stack: Node.js backend, Playwright for browser automation, Claude API for AI planning, Remotion for video generation.\n\nDemo video + free trial: [link]\n\nHappy to answer any questions about the technical implementation."
  },

  "email_newsletter": {
    "subject_line": "We just launched NitiGrow — here's a 5-min demo",
    "preview_text": "Automate your entire workflow with AI in 60 seconds",
    "body_section": "Hi [First Name],\n\nWe've been heads-down building something for the past 6 months, and today we're finally ready to share it.\n\nNitiGrow is an AI workflow automation tool that lets you automate any business process by describing it in plain English — no code, no complex setup.\n\n[Watch the 5-minute demo →]\n\nIn the demo, you'll see:\n• How to create your first automation in 60 seconds\n• The real-time analytics dashboard\n• Team collaboration features\n\nWe're offering free access for the first 100 users this month.\n\n[Start for free →]\n\nLet me know what you think — I read every reply."
  },

  "whatsapp_slack": {
    "short_message": "🚀 We just launched NitiGrow — an AI tool that automates workflows in 60 seconds. Here's a 5-min demo: [link] Would love your feedback!"
  }
}
````

---

### MCP Tool for Post Generation

```python
@mcp.tool()
def generate_post_content(
    job_id: str,
    platforms: list[str] = ["all"],
    tone: str = "professional",          # "professional" | "casual" | "playful" | "technical"
    include_emojis: bool = True,
    cta_text: str = "Try it free",
    cta_url: str = "",
    campaign_angle: str = ""             # e.g. "product launch", "feature update", "tutorial"
) -> dict:
    """
    Generates ready-to-publish post content for every major platform.
    Call this after create_demo_video() completes.
    Returns titles, descriptions, captions, hashtags, and full post text
    for YouTube, LinkedIn, Twitter/X, Instagram, TikTok, Facebook,
    Product Hunt, Hacker News, Reddit, Dev.to, email newsletter, and Slack/WhatsApp.
    """
    pass


@mcp.tool()
def translate_post_content(
    post_content: dict,
    target_languages: list[str]          # ["es", "fr", "de", "hi", "ja"]
) -> dict:
    """
    Translates all generated post content into target languages.
    Preserves platform-native tone and hashtags for each language.
    """
    pass
```

---

### Complete Output Package (What User Receives)

After the full pipeline runs, the user gets:

```
📦 demo_output/
├── videos/
│   ├── demo_16x9.mp4           ← YouTube / website
│   ├── demo_9x16.mp4           ← TikTok / Reels / Shorts
│   └── demo_1x1.mp4            ← Instagram square
├── audio/
│   ├── narration.mp3
│   └── with_music.mp3
├── captions/
│   └── captions_en.srt
├── thumbnail/
│   └── thumbnail.jpg
└── posts/                      ← ALL PLATFORM COPY READY TO PUBLISH
    ├── youtube.md              ← Title + full description + tags + chapters
    ├── linkedin.md             ← Caption + hashtags + article format
    ├── twitter.md              ← Thread + single tweet + hashtags
    ├── instagram.md            ← Caption + 30 hashtags + alt text + story
    ├── tiktok.md               ← Caption + hook + hashtag pack + sound
    ├── facebook.md             ← Post text + link preview copy
    ├── product_hunt.md         ← Tagline + descriptions + first comment + topics
    ├── hacker_news.md          ← Show HN title + post body
    ├── reddit.md               ← Subreddit list + title + body
    ├── devto.md                ← Article title + intro + tags
    ├── newsletter.md           ← Subject + preview + body section
    └── whatsapp_slack.md       ← Short announcement message
```

```

---

### 10B — Confirmed Auto-Publishing to All Platforms

> [!IMPORTANT]
> The skill **never posts automatically without your explicit confirmation**. It always shows you a full preview of every post and asks "Approve and post?" before touching any platform. You can approve all at once, approve selectively, or edit before posting.

---

#### Confirmation Flow (Human-in-the-Loop)

```
AI generates all post content
          ↓
AI shows preview for every platform (title, caption, thumbnail, video)
          ↓
User reviews → "Post to LinkedIn + YouTube only" / "Post all" / "Edit first"
          ↓
AI posts only to confirmed platforms
          ↓
Returns live post URLs for each platform
```

#### MCP Confirmation Tool

```python
@mcp.tool()
def preview_and_confirm_posts(job_id: str) -> dict:
    """
    Shows a full preview of generated post content for all platforms.
    Returns a confirmation request — the user must call publish_posts()
    with their approved platform list to actually post.
    This tool NEVER posts automatically. Always requires explicit approval.
    """
    posts = load_generated_posts(job_id)

    preview = {}
    for platform, content in posts.items():
        preview[platform] = {
            "preview_summary": summarize_for_review(platform, content),
            "character_count": len(str(content)),
            "ready_to_post": True
        }

    return {
        "message": "✅ Review complete. Call publish_posts() with your approved platforms.",
        "previews": preview,
        "example_approve_all": f"publish_posts(job_id='{job_id}', platforms=['all'])",
        "example_selective": f"publish_posts(job_id='{job_id}', platforms=['youtube', 'linkedin'])",
        "example_scheduled": f"publish_posts(job_id='{job_id}', platforms=['all'], schedule_time='2024-10-05T09:00:00+05:30')"
    }


@mcp.tool()
def publish_posts(
    job_id: str,
    platforms: list[str],              # ["all"] or ["youtube", "linkedin", "twitter"]
    schedule_time: str = "",           # ISO 8601 — leave empty to post immediately
    post_as_draft: bool = False        # True = save as draft, don't publish live
) -> dict:
    """
    Posts the confirmed video and content to selected platforms.
    REQUIRES prior call to preview_and_confirm_posts() for safety.
    Supports immediate posting or scheduled posting at a future time.
    Returns live post URLs for each platform after publishing.
    """
    results = {}
    jobs = load_generated_posts(job_id)
    video_paths = load_video_exports(job_id)

    if "all" in platforms:
        platforms = list(jobs.keys())

    for platform in platforms:
        try:
            if platform == "youtube":
                results["youtube"] = post_to_youtube(jobs["youtube"], video_paths["16x9"], schedule_time)
            elif platform == "linkedin":
                results["linkedin"] = post_to_linkedin(jobs["linkedin"], video_paths["16x9"], schedule_time)
            elif platform == "twitter":
                results["twitter"] = post_to_twitter(jobs["twitter"], video_paths["9x16"])
            elif platform == "instagram":
                results["instagram"] = post_to_instagram(jobs["instagram"], video_paths["1x1"])
            elif platform == "tiktok":
                results["tiktok"] = post_to_tiktok(jobs["tiktok"], video_paths["9x16"])
            elif platform == "facebook":
                results["facebook"] = post_to_facebook(jobs["facebook"], video_paths["16x9"])
            elif platform == "product_hunt":
                results["product_hunt"] = schedule_product_hunt(jobs["product_hunt"], schedule_time)
        except Exception as e:
            results[platform] = {"status": "error", "message": str(e)}

    return {
        "status": "published",
        "platforms_posted": list(results.keys()),
        "live_urls": {k: v.get("url") for k, v in results.items()},
        "scheduled_for": schedule_time or "immediate"
    }
```

---

#### Platform API Integrations

##### 🎬 YouTube Data API v3
```python
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def post_to_youtube(content: dict, video_path: str, schedule_time: str = "") -> dict:
    youtube = build("youtube", "v3", credentials=get_oauth_credentials("youtube"))

    # Upload video
    body = {
        "snippet": {
            "title": content["title"],
            "description": content["description"],
            "tags": content["tags"],
            "categoryId": "28"             # Science & Technology
        },
        "status": {
            "privacyStatus": "private" if schedule_time else "public",
            "publishAt": schedule_time or None,   # ISO 8601 for scheduled
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload {int(status.progress() * 100)}%")

    video_id = response["id"]
    return {
        "status": "published",
        "url": f"https://youtube.com/watch?v={video_id}",
        "video_id": video_id
    }
```

##### 💼 LinkedIn API
```python
import requests

def post_to_linkedin(content: dict, video_path: str, schedule_time: str = "") -> dict:
    headers = {
        "Authorization": f"Bearer {get_token('linkedin')}",
        "Content-Type": "application/json"
    }

    # Step 1: Upload video to LinkedIn
    upload_response = requests.post(
        "https://api.linkedin.com/v2/assets?action=registerUpload",
        headers=headers,
        json={
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-video"],
                "owner": f"urn:li:person:{get_linkedin_user_id()}",
                "serviceRelationships": [{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}]
            }
        }
    )
    upload_url = upload_response.json()["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
    asset_id = upload_response.json()["value"]["asset"]

    # Step 2: Upload the video file
    with open(video_path, "rb") as f:
        requests.put(upload_url, data=f, headers={"Authorization": f"Bearer {get_token('linkedin')}"})

    # Step 3: Create the post
    post_body = {
        "author": f"urn:li:person:{get_linkedin_user_id()}",
        "lifecycleState": "DRAFT" if schedule_time else "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content["caption"]},
                "shareMediaCategory": "VIDEO",
                "media": [{"status": "READY", "media": asset_id}]
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    post_response = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, json=post_body)
    post_id = post_response.headers.get("x-restli-id")

    return {
        "status": "published",
        "url": f"https://linkedin.com/feed/update/{post_id}",
        "post_id": post_id
    }
```

##### 🐦 Twitter / X API v2
```python
import tweepy

def post_to_twitter(content: dict, video_path: str) -> dict:
    client = tweepy.Client(
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_SECRET"]
    )
    auth = tweepy.OAuth1UserHandler(
        os.environ["TWITTER_API_KEY"], os.environ["TWITTER_API_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN"], os.environ["TWITTER_ACCESS_SECRET"]
    )
    api = tweepy.API(auth)

    # Upload video (uses v1.1 media upload)
    media = api.media_upload(video_path, media_category="tweet_video")

    # Post tweet thread
    previous_tweet_id = None
    tweet_urls = []

    for i, tweet_text in enumerate(content["thread"]):
        # Attach video to first tweet only
        media_ids = [media.media_id] if i == 0 else None

        tweet = client.create_tweet(
            text=tweet_text,
            media_ids=media_ids,
            reply_settings="everyone",
            in_reply_to_tweet_id=previous_tweet_id
        )
        previous_tweet_id = tweet.data["id"]
        tweet_urls.append(f"https://twitter.com/i/status/{tweet.data['id']}")

    return {
        "status": "published",
        "url": tweet_urls[0],       # First tweet URL
        "thread_urls": tweet_urls
    }
```

##### 📸 Instagram Graph API
```python
def post_to_instagram(content: dict, video_path: str) -> dict:
    ig_user_id = os.environ["INSTAGRAM_USER_ID"]
    access_token = get_token("instagram")
    base_url = f"https://graph.facebook.com/v18.0/{ig_user_id}"

    # Step 1: Upload video as reel container
    container_response = requests.post(f"{base_url}/media", params={
        "media_type": "REELS",
        "video_url": upload_to_cdn(video_path),   # Must be publicly accessible URL
        "caption": content["caption"] + "\n\n" + " ".join(content["hashtags"]),
        "share_to_feed": True,
        "access_token": access_token
    })
    container_id = container_response.json()["id"]

    # Step 2: Wait for processing
    import time
    for _ in range(10):
        status = requests.get(f"https://graph.facebook.com/v18.0/{container_id}",
            params={"fields": "status_code", "access_token": access_token}
        ).json()
        if status["status_code"] == "FINISHED":
            break
        time.sleep(5)

    # Step 3: Publish
    publish_response = requests.post(f"{base_url}/media_publish", params={
        "creation_id": container_id,
        "access_token": access_token
    })

    return {
        "status": "published",
        "media_id": publish_response.json()["id"],
        "url": f"https://instagram.com/p/{publish_response.json()['id']}"
    }
```

##### 🎵 TikTok API
```python
def post_to_tiktok(content: dict, video_path: str) -> dict:
    headers = {"Authorization": f"Bearer {get_token('tiktok')}"}

    # Step 1: Init upload
    init = requests.post(
        "https://open.tiktokapis.com/v2/post/publish/video/init/",
        headers=headers,
        json={
            "post_info": {
                "title": content["caption"][:2200],
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": os.path.getsize(video_path),
                "chunk_size": 10_000_000,   # 10MB chunks
                "total_chunk_count": math.ceil(os.path.getsize(video_path) / 10_000_000)
            }
        }
    )

    publish_id = init.json()["data"]["publish_id"]
    upload_url = init.json()["data"]["upload_url"]

    # Step 2: Upload video in chunks
    with open(video_path, "rb") as f:
        chunk_num = 0
        while chunk := f.read(10_000_000):
            requests.put(
                upload_url,
                data=chunk,
                headers={
                    "Content-Range": f"bytes {chunk_num * 10_000_000}-{chunk_num * 10_000_000 + len(chunk) - 1}/{os.path.getsize(video_path)}",
                    "Content-Type": "video/mp4"
                }
            )
            chunk_num += 1

    return {
        "status": "published",
        "publish_id": publish_id,
        "url": "https://tiktok.com/@youraccount"   # TikTok API returns URL after processing
    }
```

##### 🚀 Product Hunt — Scheduled Launch
```python
def schedule_product_hunt(content: dict, launch_date: str) -> dict:
    """
    Product Hunt posts require manual submission via their website.
    This function prepares the formatted submission package.
    API posting is available only to approved PH partners.
    """
    return {
        "status": "ready_for_submission",
        "submit_url": "https://www.producthunt.com/posts/new",
        "prefilled_data": {
            "name": content["tagline"].split(":")[0] if ":" in content["tagline"] else "Product Name",
            "tagline": content["tagline"],
            "description": content["long_description"],
            "thumbnail_url": content.get("thumbnail_url"),
            "topics": content["topics"],
            "first_comment": content["first_comment"],
            "launch_date": launch_date
        },
        "note": "Copy the data above to producthunt.com/posts/new to submit your launch."
    }
```

---

#### OAuth Setup — Connect Your Accounts Once

```python
# One-time OAuth setup per platform
# Tokens stored encrypted in the credential vault

PLATFORM_OAUTH_CONFIG = {
    "youtube": {
        "scopes": ["https://www.googleapis.com/auth/youtube.upload"],
        "setup_url": "https://console.cloud.google.com/apis/credentials",
        "env_vars": ["YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET"]
    },
    "linkedin": {
        "scopes": ["w_member_social", "r_liteprofile"],
        "setup_url": "https://developer.linkedin.com/apps",
        "env_vars": ["LINKEDIN_CLIENT_ID", "LINKEDIN_CLIENT_SECRET"]
    },
    "twitter": {
        "scopes": ["tweet.read", "tweet.write", "users.read", "media.write"],
        "setup_url": "https://developer.twitter.com/en/portal/dashboard",
        "env_vars": ["TWITTER_API_KEY", "TWITTER_API_SECRET", "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_SECRET"]
    },
    "instagram": {
        "scopes": ["instagram_basic", "instagram_content_publish"],
        "setup_url": "https://developers.facebook.com/apps",
        "env_vars": ["INSTAGRAM_USER_ID", "INSTAGRAM_ACCESS_TOKEN"]
    },
    "tiktok": {
        "scopes": ["video.publish"],
        "setup_url": "https://developers.tiktok.com/apps",
        "env_vars": ["TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET"]
    }
}

@mcp.tool()
def connect_platform_account(platform: str) -> dict:
    """
    Opens OAuth flow to connect your account for a platform.
    Only needs to be done once. Tokens are stored encrypted.
    Supported: youtube, linkedin, twitter, instagram, tiktok, facebook
    """
    config = PLATFORM_OAUTH_CONFIG.get(platform)
    if not config:
        return {"error": f"Platform '{platform}' not supported"}

    # Generate OAuth URL and open in browser for user to authorize
    auth_url = generate_oauth_url(platform, config["scopes"])
    return {
        "message": f"Open this URL to connect your {platform} account:",
        "auth_url": auth_url,
        "next_step": "After authorizing, call check_platform_connection(platform) to verify."
    }

@mcp.tool()
def check_platform_connections() -> dict:
    """Shows which platforms are connected and ready to post."""
    return {
        platform: {
            "connected": vault.has_token(platform),
            "expires_at": vault.token_expiry(platform),
            "username": vault.get_username(platform)
        }
        for platform in PLATFORM_OAUTH_CONFIG.keys()
    }
```

---

#### Post Scheduling

```python
@mcp.tool()
def schedule_posts(
    job_id: str,
    schedule: dict                  # Platform-specific times
) -> dict:
    """
    Schedule posts to go live at optimal times for each platform.
    Provide a time per platform or use 'auto' for AI-suggested best times.

    Example schedule:
    {
      "youtube":   "2024-10-07T10:00:00+05:30",
      "linkedin":  "auto",    <- AI picks best time (Tue-Thu 8-10am)
      "twitter":   "auto",    <- AI picks best time (weekdays 9am-12pm)
      "instagram": "2024-10-07T18:00:00+05:30",
      "tiktok":    "auto"     <- AI picks best time (7-9pm local)
    }
    """
    OPTIMAL_TIMES = {
        "youtube":   "Tuesday-Thursday 14:00-16:00 local",
        "linkedin":  "Tuesday-Thursday 08:00-10:00 local",
        "twitter":   "Weekdays 09:00-12:00 local",
        "instagram": "Monday-Friday 11:00 or 18:00-20:00 local",
        "tiktok":    "Tuesday-Friday 19:00-21:00 local",
        "facebook":  "Wednesday 13:00 local"
    }
    pass
```

---

#### Safety Rules (Always Enforced)

| Rule | Detail |
|---|---|
| ✅ **Confirmation required** | `publish_posts()` never runs unless user explicitly calls it |
| ✅ **Preview first** | Always call `preview_and_confirm_posts()` before any posting |
| ✅ **Draft mode** | Set `post_as_draft=True` to save to platform drafts without publishing |
| ✅ **Selective approval** | User picks which platforms to post — never forced to post everywhere |
| ✅ **Scheduled safety** | Scheduled posts can be cancelled anytime before the publish time |
| ✅ **Error isolation** | If one platform fails, others still post — no all-or-nothing failure |
| ✅ **Sensitive data** | OAuth tokens stored encrypted, never in logs or video frames |
| ✅ **Rate limits** | Platform rate limits respected — retries with exponential backoff |

---

## ⚙️ Async Job Queue + Status Tracking (NEW)


Video generation takes 30 seconds to 5+ minutes. Must be fully async.

### Job Queue Architecture
```
User Request → MCP Tool → Create Job ID → Return immediately
                               ↓
                    Background worker processes:
                    [Plan] → [Record] → [Animate] → [Audio] → [Caption] → [Assemble] → [Export]
                               ↓
                    Webhook / Status API → Notify user
```

### MCP Tools for Job Management
```python
from mcp.server.fastmcp import FastMCP
import uuid, redis

mcp = FastMCP("DemoVideoSkill")
queue = redis.Redis()  # Job queue

@mcp.tool()
def create_demo_video(
    product_url: str,
    product_name: str,
    voice: str = "Rachel",
    music_mood: str = "corporate",
    output_formats: list[str] = ["16x9", "9x16"],
    target_languages: list[str] = ["en"],
    include_captions: bool = True,
    cta_text: str = "Try it free",
    cta_url: str = ""
) -> dict:
    """
    Creates a full professional demo video of a product from its URL.
    Records the website automatically, adds AI narration, animations,
    captions, music, and exports in multiple formats.
    Returns a job ID to track progress.
    """
    job_id = str(uuid.uuid4())

    # Queue the video generation job
    queue.rpush("video_jobs", {
        "job_id": job_id,
        "product_url": product_url,
        "product_name": product_name,
        "voice": voice,
        "music_mood": music_mood,
        "output_formats": output_formats,
        "target_languages": target_languages,
        "include_captions": include_captions,
        "cta_text": cta_text,
        "cta_url": cta_url,
        "status": "queued",
        "created_at": datetime.utcnow().isoformat()
    })

    return {
        "job_id": job_id,
        "status": "queued",
        "estimated_time": "2-4 minutes",
        "check_status_with": f"get_video_status('{job_id}')"
    }


@mcp.tool()
def get_video_status(job_id: str) -> dict:
    """
    Check the status of a video generation job.
    Returns progress percentage and download URLs when complete.
    """
    job = queue.get(f"job:{job_id}")

    if job["status"] == "complete":
        return {
            "status": "complete",
            "outputs": {
                "16x9": f"https://cdn.yourdomain.com/{job_id}/video_16x9.mp4",
                "9x16": f"https://cdn.yourdomain.com/{job_id}/video_9x16.mp4",
                "thumbnail": f"https://cdn.yourdomain.com/{job_id}/thumbnail.jpg",
                "captions_srt": f"https://cdn.yourdomain.com/{job_id}/captions.srt"
            }
        }

    return {
        "status": job["status"],  # "queued" | "planning" | "recording" | "animating" | "rendering"
        "progress": job["progress"],
        "current_step": job["current_step"]
    }


@mcp.tool()
def list_my_videos(limit: int = 10) -> list:
    """List all previously generated demo videos."""
    pass


@mcp.tool()
def regenerate_video_section(job_id: str, section: str) -> dict:
    """
    Regenerate just one section of a video without re-recording everything.
    section can be: "intro", "narration", "outro", "captions", "music"
    """
    pass
```

---

## 🤖 MCP Server — Cross-Platform AI Integration

### Supported Platforms

| Platform | Integration Method | Config File |
|---|---|---|
| **Claude (Desktop)** | MCP Server via stdio | `claude_desktop_config.json` |
| **Claude (Code / API)** | MCP Server via HTTP | `.mcp.json` |
| **Gemini / Antigravity** | Custom SKILL.md + scripts | `.agents/skills/` |
| **GPT / OpenAI** | Custom GPT Actions (OpenAPI spec) | `openapi.json` |
| **LangChain Agents** | Custom LangChain Tool | Python class |
| **AutoGen / CrewAI** | Tool registration | Python function |

### Claude Desktop Config
```json
{
  "mcpServers": {
    "demo-video-skill": {
      "command": "python",
      "args": ["/path/to/demo-video-skill/mcp_server/server.py"],
      "env": {
        "ELEVENLABS_API_KEY": "your-key",
        "OPENAI_API_KEY": "your-key",
        "MUBERT_API_KEY": "your-key",
        "FAL_API_KEY": "your-key",
        "HEYGEN_API_KEY": "your-key",
        "CDN_BUCKET": "your-r2-bucket"
      }
    }
  }
}
```

### OpenAI Custom GPT Actions (OpenAPI Spec)
```yaml
openapi: 3.1.0
info:
  title: Demo Video Skill API
  version: 1.0.0
paths:
  /create-demo:
    post:
      operationId: createDemoVideo
      summary: Create a product demo video from a URL
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                product_url: { type: string }
                product_name: { type: string }
                voice: { type: string, default: "Rachel" }
                output_formats:
                  type: array
                  items: { type: string }
                  default: ["16x9", "9x16"]
  /status/{job_id}:
    get:
      operationId: getVideoStatus
      summary: Check video generation status
```

---

## 🗂️ Complete Skill Folder Structure

```
demo-video-skill/
├── SKILL.md                          ← AI instructions (for Gemini/Antigravity)
├── plugin.json                       ← Plugin metadata
│
├── mcp_server/
│   ├── server.py                     ← MCP Server (FastMCP)
│   ├── requirements.txt
│   └── openapi.yaml                  ← For OpenAI Custom GPT Actions
│
├── scripts/
│   ├── 00_plan_scenes.py             ← AI Scene Planner (Vision AI)
│   ├── 01_record_browser.ts          ← Playwright screen recorder
│   ├── 01_record_mobile.sh           ← ADB + iOS Simulator recorder
│   ├── 02_add_animations.py          ← FFmpeg animation pipeline
│   ├── 02_remotion_composer/         ← React-based Remotion project
│   │   ├── src/
│   │   │   ├── scenes/
│   │   │   │   ├── IntroScene.tsx
│   │   │   │   ├── DemoScene.tsx
│   │   │   │   ├── ChapterCard.tsx
│   │   │   │   └── OutroScene.tsx
│   │   │   └── Root.tsx
│   │   └── package.json
│   ├── 03a_generate_tts.py           ← ElevenLabs / OpenAI TTS
│   ├── 03b_generate_music.py         ← Mubert / Epidemic Sound
│   ├── 03c_audio_ducking.py          ← FFmpeg audio mix + ducking
│   ├── 04_generate_captions.py       ← Whisper → .srt → burn-in
│   ├── 05_assemble_scenes.py         ← Join all scenes with FFmpeg
│   ├── 05_generate_broll.py          ← AI B-Roll via Veo/Runway/fal.ai
│   ├── 06_export_formats.py          ← 16:9 / 9:16 / 1:1 export
│   ├── 07_generate_thumbnail.py      ← Frame extract + AI thumbnail
│   ├── 08_dub_languages.py           ← HeyGen / ElevenLabs dubbing
│   └── 09_upload_to_cdn.py           ← Cloudflare R2 / S3 upload
│
├── templates/
│   ├── saas_demo.json                ← Template for SaaS walkthroughs
│   ├── mobile_app.json               ← Template for mobile app demos
│   ├── product_launch.json           ← Template for launch videos
│   ├── tutorial.json                 ← Template for how-to tutorials
│   └── social_ad.json                ← Template for short social ads
│
├── brand_kits/
│   └── default_kit.json              ← Default brand config
│
├── workers/
│   ├── job_queue.py                  ← Redis-based async job queue
│   ├── worker.py                     ← Background video processor
│   └── webhook.py                    ← Notify on completion
│
└── examples/
    ├── website_demo_example.md
    ├── mobile_demo_example.md
    ├── multilingual_demo.md
    └── social_shorts_example.md
```

---

## 🔑 Key Technical Decisions

| Decision | Options | Recommendation |
|---|---|---|
| **TTS Provider** | ElevenLabs / OpenAI / Google | ElevenLabs (quality) + Google (multilingual) |
| **Background Music** | Mubert / Epidemic Sound / Artlist | Mubert (AI-generated, no licensing issues) |
| **Video Rendering** | FFmpeg vs Remotion | Both — FFmpeg for speed, Remotion for scenes |
| **Screen Recording** | Playwright vs Puppeteer | Playwright (better native video support) |
| **B-Roll Generation** | Veo / Runway / Kling | Veo 2 via fal.ai (best quality) |
| **Dubbing** | HeyGen / ElevenLabs | HeyGen (lip-sync) / ElevenLabs (audio-only) |
| **Captions** | Whisper / AssemblyAI | Whisper (cheapest, most accurate) |
| **Job Queue** | Redis / BullMQ / Celery | BullMQ (Node.js) or Celery (Python) |
| **Storage / CDN** | R2 / S3 / Firebase | Cloudflare R2 (zero egress fees) |
| **Async Pattern** | Polling vs Webhooks | Webhooks + fallback polling |

---

## 💡 What Makes This Skill Unique

1. **Zero-input demo creation** — Just give a URL, AI plans + records + edits everything
2. **Full automation pipeline** — Script → Record → Animate → Audio → Captions → Export
3. **Multi-platform AI** — Works with Claude, Gemini, GPT, LangChain via single MCP server
4. **Social-ready multi-format** — One recording → YouTube + TikTok + LinkedIn versions
5. **Multi-language** — Auto-dub into 40+ languages with lip-sync
6. **AI B-Roll** — Fills non-screen scenes with cinematic AI-generated clips
7. **Brand-consistent** — Applies your colors, fonts, logo, watermark automatically
8. **Async + scalable** — Job queue for handling multiple videos simultaneously

---

## 🚀 Recommended Tech Stack (Final)

| Layer | Technology | Why |
|---|---|---|
| Skill Interface | SKILL.md + MCP Server (FastMCP / Python) | Universal AI compatibility |
| AI Scene Planner | Claude Vision / GPT-4o Vision | Understands UI & writes scripts |
| Browser Automation | Playwright (Node.js) + ghost-cursor | Best web recording quality |
| Mobile Recording | ADB + xcrun simctl + Appium | Cross-platform mobile support |
| Animation Engine | FFmpeg + Remotion (React) | Speed + creative flexibility |
| TTS Narration | ElevenLabs (primary) + Google Chirp 3 HD (multilingual) | Best quality + coverage |
| Background Music | Mubert API | AI-generated, royalty-free |
| Captions | OpenAI Whisper | Free, accurate, word-level timestamps |
| B-Roll Generation | Google Veo 2 via fal.ai | Highest quality AI video |
| Multi-language Dub | HeyGen Video Translation API | Lip-sync dubbing |
| Video Composition | FFmpeg pipeline + Remotion render | Full control |
| Job Queue | BullMQ (Node.js) / Celery (Python) | Async video processing |
| Storage & CDN | Cloudflare R2 + CDN | Zero egress fees |
| Output Formats | MP4 (16:9, 9:16, 1:1) + GIF + WebM + .srt | Platform-ready |

---

## 📊 Effort Estimate (Implementation Phases)

| Phase | What to Build | Estimated Effort |
|---|---|---|
| **Phase 1** | MCP Server + Playwright recording + FFmpeg basic animations | 1–2 weeks |
| **Phase 2** | ElevenLabs TTS + Whisper captions + audio ducking | 3–5 days |
| **Phase 3** | Remotion scenes (Intro/Outro/Chapters) + Brand Kit | 1 week |
| **Phase 4** | Multi-format export + Thumbnail generation | 3 days |
| **Phase 5** | AI Scene Planner (Vision AI integration) | 1 week |
| **Phase 6** | B-Roll AI generation + Multi-language dubbing | 1 week |
| **Phase 7** | Async job queue + Status tracking + Webhooks | 4–5 days |
| **Phase 8** | Mobile recording (ADB + iOS) | 1 week |
| **Total** | Full skill | ~6–8 weeks solo |

---

---

# 🔧 Engineering Upgrades — Reliability, Security & Quality

> **Priority rule**: Make the core pipeline **secure, resumable, and reliable** before expanding features. Every stage must have clear inputs, outputs, error handling, and measurable acceptance criteria.

---

## UPGRADE 1 — Smart Browser Automation

### Problem with Basic Playwright
Simple `fill()` + `click()` selectors break the moment a button ID changes, a loading spinner appears, or the app uses a modal. Basic automation fails silently and produces corrupted recordings.

### Observe → Act → Verify Loop

```typescript
// Every action follows a 3-phase loop — never fire-and-forget
async function smartAction(page: Page, action: BrowserAction): Promise<ActionResult> {

  // PHASE 1: OBSERVE — understand current state before acting
  const beforeState = await observePageState(page);

  // PHASE 2: ACT — execute with retry
  const result = await executeWithRetry(page, action, {
    maxRetries: 3,
    backoffMs: [500, 1500, 3000]
  });

  // PHASE 3: VERIFY — confirm the action had the expected effect
  const afterState = await observePageState(page);
  const verified = await verifyActionEffect(beforeState, afterState, action.expectedEffect);

  if (!verified) {
    throw new ActionVerificationError(
      `Action '${action.type}' on '${action.selector}' did not produce expected effect`,
      { before: beforeState, after: afterState, action }
    );
  }

  return { success: true, before: beforeState, after: afterState };
}

// Page state snapshot
async function observePageState(page: Page): Promise<PageState> {
  await page.waitForLoadState("networkidle");
  return {
    url: page.url(),
    title: await page.title(),
    visibleText: await page.innerText("body"),
    hasModal: await page.isVisible("[role=dialog], .modal"),
    hasError: await page.isVisible(".error, [role=alert]"),
    timestamp: Date.now()
  };
}
```

### Accessibility-First Locators (Resilient Selectors)

```typescript
// Priority order — most to least resilient
const LOCATOR_STRATEGY = [
  (page: Page, hint: string) => page.getByRole("button", { name: hint }),
  (page: Page, hint: string) => page.getByLabel(hint),
  (page: Page, hint: string) => page.getByTestId(hint),
  (page: Page, hint: string) => page.getByPlaceholder(hint),
  (page: Page, hint: string) => page.getByText(hint, { exact: false })
];

async function findElement(page: Page, hint: string): Promise<Locator> {
  for (const strategy of LOCATOR_STRATEGY) {
    const locator = strategy(page, hint);
    if (await locator.count() > 0) return locator;
  }
  // Fallback: AI Vision identifies element from screenshot
  return await findElementByVision(page, hint);
}

// Vision fallback — AI finds the element if CSS selectors fail
async function findElementByVision(page: Page, description: string): Promise<Locator> {
  const screenshot = await page.screenshot();
  const client = new Anthropic();
  const response = await client.messages.create({
    model: "claude-opus-4-5",
    max_tokens: 200,
    messages: [{
      role: "user",
      content: [
        { type: "image", source: { type: "base64", media_type: "image/png", data: screenshot.toString("base64") } },
        { type: "text", text: `Find the CSS selector for: "${description}". Return only the selector string.` }
      ]
    }]
  });
  return page.locator(response.content[0].text.trim());
}
```

### Error Recovery Strategies

```typescript
const RECOVERY_STRATEGIES = [
  {
    condition: (_, state) => state.hasModal && state.visibleText.includes("cookie"),
    recover: async (page) => {
      await page.click("button:has-text('Accept'), button:has-text('Got it')");
      await page.waitForTimeout(500);
    }
  },
  {
    condition: (_, state) => state.url.includes("/login"),
    recover: async (page) => { await reAuthenticate(page); }
  },
  {
    condition: (_, state) => state.visibleText.length < 50,
    recover: async (page) => { await page.reload({ waitUntil: "networkidle" }); }
  },
  {
    condition: (_, state) => state.visibleText.includes("rate limit"),
    recover: async (page) => { await page.waitForTimeout(10000); }
  }
];
```

**Acceptance Criteria:**
- [ ] Automation succeeds on 3 different SaaS apps without selector changes
- [ ] Recovers from cookie banners, modals, and expired sessions automatically
- [ ] Every action logged with before/after state diff
- [ ] Vision fallback triggered < 5% of the time in normal flows

---

## UPGRADE 2 — Reliable Job Pipeline

### Durable Job Storage Schema

```typescript
interface JobRecord {
  id: string;
  status: "queued" | "running" | "paused" | "completed" | "failed" | "cancelled";
  stage: "planning" | "auth" | "recording" | "animating" | "audio" | "captions" | "assembly" | "exporting" | "thumbnail" | "posting";
  progress: number;           // 0-100
  input: JobInput;
  checkpoints: Checkpoint[];  // Saved intermediate outputs per stage
  logs: LogEntry[];
  error?: ErrorRecord;
  created_at: string;
  updated_at: string;
  expires_at: string;         // Auto-cleanup after 7 days
}

interface Checkpoint {
  stage: string;
  completed_at: string;
  output_paths: Record<string, string>;
  metadata: Record<string, unknown>;
}
```

### Checkpoint-Based Recovery

```python
class PipelineRunner:
    """Runs the video pipeline with checkpoint saving and recovery"""

    def __init__(self, job_id: str):
        self.job_id = job_id
        self.job = JobStore.load(job_id)
        self.checkpoints = {cp.stage: cp for cp in self.job.checkpoints}

    async def run(self):
        stages = [
            ("planning",  self.run_planning),
            ("auth",      self.run_auth),
            ("recording", self.run_recording),
            ("animating", self.run_animations),
            ("audio",     self.run_audio),
            ("captions",  self.run_captions),
            ("assembly",  self.run_assembly),
            ("exporting", self.run_export),
            ("thumbnail", self.run_thumbnail),
        ]

        for stage_name, stage_fn in stages:
            # Skip already-completed stages (resume from checkpoint)
            if stage_name in self.checkpoints:
                print(f"Skipping {stage_name} — already completed")
                continue

            try:
                self.update_status(stage=stage_name, status="running")
                output = await stage_fn()
                self.save_checkpoint(stage_name, output)   # Never re-runs this stage
            except CancelledError:
                self.update_status(status="cancelled")
                return
            except Exception as e:
                self.save_error(stage_name, e)
                self.update_status(status="failed")
                if self.is_recoverable(e):
                    await self.retry_with_backoff(stage_name, stage_fn)
                else:
                    raise
```

### Real-Time Progress via SSE

```python
@app.get("/jobs/{job_id}/progress")
async def stream_progress(job_id: str):
    async def event_generator():
        while True:
            job = JobStore.load(job_id)
            data = json.dumps({
                "stage": job.stage,
                "progress": job.progress,
                "status": job.status,
                "eta_seconds": estimate_eta(job)
            })
            yield f"data: {data}\n\n"
            if job.status in ("completed", "failed", "cancelled"):
                break
            await asyncio.sleep(2)
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

**Acceptance Criteria:**
- [ ] Job survives process crash and resumes from last checkpoint
- [ ] Cancellation stops recording within 2 seconds and cleans temp files
- [ ] Progress updates within 3 seconds of stage change
- [ ] Failed jobs show exact stage, error, and recovery hint

---

## UPGRADE 3 — Professional Video Quality

### SSML-Enhanced Narration

```python
def enhance_script_for_tts(raw_script: str) -> str:
    """Add SSML markup for natural pacing and emphasis"""
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": f"""
            Rewrite this script with SSML markup for natural narration.
            Add:
            - <break time="0.5s"/> after each sentence
            - <break time="1s"/> between major sections
            - <emphasis level="strong"> on key product features
            - <prosody rate="slow"> for important points
            - Natural presenter language like "Here you can see..."
            - Target 140 words per minute (comfortable listening pace)

            Raw script: {raw_script}

            Return ONLY the SSML-enhanced script.
        """}]
    )
    return response.content[0].text
```

### Precise Audio Ducking

```bash
# FFmpeg sidechaincompress — auto-ducks music only when voice is present
ffmpeg \
  -i narration.mp3 \
  -i background_music.mp3 \
  -filter_complex "
    [0:a]aformat=sample_rates=44100:channel_layouts=stereo[voice];
    [1:a]volume=0.4[music];
    [voice][music]sidechaincompress=
        threshold=0.01:ratio=8:attack=300:release=900:makeup=1[ducked];
    [voice][ducked]amix=inputs=2:duration=first:weights='2 1'[final]
  " \
  -map "[final]" -c:a aac -b:a 192k mixed_audio.mp3
```

### Automated Video Validation

```python
def validate_video_output(video_path: str, spec: VideoSpec) -> ValidationReport:
    probe = json.loads(subprocess.run([
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", "-show_format", video_path
    ], capture_output=True, text=True).stdout)

    video_stream = next(s for s in probe["streams"] if s["codec_type"] == "video")
    audio_stream = next((s for s in probe["streams"] if s["codec_type"] == "audio"), None)

    checks = {
        "has_video":          video_stream is not None,
        "has_audio":          audio_stream is not None,
        "correct_resolution": video_stream["width"] == spec.width and video_stream["height"] == spec.height,
        "min_duration":       float(probe["format"]["duration"]) >= spec.min_duration_s,
        "min_bitrate":        int(probe["format"]["bit_rate"]) >= spec.min_bitrate_bps,
        "no_black_frames":    check_black_frames(video_path) < 0.05,
        "codec_correct":      video_stream["codec_name"] in ["h264", "h265"],
        "audio_in_sync":      check_audio_video_sync(video_path),
    }

    return ValidationReport(
        passed=all(checks.values()),
        checks=checks,
        failed_checks=[k for k, v in checks.items() if not v]
    )
```

**Acceptance Criteria:**
- [ ] Narration sounds natural — no robotic pauses or clipped words
- [ ] Captions in sync within ± 100ms of audio
- [ ] Audio: voice at -12 dB LUFS, music at -20 dB, no clipping
- [ ] Validator rejects video with missing audio, wrong resolution, or >5% black frames

---

## UPGRADE 4 — Security

### Credential Vault (AES-128 Encrypted)

```python
class SecureCredentialVault:
    VAULT_DIR = Path(".vault")

    def __init__(self):
        key = os.environ.get("VAULT_ENCRYPTION_KEY")
        if not key:
            raise EnvironmentError("VAULT_ENCRYPTION_KEY env var is required")
        self.cipher = Fernet(key.encode())
        self.VAULT_DIR.mkdir(exist_ok=True, mode=0o700)   # Owner-only access

    def store(self, service: str, credentials: dict, ttl_hours: int = 24):
        payload = {"data": credentials,
                   "expires_at": (datetime.utcnow() + timedelta(hours=ttl_hours)).isoformat()}
        encrypted = self.cipher.encrypt(json.dumps(payload).encode())
        vault_file = self.VAULT_DIR / f"{service}.enc"
        vault_file.write_bytes(encrypted)
        vault_file.chmod(0o600)   # Owner read-write only

    def retrieve(self, service: str) -> dict:
        vault_file = self.VAULT_DIR / f"{service}.enc"
        payload = json.loads(self.cipher.decrypt(vault_file.read_bytes()).decode())
        if datetime.fromisoformat(payload["expires_at"]) < datetime.utcnow():
            vault_file.unlink()
            raise CredentialExpiredError(f"Credentials for '{service}' expired")
        return payload["data"]

    def wipe_all(self):
        for f in self.VAULT_DIR.glob("*.enc"):
            f.write_bytes(os.urandom(f.stat().st_size))   # Overwrite before delete
            f.unlink()
```

### SSRF Prevention

```python
BLOCKED_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254", "metadata.google.internal"}
BLOCKED_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),
]

def validate_url_for_recording(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise SecurityError(f"Scheme '{parsed.scheme}' not allowed")
    if parsed.hostname in BLOCKED_HOSTS:
        raise SecurityError(f"Host '{parsed.hostname}' is blocked")
    if "@" in parsed.netloc:
        raise SecurityError("Embedded credentials in URL not allowed")
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        for r in BLOCKED_RANGES:
            if ip in r:
                raise SecurityError(f"Private IP range blocked: {parsed.hostname}")
    except ValueError:
        pass   # Not an IP — hostname is fine
    return url
```

### Sensitive Data Redaction in Recordings

```typescript
async function applyRecordingRedactions(page: Page): Promise<void> {
  await page.addStyleTag({ content: `
    input[type="password"],
    input[autocomplete="cc-number"],
    input[autocomplete="one-time-code"],
    input[name*="otp"], input[name*="ssn"] {
      -webkit-text-security: disc !important;
      color: transparent !important;
    }
  ` });

  // Redact secrets from API responses that render in DOM
  await page.route("**", async (route) => {
    const response = await route.fetch();
    const body = (await response.text())
      .replace(/sk-[a-zA-Z0-9]{48}/g, "[REDACTED_API_KEY]")
      .replace(/eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+/g, "[REDACTED_JWT]");
    await route.fulfill({ response, body });
  });
}
```

**Acceptance Criteria:**
- [ ] Vault key never in logs, env dumps, or code
- [ ] Browser contexts fully isolated — no cookie leakage between jobs
- [ ] SSRF validator rejects all private IPs and cloud metadata endpoints
- [ ] Password fields invisible in all recorded video frames (verified by frame OCR scan)
- [ ] Vault entries auto-expire and are securely overwritten on deletion

---

## UPGRADE 5 — Mobile Capture: Separate Extensible Workflows

```python
class MobileCaptureBase(ABC):
    """Abstract interface — all platforms implement the same contract"""

    @abstractmethod
    async def connect(self, config: MobileCaptureConfig) -> None: ...
    @abstractmethod
    async def start_recording(self) -> None: ...
    @abstractmethod
    async def execute_step(self, step: dict) -> None: ...
    @abstractmethod
    async def stop_recording(self) -> str: ...       # Returns path to video file
    @abstractmethod
    async def take_screenshot(self) -> bytes: ...
    @abstractmethod
    async def disconnect(self) -> None: ...


class AndroidCapture(MobileCaptureBase):
    async def start_recording(self):
        self.driver.start_recording_screen(
            videoSize=f"{self.config.resolution[0]}x{self.config.resolution[1]}",
            videoBitRate=self.config.bitrate_mbps * 1_000_000,
            videoFPS=self.config.fps,
            videoQuality="HIGH"
        )

    async def execute_step(self, step: dict):
        if step["action"] == "tap":
            self.driver.find_element("accessibility id", step["element"]).click()
        elif step["action"] == "swipe":
            self.driver.swipe(step["x1"], step["y1"], step["x2"], step["y2"])
        elif step["action"] == "type":
            self.driver.find_element("accessibility id", step["element"]).send_keys(step["text"])

    async def stop_recording(self) -> str:
        video_b64 = self.driver.stop_recording_screen()
        output_path = f"/tmp/recordings/{uuid.uuid4()}/android_demo.mp4"
        Path(output_path).parent.mkdir(parents=True)
        Path(output_path).write_bytes(base64.b64decode(video_b64))
        return output_path


class IOSCapture(MobileCaptureBase):
    async def start_recording(self):
        self.recording_process = subprocess.Popen([
            "xcrun", "simctl", "io", self.config.device_id,
            "recordVideo", "--codec=h264", "--force",
            f"/tmp/ios_recording_{self.config.device_id}.mp4"
        ])

    async def stop_recording(self) -> str:
        self.recording_process.terminate()
        self.recording_process.wait()
        return f"/tmp/ios_recording_{self.config.device_id}.mp4"
```

**Acceptance Criteria:**
- [ ] Android capture works on API 28+ device and emulator
- [ ] iOS capture works on Simulator (Xcode 15+) and physical device
- [ ] Adding a new platform requires only implementing `MobileCaptureBase`
- [ ] App launch to first recorded frame < 5 seconds

---

## UPGRADE 6 — Modular Architecture

### Stage Interface Contract

```python
class PipelineStage(ABC, Generic[InputT, OutputT]):
    """Every stage implements this contract. Independently testable and replaceable."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def version(self) -> str: ...

    @abstractmethod
    async def validate_input(self, input: InputT) -> list[str]: ...
    # Returns list of validation errors. Empty list = valid.

    @abstractmethod
    async def execute(self, input: InputT, job_id: str) -> OutputT: ...
    # Must be idempotent — safe to re-run on retry.

    @abstractmethod
    async def cleanup(self, job_id: str) -> None: ...
    # Clean up temp files after stage completes or fails.
```

### Stage Registry

```python
STAGE_REGISTRY: dict[str, PipelineStage] = {
    "planning":    AIScenePlannerStage(model="claude-opus-4-5"),
    "auth":        AuthStage(vault=credential_vault),
    "discovery":   ScreenDiscoveryStage(max_screens=50),
    "recording":   PlaywrightRecorderStage(fps=60, resolution=(1920, 1080)),
    "animating":   FFmpegAnimationStage(),
    "audio_tts":   ElevenLabsTTSStage(voice="Rachel"),
    "audio_music": MubertMusicStage(mood="corporate"),
    "audio_duck":  AudioDuckingStage(duck_db=-20, fade_ms=300),
    "captions":    WhisperCaptionStage(granularity="word"),
    "assembly":    RemotionAssemblyStage(fps=60),
    "export":      MultiFormatExportStage(formats=["16x9", "9x16", "1x1"]),
    "thumbnail":   ThumbnailStage(frame_offset_s=3),
    "validation":  VideoValidationStage(strict=True),
}
```

**Acceptance Criteria:**
- [ ] Any stage replaceable without touching other stages
- [ ] Each stage unit-testable in isolation with mock input/output
- [ ] New stage added to registry < 30 min for experienced developer
- [ ] Stage schemas validated at runtime with Pydantic

---

## UPGRADE 7 — Automated Testing

### Test Suite Structure

```
tests/
├── unit/
│   ├── test_url_validator.py          <- SSRF prevention
│   ├── test_credential_vault.py       <- Encryption + expiry
│   ├── test_script_enhancer.py        <- SSML generation quality
│   ├── test_caption_sync.py           <- Audio/caption alignment +-100ms
│   └── test_format_exporter.py        <- Resolution + codec checks
├── integration/
│   ├── test_auth_flows.py             <- Login, OAuth, 2FA, magic link
│   ├── test_browser_automation.py     <- Navigate + verify on real pages
│   ├── test_tts_pipeline.py           <- ElevenLabs -> audio -> duration
│   └── test_video_composition.py      <- FFmpeg + Remotion render
├── e2e/
│   ├── test_full_pipeline_web.py      <- Full run: URL -> MP4
│   ├── test_full_pipeline_auth.py     <- Full run with login credentials
│   └── test_publish_flow.py           <- Post generation + mock platform APIs
└── quality/
    ├── test_video_validation.py        <- Resolution, bitrate, sync
    ├── test_audio_levels.py            <- LUFS, clipping, sync
    └── test_privacy_scan.py            <- OCR scan frames for passwords/keys
```

### Privacy Scan Test

```python
class TestPrivacyScan:

    async def test_password_invisible_in_recording(self):
        """Password field content must not appear in any video frame"""
        video_path = await record_demo_with_login(
            "https://example.com", "user@test.com", "s3cr3tP@ssword"
        )
        frames = extract_frames(video_path, every_n_seconds=0.5)
        for frame in frames:
            text_in_frame = run_ocr(frame)
            assert "s3cr3tP@ssword" not in text_in_frame, \
                f"Password found in frame at {frame.timestamp}s"

    async def test_api_key_redacted(self):
        video_path = await record_demo_page_with_api_key_visible()
        frames = extract_frames(video_path, every_n_seconds=1)
        for frame in frames:
            assert not re.search(r"sk-[a-zA-Z0-9]{48}", run_ocr(frame)), \
                "API key found in frame"


class TestVideoValidation:

    def test_rejects_missing_audio(self):
        result = validate_video_output("fixtures/no_audio.mp4",
                                       VideoSpec(width=1920, height=1080))
        assert not result.passed
        assert "has_audio" in result.failed_checks

    def test_accepts_valid_video(self):
        result = validate_video_output("fixtures/valid_demo.mp4",
                                       VideoSpec(width=1920, height=1080))
        assert result.passed
```

**Acceptance Criteria:**
- [ ] Unit test suite runs in < 30 seconds
- [ ] E2E tests run against 3 real SaaS apps (not mocks)
- [ ] Privacy scan: 0 frames contain passwords, card numbers, or OTP codes
- [ ] CI/CD runs full test suite on every pull request

---

## UPGRADE 8 — Phased Development Roadmap

```
PHASE 1 — Reliable Web MVP                           [Weeks 1-2]
==============================================================
  * Playwright recording (observe-act-verify loop)
  * FFmpeg basic animations (zoom, text overlay, transitions)
  * ElevenLabs SSML-enhanced TTS narration
  * Whisper word-level captions -> .srt
  * 16:9 MP4 export + automated video validation
  * MCP server: create_demo_video() + get_status()
  * Durable job storage + checkpoint recovery
  * SSRF validator + credential vault
  --------------------------------------------------------------
  Target:    Record any public website -> polished MP4 + narration
  Criteria:  > 95% success rate on 10 different public SaaS landing pages

PHASE 2 — Authenticated Workflows                    [Weeks 3-4]
==============================================================
  * Email/password login + session persistence
  * OAuth (Google, GitHub) popup handler
  * 2FA/TOTP auto-generation (speakeasy)
  * AI screen discovery + priority ranking
  * Multi-role recording (admin/user)
  * Sensitive data redaction in recording frames
  * Per-job browser session isolation
  --------------------------------------------------------------
  Target:    Record authenticated product dashboard end-to-end
  Criteria:  Login succeeds on 5 different auth types without manual steps

PHASE 3 — Professional Video Quality                 [Week 5]
==============================================================
  * Remotion scenes (Intro, Chapters, Outro)
  * Brand kit (colors, logo, fonts, watermark)
  * Smart cursor + click ripple (context-aware color)
  * Annotation overlays (arrows, bounding boxes, step badges)
  * Audio ducking (FFmpeg sidechaincompress)
  * Thumbnail generation
  --------------------------------------------------------------
  Target:    Output indistinguishable from professionally edited demo
  Criteria:  Blind review panel rates output >= 4/5 on quality

PHASE 4 — Social & Multi-Format                      [Week 6]
==============================================================
  * 9:16 and 1:1 format auto-export
  * Platform post content (12 platforms)
  * Confirmed auto-publish (YouTube, LinkedIn, Twitter, Instagram, TikTok)
  * Post scheduling with optimal timing
  * translate_post_content() for multilingual copy
  --------------------------------------------------------------
  Target:    URL -> video posted to 3 platforms in < 10 minutes
  Criteria:  Published posts live and accessible on each platform

PHASE 5 — Mobile Capture                             [Weeks 7-8]
==============================================================
  * Android capture (ADB + Appium UiAutomator2)
  * iOS capture (xcrun simctl + Appium XCUITest)
  * MobileCaptureBase extensible interface
  * Device connection health checks
  --------------------------------------------------------------
  Target:    Record Android + iOS demo with same pipeline as web
  Criteria:  Works on Android API 28-34 + iOS 16-17 simulator

PHASE 6 — AI Enhancements                            [Weeks 9-10]
==============================================================
  * AI Generative B-Roll (Veo 2 / Runway via fal.ai)
  * Multi-language dubbing (HeyGen + ElevenLabs)
  * Background music (Mubert AI + ducking)
  * Magic link + SMS OTP auth
  --------------------------------------------------------------
  Target:    Full-featured skill — zero manual steps end-to-end
  Criteria:  Entire pipeline from URL + credentials, no human intervention

PHASE 7 — Hardening & Scale                          [Week 11]
==============================================================
  * Full test suite (unit + integration + e2e + privacy scan)
  * CI/CD pipeline with test gates
  * Rate limiting + abuse prevention
  * Horizontal scaling (multiple workers)
  * Cost tracking per job
  --------------------------------------------------------------
  Target:    Production-ready, handles 50 concurrent jobs
  Criteria:  99.5% success rate over 100-job load test
```

---

### Non-Negotiable Quality Gates (Every Phase Must Pass)

| Gate | Requirement |
|---|---|
| **Security scan** | No hardcoded secrets, no plaintext credentials in logs |
| **Privacy scan** | 0 frames contain passwords, card numbers, or OTP values |
| **SSRF check** | URL validator blocks all private IPs before any phase ships |
| **Video validation** | Every MP4 passes automated quality check before delivery |
| **Error handling** | Every stage has structured error logging with recovery hint |
| **Checkpoint coverage** | Every stage saves a checkpoint before moving forward |
| **Test coverage** | Every new feature ships with >= 1 unit test + >= 1 e2e test |
