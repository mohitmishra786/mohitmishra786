# writing-commit-messages

## Problem

Agents write commit subjects that restate the diff ("add validation to form", "update config") instead of explaining **why** the change was necessary. Reviewers see what changed but not the reasoning, constraints, or trade-offs. Worse, agents skip the pass because parent workflows (`git status` → `git diff` → `git log` → commit) look like commit prep is already done.

## What it does

**Hard gate** before every `git commit`: learn repo style, bound the staged diff, write a why-grounded message, cross-check against the patch, and state the chosen subject in the reply before committing. Collapses duplicate git prep from user rules into one pass so nothing else substitutes for it.

## When to install

Install when agents write commits for you and you want messages that earn their place in `git log`, not just describe the patch.

```bash
npx skills add lucavb/skills --skill writing-commit-messages
```

## Wiring parent workflows

Parent rules and skills must point here explicitly — otherwise agents take the shortest path to `git commit`.

| Parent workflow | Add this line before commit |
|-----------------|----------------------------|
| Cursor user rule `committing-changes-with-git` | Before commit, complete the writing-commit-messages skill pass (steps 1–4; body + cross-check). |
| Domain deploy skill (e.g. home-ansible-session) | Run writing-commit-messages pass (steps 1–4), then commit and push. |
| Repo `AGENTS.md` Git section | Before commit: writing-commit-messages pass (steps 1–4). |

[ticket-to-pr-pipeline](../ticket-to-pr-pipeline/SKILL.md) Phase 5 already references this pass.

## Prerequisites

None. Works with any agent that can run `git log` and `git commit`.
