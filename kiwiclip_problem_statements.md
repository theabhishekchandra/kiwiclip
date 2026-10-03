# 🎯 Problem Statements — KiwiClip

> **Note (scope update):** The v1 implementation lives in [`skills/kiwiclip/`](skills/kiwiclip/SKILL.md) as an installable Agent Skill, modeled on [`latent-spaces/brag`](https://github.com/latent-spaces/brag). It ships a deliberately narrow slice of the problems below — one authenticated-or-public web flow, narrated and captioned, no mobile/dubbing/auto-posting yet. See [`skills/kiwiclip/references/roadmap.md`](skills/kiwiclip/references/roadmap.md) for what's deferred and why. This document remains the full long-term problem space.

Based on the research and architecture designed for KiwiClip, this document outlines the core problems, bottlenecks, and pain points the system is explicitly built to solve. 

These problem statements define the *why* behind the architecture.

---

## 1. The Manual Workflow Bottleneck
**Problem:** Creating a high-quality product demo video is currently a disjointed, multi-tool, and highly manual process.
* **Scripting:** Requires a human to write a compelling script and align it with visual steps.
* **Recording:** Requires manual screen recording, retakes for mistakes, and careful pacing.
* **Editing:** Requires importing to Premiere/Final Cut, adding cursor effects, cutting dead space, and rendering.
* **Voiceover:** Requires recording audio separately and manually syncing it to the video timeline.
* **Impact:** A simple 2-minute demo video can take 1-3 days to produce, making it impossible to scale for frequent product updates or personalized sales outreach.

## 2. UI Automation Fragility
**Problem:** Traditional browser automation (e.g., standard Playwright/Selenium) is too brittle for autonomous video generation.
* **Selector Rot:** Hardcoded CSS selectors break whenever the engineering team updates the UI (e.g., changing a button's ID or class).
* **Silent Failures:** Standard automation scripts click blindly; if a loading spinner is present or a modal blocks the screen, the click fails, but the recording continues, resulting in a ruined video.
* **Cookie Banners & Modals:** Unexpected popups ruin the visual recording and block subsequent automated steps.
* **Impact:** High failure rates and corrupted recordings require constant human supervision and script maintenance.

## 3. Post-Production Polish & Quality
**Problem:** Automated recordings look like robotic QA tests, not professional marketing assets.
* **Lack of Context:** A raw screen recording lacks visual cues (like cursor highlights, click ripples, or zoom-ins) that tell the viewer what to focus on.
* **Robotic Audio:** Standard Text-to-Speech (TTS) engines lack natural pacing, emotion, and emphasis, making the video feel cheap and unengaging.
* **Audio Clashing:** Background music frequently drowns out the narrator if not meticulously mixed (ducked) by a human editor.
* **Impact:** AI-generated videos suffer from an "uncanny valley" of quality that harms brand perception.

## 4. Distribution, Localization & Formats
**Problem:** Repurposing a single video for global and cross-platform marketing is tedious and expensive.
* **Aspect Ratios:** A 16:9 YouTube video doesn't work on TikTok/Instagram Reels (9:16) or LinkedIn (1:1). Manually reframing videos takes hours.
* **Language Barriers:** Dubbing a video into French, Spanish, or Japanese requires hiring voice actors or manually generating new TTS and re-syncing the entire video.
* **Copywriting:** After the video is done, a marketer still has to spend 1-2 hours writing platform-specific copy (YouTube timestamps, LinkedIn articles, Twitter threads, TikTok hooks).
* **Impact:** Companies settle for English-only, single-platform distribution because repurposing is too labor-intensive.

## 5. Security & Privacy in Authenticated Recording
**Problem:** Recording authenticated dashboards introduces massive security risks.
* **Credential Leaks:** Passing raw passwords to an automation script risks exposing them in logs, environment variables, or databases.
* **Visual Data Leaks:** Typing a password or OTP on screen means the secret is permanently burned into the recorded video frames.
* **Network Vulnerabilities (SSRF):** Allowing an AI to navigate arbitrary URLs can be exploited to access internal cloud infrastructure (e.g., AWS metadata endpoints or localhost).
* **Impact:** Enterprise users cannot trust an AI system to record their secure dashboards without rigorous data protection guarantees.

## 6. System Reliability & Resumability
**Problem:** Video generation is a highly latent, resource-intensive process (taking 2–10+ minutes). 
* **State Loss:** If the system crashes, rate-limits on an API, or times out during minute 8 of a 10-minute job, all progress and API costs are lost.
* **Sync Blocking:** Running video processing synchronously ties up server threads, leading to application timeouts and poor user experience.
* **Impact:** Unreliable execution pipelines result in frustrated users and wasted compute/API resources.

## 7. Mobile Platform Fragmentation
**Problem:** Screen recording pipelines are typically built *only* for the web.
* **Ecosystem Divide:** Recording native iOS and Android apps requires entirely different infrastructure (Appium, ADB, XCUITest, Simulators) than web browsers.
* **Action Mapping:** A "click" on the web is fundamentally different from a "swipe" or "tap" on a mobile device.
* **Impact:** Companies with mobile apps are left out of automated demo generation, forcing them to maintain separate manual workflows for mobile marketing.

---

## 8. Original User Requirements (The "North Star")

The problem statements and system architecture above are directly derived from the core constraints and feature requests defined by the user. Below is the detailed breakdown of these requirements, which serve as the definitive benchmark for the product's success.

### Requirement 1: Open-Source AI Assistant Skill (MCP Integration via Git)
**User Quote:** *"I want to create new skill for claude and all other ai platform"* AND *"this is i will create only git repo and any one can use it from that"*
* **Detail:** The system must not be a centralized, closed-source web app. It must be a self-hostable Git repository exposing an MCP (Model Context Protocol) server.
* **Objective:** Anyone can clone the repository, run it locally, and connect their desktop AI assistant (Claude/Cursor/Gemini). This empowers any developer to spin up the entire video generation pipeline on their own machine, supplying their own local environment variables and securely keeping their credentials on their own local device.

### Requirement 2: Ubiquitous Product Coverage (Web + Mobile)
**User Quote:** *"...where use can create demo video of there website and mobile app etc all product"*
* **Detail:** The recording infrastructure cannot be limited to just standard Chrome web browsing. It must have dedicated pipelines capable of launching, authenticating, and interacting with native Android (.apk) and iOS (.app) applications.
* **Objective:** Ensure the skill serves as a universal marketing engine regardless of where the target product lives.

### Requirement 3: Human-Grade Video Editing & Effects
**User Quote:** *"...and you can generate all type of videos and format you can add animation effect etc, as you are doing in videos when you are editing."*
* **Detail:** The output must visually mimic the polish of a human video editor using Adobe Premiere or Final Cut. 
* **Objective:** The system must automatically apply dynamic zooms, smooth transitions, cursor click ripples, highlight boxes, and text callouts. Furthermore, it must output multiple aspect ratios (16:9 for YouTube, 9:16 for TikTok/Shorts, 1:1 for Instagram) natively, rather than just awkwardly cropping a single video.

### Requirement 4: Professional AI Voiceover Synthesis
**User Quote:** *"...also you add audio from text with your ai or generate audio from any other platform."*
* **Detail:** The skill must completely eliminate the need for a human voice actor. It must take the AI-generated script and convert it into high-fidelity, natural-sounding audio.
* **Objective:** Integration with top-tier TTS providers (like ElevenLabs or Google Cloud TTS) using SSML (Speech Synthesis Markup Language) to ensure the AI narrator pauses naturally, emphasizes key features, and breathes like a real human presenter.

### Requirement 5: Secure Authenticated Recording (Behind the Login Wall)
**User Quote:** *"...also add in this you can provide login details and all other to access all possible screens"*
* **Detail:** The system must be capable of logging into secured, private dashboards (SaaS tools, internal portals, private accounts).
* **Objective:** It must securely accept and vault user credentials (Email/Password, OAuth, 2FA/OTP tokens). More importantly, once logged in, it must use Vision AI to autonomously "discover" and map out the accessible screens behind the auth wall, determining which features are most important to highlight in the demo.

### Requirement 6: Platform-Native Post Generation
**User Quote:** *"...also write platform post details like tital decriptioin"*
* **Detail:** Video generation is only half the marketing battle. The skill must also generate the textual collateral required to distribute the video.
* **Objective:** For every video generated, the AI must output a complete package of social media copy optimized for each specific platform's algorithm. This includes YouTube titles/chapters, LinkedIn professional articles, Twitter/X thread hooks, Instagram/TikTok hashtags, and Product Hunt launch copy.

### Requirement 7: Confirmed Auto-Publishing (Human-in-the-Loop)
**User Quote:** *"...add it can also post in that platform after you confirmation"*
* **Detail:** The skill must integrate with social media APIs (LinkedIn, X, YouTube, Meta) to physically publish the generated video and copy.
* **Objective:** Strict security and quality control: the system must **never** post autonomously. It must present a preview of the video and the copy to the user within the chat interface, requiring explicit approval (`publish_posts()`) before initiating the API upload.

### Requirement 8: Architecture & Research-First Approach
**User Quote:** *"don't build any thing i want just collect knowldge about this"*
* **Detail:** The foundation of this project requires rigorous planning to avoid building a fragile, toy prototype.
* **Objective:** Before a single line of production code is executed, the entire architecture—encompassing asynchronous queues, FFmpeg pipelines, secure credential vaulting, Playwright/Appium recording environments, and AI orchestration—must be fully mapped, estimated, and vetted for feasibility.
