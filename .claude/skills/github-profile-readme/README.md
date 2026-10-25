# github-profile-readme

A [Claude](https://claude.com/claude-code) **skill** that builds a great GitHub *profile* README — the special `README.md` in the repo named after your username (`github.com/<you>/<you>`) that renders at the top of your profile page.

It was refreshed from a 2026 live survey of **520 verified public profile READMEs** across curated examples and GitHub user search, so its defaults reflect what actually works in the wild rather than whatever is trending. Instead of dumping every widget onto the page, it interviews you, picks **one coherent archetype** that fits your goals and how much upkeep you'll tolerate, drafts real markdown from your actual work, wires any dynamic widgets correctly, and gives you exact install steps.

## What's inside

- **`SKILL.md`** — the skill itself: the workflow, the archetype picker, and the principles.
- **`references/`** — load-on-demand depth: the nine archetypes, the 520-profile survey, a copy-paste technique catalog, a tools reference with caveats, and a pitfalls + pre-publish checklist.
- **`assets/templates/`** — a ready-to-fill starter for each archetype (plus an Actions workflow for the self-updating style).
- **`scripts/build_widgets.py`** — generates consistent, theme-matched widget markdown (badges, stats cards, tech stack, typing SVG) from simple flags.

## The nine archetypes

Minimalist / Prose-First · Badge / Icon Card · Stats Dashboard · Descriptive Resume · Code-as-Bio · Self-Updating / Automated · Visual Showcase · Persona / Themed · Interactive / Game Mode.

The skill helps you pick exactly one (plus at most one accent) based on your maintenance tolerance, personality, and what you want to lead with.

## How it's packaged

This repo *is* an **Agent Skill** — `SKILL.md` sits at the root with the required `name` / `description` frontmatter, and `references/`, `assets/`, and `scripts/` are the standard supporting folders. [Agent Skills](https://www.anthropic.com/news/skills) is an open `SKILL.md` standard introduced by Anthropic and now read natively by Claude Code, Cursor, Windsurf, OpenAI Codex, Gemini CLI, and others. Because the format is identical everywhere, the same folder installs into any of them — you just drop it in that tool's skills directory.

## Install

### Easiest — paste this prompt to your coding agent

Copy the block below into Claude Code, Cursor, Codex, Windsurf, or any coding agent. It installs **only this skill** and does nothing else:

```text
Install the GitHub profile README agent skill for me, and nothing else.

1. Figure out which coding agent you are and your skills directory:
   - Claude Code → ~/.claude/skills/
   - Cursor      → ~/.cursor/skills/
   - OpenAI Codex → ~/.codex/skills/
   - Windsurf    → .windsurf/skills/  (project-local)
   - otherwise   → your documented global skills directory
2. Clone https://github.com/boffti/github-profile-readme into
   <that directory>/github-profile-readme
   (use: git clone https://github.com/boffti/github-profile-readme <dir>/github-profile-readme)
3. Confirm SKILL.md exists at the root of the cloned folder.
4. Do not modify any other files, settings, or skills. Report the final install path and stop.
```

Restart the agent (or start a new session) so it picks up the skill.

### Or install it yourself

Pick your agent. Each command clones the skill into that tool's skills folder; on the next session the agent discovers it automatically.

**Claude Code** — `~/.claude/skills/` (global) or `.claude/skills/` (per-project)

```sh
git clone https://github.com/boffti/github-profile-readme ~/.claude/skills/github-profile-readme
```

Or with the cross-agent CLI installer:

```sh
npx skills add https://github.com/boffti/github-profile-readme    # anthropics/skills CLI
```

**Cursor** — `~/.cursor/skills/` (global) or `.cursor/skills/` (per-project)

```sh
git clone https://github.com/boffti/github-profile-readme ~/.cursor/skills/github-profile-readme
```

**OpenAI Codex** — `~/.codex/skills/` (global) or `.codex/skills/` (per-project)

```sh
git clone https://github.com/boffti/github-profile-readme ~/.codex/skills/github-profile-readme
```

**Windsurf** — `.windsurf/skills/` (per-project only; no global dir)

```sh
git clone https://github.com/boffti/github-profile-readme .windsurf/skills/github-profile-readme
```

> Other SKILL.md-aware agents (Aider, Gemini CLI, Kilo Code, OpenCode, Antigravity, …) follow the same pattern — clone into their skills directory. A universal installer like [`skillport`](https://github.com/gotalab/skillport) or [`openskills`](https://github.com/numman-ali/openskills) can place it for any of them.

## Use it

Once installed, just ask in plain language — the skill triggers on intent, no command needed:

> *"help me make my GitHub profile README"* · *"make my GitHub look good"* · *"set up my dev profile"*

In Cursor or Codex you can also invoke it explicitly by typing `/` and picking `github-profile-readme`.

**Standalone (no agent):** the `references/` and `assets/templates/` files are plain markdown you can read and copy by hand, and `scripts/build_widgets.py` runs on any Python 3.

```sh
python scripts/build_widgets.py --username octocat --theme tokyonight \
  --socials linkedin:octocat,email:o@cat.dev --stats --top-langs --stack py,ts,go,docker
```

## Publishing your own copy

To make a fork installable by others: keep the repo **public** with `SKILL.md` at the root and a clear `description` (that line is what every agent uses to decide when to fire the skill). That's all the install commands above need. To go further, submit it to a marketplace — open a PR to [anthropics/skills](https://github.com/anthropics/skills), or list it on a directory like [skillsmp.com](https://skillsmp.com/) — or bundle it into a Claude Code plugin marketplace so users can `/plugin install` it.

## License

[MIT](./LICENSE). Use it, fork it, build on it.
