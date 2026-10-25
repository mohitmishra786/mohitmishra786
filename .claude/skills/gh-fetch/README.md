# gh-fetch

## Problem

Agents WebFetch `github.com` instead of `gh` or a local checkout — slower, rate-limited, poor on private repos, HTML instead of structured data.

## What it does

Unified **fetch** and **checkout** workflow for GitHub:

- **fetch** — `gh` CLI for issues, PRs, diffs, and single-file access
- **checkout** — ask-first local path or shallow temp clone when multiple file accesses are foreseen

Command table adapted from [retlehs/gh-fetch](https://github.com/retlehs/gh-fetch).

## When to install

Install when agents should reach GitHub through `gh` or local checkout instead of WebFetch.

```bash
npx skills add lucavb/skills --skill gh-fetch
```

## Examples

| User intent | Foresee | Branch |
|-------------|---------|--------|
| PR diff | one | fetch — `gh pr diff` |
| One file | one | fetch — `gh api …/contents/…` |
| "How does auth work?" | many | checkout |
| Grep repo | many | checkout |

## Prerequisites

- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated (`gh auth login`)
