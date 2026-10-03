# /kiwiclip

**You shipped it. Now show how it works.**

`/kiwiclip` is an agent skill that turns a product — a local project, a live URL, or a live URL behind a login — into a short, narrated, captioned demo walkthrough video, plus ready-to-paste platform copy. One command, runs entirely on your own machine with your own credentials and API keys.

It's deliberately narrow for v1: one real flow, shown accurately, explained well. No mobile, no auto-posting, no twelve-platform blast. See [`skills/kiwiclip/references/roadmap.md`](skills/kiwiclip/references/roadmap.md) for what's deferred and why.

## Quick start

This works today, straight from a clone of this repo — no GitHub account or published plugin needed.

1. **Install the script dependencies** (from the repo root):

   ```bash
   pip install -r skills/kiwiclip/scripts/requirements.txt
   playwright install chromium
   ```

2. **Set a TTS key** — narration is on by default, and captions always use OpenAI's Whisper regardless of which TTS provider you pick:

   ```bash
   export ELEVENLABS_API_KEY=...   # best narration quality, or:
   export OPENAI_API_KEY=...       # fallback for narration, and required for captions either way
   ```

   No keys yet? Run with `--no-voice --no-captions` and skip this step for now.

3. **Make the skill visible to your agent.** Claude Code and opencode already pick it up automatically from this repo's `.claude/skills/kiwiclip/` / `.opencode/skills/kiwiclip/` symlinks — just open this folder as your project. For any other agent, copy it in:

   ```bash
   rsync -a --exclude '.DS_Store' skills/kiwiclip/ ~/.claude/skills/kiwiclip/
   ```

   Restart your agent after copying.

4. **Run it:**

   ```text
   let's /kiwiclip
   /kiwiclip https://app.example.com --login
   /kiwiclip --tone tutorial --duration 90
   ```

   Credentials for `--login` runs come from environment variables (`KIWICLIP_EMAIL`, `KIWICLIP_PASSWORD`, `KIWICLIP_TOTP_SECRET`) or a local, gitignored `.kiwiclip/credentials.env` — never from chat text. See [`skills/kiwiclip/references/auth.md`](skills/kiwiclip/references/auth.md).

You get a `kiwiclip-output/` folder with the plan, the rendered video, a thumbnail, captions, and platform-copy files. Nothing gets posted anywhere — that stays your call.

## Install as a plugin (once this repo is on GitHub)

The steps above are enough to use `/kiwiclip` from this checkout. These installers are for pulling it into *other* projects, once you've pushed this repo somewhere (replace `theabhishekchandra` with where you put it):

**Claude Code:**

```bash
/plugin marketplace add theabhishekchandra/kiwiclip
/plugin install kiwiclip@kiwiclip
```

**Codex:**

```bash
codex plugin marketplace add theabhishekchandra/kiwiclip
codex plugin add kiwiclip@kiwiclip
```

**Any other agent** (Cursor, Copilot, Gemini CLI, opencode, and more) via the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills add https://github.com/theabhishekchandra/kiwiclip --skill kiwiclip
```

### Also works with

This repo exposes the skill at every agent's standard discovery path via symlinks — no extra config needed.

| Agent | How it discovers |
|---|---|
| **Claude Code** | `.claude/skills/kiwiclip/` (in addition to the `.claude-plugin/` marketplace install above) |
| **Codex CLI** | Reads `.agents/skills/kiwiclip/`, walking up to repo root |
| **opencode** | Auto-detects from `.opencode/skills/kiwiclip/` |
| **Other agents** | Point custom instructions at `skills/kiwiclip/SKILL.md` |

## Requirements

- An agent that supports Agent Skills — Claude Code, opencode, Codex CLI, or any agent with custom instructions.
- Python 3.9+ and `ffmpeg`/`ffprobe` on `PATH`.
- A TTS provider key (`ELEVENLABS_API_KEY` or `OPENAI_API_KEY`) if narration is on (the default), and `OPENAI_API_KEY` specifically for captions (Whisper), even if ElevenLabs is doing the narration.
- Optional: `pytesseract` + the `tesseract` binary, for the automated privacy scan in Step 3. Without them, `privacy_scan.py` prints a clear "skipped" warning instead of silently passing — the skill then asks you to eyeball a few frames yourself.

## What's in this repo

- `skills/kiwiclip/SKILL.md` — the skill itself, with step-by-step references and runnable scripts under `skills/kiwiclip/references/` and `skills/kiwiclip/scripts/`
- `plugin.json` — portable Agent Plugins manifest
- `.claude-plugin/`, `.codex-plugin/` — per-agent plugin manifests
- `.claude/skills/kiwiclip/`, `.agents/skills/kiwiclip/`, `.opencode/skills/kiwiclip/` — symlinks → `skills/kiwiclip/` for per-agent discovery
- `kiwiclip_research.md`, `kiwiclip_problem_statements.md` — the original, much larger research pass. Still useful background; see the note at the top of each for how the scope here narrowed from it.

## License

MIT — see [LICENSE](LICENSE).
