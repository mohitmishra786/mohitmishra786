---
name: gh-fetch
description: >-
  GitHub fetch — gh CLI for GitHub URLs; checkout when multiple file accesses
  are foreseen. Use when the user shares a GitHub link or wants remote repo source.
---

# GitHub fetch

A **fetch** run is the same **process** every GitHub task: parse → **foresee** → **fetch** or **checkout**.

## Steps

### 1. Parse

Parse `owner/repo` (+ issue/PR number if present) from URL or user text.

**Completion criterion:** `owner/repo` identified (or user asked to clarify).

### 2. Foresee

Before **checkout**, decide: will this task need more than one file read or a repo-wide search (Grep/Glob)?

- **No** → **fetch** branch (Step 3).
- **Yes** → **checkout** branch (Step 4).
- Task expands mid-run → re-**foresee** before the second access; switch branches if needed.

**Completion criterion:** branch chosen and recorded (fetch vs checkout).

### 3. Fetch branch

Follow [GH-COMMANDS.md](GH-COMMANDS.md) for the URL type. Single file: `gh api repos/owner/repo/contents/path?ref=branch`.

**Completion criterion:** requested content returned via `gh`; no **checkout** started.

### 4. Checkout branch

Follow [CHECKOUT.md](CHECKOUT.md) — ask for local path, verify remote, clone only with approval.

**Completion criterion:** verified local path in use, or approved shallow clone at a known absolute path; Read/Grep/Glob target that tree.

## Reach

Reach GitHub through **`gh`** (**fetch** branch) or a verified **checkout** path. If `gh` is missing or unauthenticated, WebFetch is the fallback.

**Done when:** every access went through **fetch** or **checkout** per the **foresee** gate; WebFetch used only on genuine `gh` failure.
