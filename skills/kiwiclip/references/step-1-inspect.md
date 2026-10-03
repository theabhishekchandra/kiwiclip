# Step 1 — Inspect

## Determine the input type

| Input | How to recognize it | Where material comes from |
|---|---|---|
| Local project | No URL given, current directory is a project | The code: README, routes, main pages, package metadata |
| Public URL | An `http(s)://` URL with no `--login` | The live, rendered page |
| Authenticated URL | A URL with `--login` | The live page, after completing the login flow in [auth.md](auth.md) |

If the input matches none of these, ask the user what to demo rather than guessing.

## Local project

Read the code directly: entry page/route, README, the main component tree, and any docs describing what the product does. Identify the 1–3 flows a user would actually perform, not every route that exists.

## Public URL

Load the page in a headless browser (not a plain HTTP fetch — most products render with JS). Screenshot it. Follow a handful of primary nav links to understand structure, but do not crawl the whole site; that's a later-phase feature (see [roadmap.md](roadmap.md)). Three to six screens is enough material for a demo.

## Authenticated URL

Before touching credentials, read [auth.md](auth.md) in full. In short:

1. Credentials must already be in environment variables (`KIWICLIP_EMAIL`, `KIWICLIP_PASSWORD`, `KIWICLIP_TOTP_SECRET`) or a local `.kiwiclip/credentials.env` file — never pasted into chat. If the user pastes a password inline, tell them to move it to an env var instead and don't repeat it back.
2. Validate the login URL and the product URL against the SSRF blocklist (`scripts/validate_url.py`) before navigating anywhere.
3. Log in once, save the session, and reuse it rather than re-authenticating per screen.
4. After login, don't auto-crawl every authenticated route. Propose the 3–4 highest-value screens for *this* flow to the user and confirm before recording. Full authenticated-sitemap discovery is a later-phase feature — see [roadmap.md](roadmap.md).

## The planning rubric

Before writing anything, be able to answer:

1. What does the product do, in one sentence?
2. Who is this demo for — a new user, a sales prospect, a docs page, a support article?
3. What's the single most important flow to show end-to-end?
4. Does showing it require login? If so, which role?
5. What are the 3–5 concrete screens/steps that make up that flow?
6. What's the one thing a viewer must understand and remember afterward?
7. Which tone fits — `walkthrough`, `tutorial`, or `marketing-demo`?
8. Which export format(s) are actually needed? (Default to just `16x9` unless told otherwise — don't render formats nobody asked for.)
9. What's the one-line summary for the platform-copy files?

**Gate:** all nine are answered before moving to Step 2.
