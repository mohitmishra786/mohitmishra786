---
name: github-profile-readme
description: >-
  Create or upgrade a GitHub *profile* README — the special README.md in the
  repo named exactly after a username (github.com/<user>/<user>) that renders at
  the top of the profile page. Use this whenever someone wants to make, design,
  redesign, refresh, or "level up" their GitHub profile, set up their
  github.com/<user>/<user> repo, add stats cards / badges / a tech stack / an
  auto-updating blog feed to their profile, or asks "how do I get that box on my
  GitHub page." Trigger even when they don't say the word "README" — "make my
  GitHub look good", "personalize my GitHub", or "set up my dev profile" all
  count. It picks a coherent style for the person, drafts real markdown, wires
  any dynamic widgets correctly, and gives exact install steps.
---

# GitHub Profile README

## What this is

A GitHub **profile** README is the `README.md` inside a repo whose name is
*identical* to the account username (e.g. `github.com/octocat/octocat`). GitHub
renders it at the top of the profile page. It is the first thing recruiters,
collaborators, and curious visitors see, so it is worth getting right.

This skill turns "I want a good GitHub profile" into a finished, coherent,
accessible README in one of nine proven styles — built from the person's real
work, not generic filler. It was refreshed from a 2026 survey of 520 verified
public profile READMEs (181 curated examples plus 339 profiles found through
GitHub user search), so the defaults reflect what actually works in the wild, not
just gallery fashion.

The single most important idea: **a coherent style with real substance beats a
pile of widgets every time.** Most bad profiles fail not from too little
decoration but from too much of it wrapped around nothing specific. Lead with who
the person is and what they build; decoration is the garnish, never the meal.

## The non-negotiable mechanic

Before anything else, make sure the user understands and the setup matches this:

- The repo **must** be named exactly the username, case included
  (`<username>/<username>`).
- The file is `README.md` on the **default branch**.
- The repo must be **public**.
- The `README.md` must live in the repo root and contain content.
- Managed user accounts cannot use profile READMEs.
- Older same-name public repos created before July 2020 may need GitHub's manual
  "Share to profile" flow before the README appears.
- Note the actual default branch (`main` vs `master`). Any raw image URL that
  hardcodes the wrong branch silently 404s — a top cause of broken hero images.

If any of these is off, the README simply will not appear on the profile. Confirm
it early.

## Workflow

Follow these steps in order. Do the human parts (interview, style choice) before
writing any markdown.

1. **Interview the person.** You cannot write a specific profile from generic
   input. Gather: their name, a one-line headline/role, *what they actually
   build* (concrete, not "passionate developer"), current focus, the 3–5 links
   that genuinely matter (GitHub, site, LinkedIn/X, email), the tech they truly
   use day to day, and — critically — **how much ongoing upkeep they will
   tolerate.** Read personality cues: playful vs corporate, minimal vs maximal.
   If they're vague, ask 2–3 sharp questions rather than guessing.

2. **Pick exactly one archetype.** Use the decision guidance below,
   `references/archetypes.md`, and the survey calibration in
   `references/survey-2026.md`. Resist mixing more than two styles. When unsure,
   bias toward *less* — a clean Minimalist profile never looks bad; a kitchen-sink
   page usually does.

3. **Confirm the repo mechanic** (above): name, default branch, public.

4. **Draft the skeleton in markdown, substance first.** Heading/greeting → a
   one-to-three-line identity statement *in real prose* → the archetype-specific
   body. Write the human content before adding any decoration.

5. **Add the link row.** Prefer a tidy centered row of shields.io social badges
   or plain text links. Use real, verified URLs and a `mailto:`. Pick **one**
   badge style (`flat-square` *or* `for-the-badge`, never both) and keep it
   throughout. A polished profile without an obvious next step is unfinished, so
   include at least one direct contact path whenever the user provides one.

6. **Add tech/skills only if relevant.** Group by category, prune to what they
   actually use, one consistent icon/badge style. Skip the 30-logo wall — it
   signals padding, not range.

7. **Add dynamic widgets only if they fit the archetype.** Stats card,
   top-languages, streak, etc. Pass the **same theme** and `hide_border=true` to
   every card so they read as one system. Default to at most the stats +
   top-languages pair when activity is part of the story; tuck streaks, trophies,
   visitor counters, snake graphs, and secondary widgets inside `<details>` or
   omit them. See `references/tools.md` for each service and its caveats.

8. **Wire automation only if they'll maintain it.** If they want live content
   (blog feed, now-playing, WakaTime), use HTML comment markers plus a
   `.github/workflows/*.yml` cron and document the required secrets. See
   `references/archetypes.md` (Self-Updating) and the
   `assets/templates/self-updating-*` files. Otherwise keep it static and honest
   — stale automation that says "No activity" is worse than no automation.

9. **Polish.** Every `<img>` gets meaningful `alt` text. Black brand glyphs get a
   `<picture>` dark-mode variant. Verify every link and image renders. Check the
   narrow/mobile view. Remove every leftover GitHub default-template comment and —
   the #1 genre mistake — any *other person's* username, feed URL, branch, or
   stats URL left in a copied snippet.

10. **Write install instructions** and preview. See "Installing it" below.
    Always preview in both GitHub light and dark themes before declaring done.

## Choosing an archetype

Map the person along three axes — **maintenance tolerance, personality, and what
they want to lead with** — then pick one. Full descriptions, section skeletons,
and ready templates are in `references/archetypes.md` and `assets/templates/`.

| Archetype | 2026 sample | Lead with | Effort | Upkeep | Best for |
|---|---:|---|---|---|---|
| **Minimalist / Prose-First** | 39.6% | A few honest sentences | Low | None | Senior/experienced devs; anyone wanting signal over noise. The safest, most timeless default. |
| **Visual Showcase** | 15.2% | A hero GIF/banner/image | Medium | Low | Visual/design-minded folks; friendly first impression. |
| **Stats Dashboard** | 14.0% | Live activity cards | Medium | Low | Active daily contributors who want activity as the headline. |
| **Self-Updating / Automated** | 12.7% | Always-fresh injected content | High | Automated | People who blog/ship/stream often *and* enjoy automation. |
| **Badge / Icon Card** | 7.9% | Stack + socials at a glance | Low | Low | People who'd rather not write much. Badges are common as components, but standalone badge walls are less common than minimal prose. |
| **Code-as-Bio** | 3.7% | An About written as a code snippet | Low | Low | A memorable coder flex in the language they identify with. |
| **Descriptive Resume** | 3.3% | Narrative bio (About/Skills/Experience) | Medium | Low | Job-hunters with real credentials: roles, talks, papers, certs. |
| **Persona / Themed** | 1.9% | A strong aesthetic (anime, retro, fancy font) | Medium | Low | Those who want personality and accept some pro/accessibility tradeoffs. |
| **Interactive / Game Mode** | 1.7% | A live playable README | High | Automated | Engineers who explicitly want a showpiece and will maintain a backend. |

**Quick rule by time budget:** none → Minimalist. Low but visual → Badge or
Visual. Some → Stats, Descriptive, or Code-as-Bio. Lots/ongoing →
Self-Updating or Interactive. Pick one primary style and at most one secondary
accent.

## Survey-calibrated defaults

The 2026 survey found that Minimalist / Prose-First profiles were the largest
bucket, while images, badges, and stats were common components across multiple
styles. That changes the default stance:

- If the prompt is vague, start from a specific prose intro, contact row, and
  compact stack. Add widgets only after the user's goal justifies them.
- Treat Visual Showcase, Stats Dashboard, and Self-Updating as explicit choices,
  not automatic "level up" moves.
- Keep the first 15 lines decisive: name, role, what they build, and where a
  visitor should go next.
- Use `<details>` more aggressively than the wild baseline. It keeps optional
  proof available without making the first screen a widget pile.
- Audit accessibility harder than the average profile: the survey found missing
  or empty image alt text in 47.3% of sampled READMEs, so generated output should
  clearly beat that baseline.

## Building blocks

The reusable, copy-pasteable snippets (centered wrapper, badge rows, stats cards,
tech walls, `<details>`, code-as-bio, typing SVG, theme-aware images, auto-update
markers, table dashboards, and more) live in `references/techniques.md`, each with
placeholders and notes on when it helps. The services that power them (shields.io,
github-readme-stats, skillicons.dev, komarev, capsule-render, etc.) with their
URLs and *caveats* are in `references/tools.md` — read the caveats before using a
service, because several popular ones are dead or rate-limited and leave broken
images.

For a fast start, copy the matching file from `assets/templates/`, then replace
every `{{PLACEHOLDER}}` with the person's real data.

The helper script `scripts/build_widgets.py` emits correct, theme-consistent
markdown for the common widgets (social badges, stats cards, tech stack, typing
SVG) from simple flags — use it instead of hand-assembling fiddly URLs:

```bash
python scripts/build_widgets.py --username octocat --theme tokyonight \
  --socials linkedin:octocat,x:octocat,email:o@cat.dev \
  --stats --top-langs --stack py,ts,go,docker,react,postgres
```

## Principles (the "why")

- **Substance over decoration.** The first screen must say who they are and what
  they build, in specific prose. "Passionate developer who loves to code" wastes
  the most valuable lines on the page. This is the difference between a profile
  that looks designed and one that looks generated.
- **One coherent style, one theme.** Competing widgets and clashing badge styles
  read as "assembled from tutorials." Consistency *is* the polish.
- **Accessibility is part of quality.** Alt text on every image, real text for the
  intro (not text trapped inside an image, which is invisible to search and
  screen readers), and restraint with motion. Fancy Unicode headings get spelled
  out as gibberish by screen readers — use them knowingly or not at all.
- **Only show what you'll maintain.** Streaks, "code time," and blog feeds that go
  stale actively advertise neglect. A simple page that stays true beats a dynamic
  one that rots.
- **Scrub copied snippets.** Leaving someone else's handle, RSS feed, or stats URL
  in a pasted block is the single most common mistake in the genre. Every
  placeholder must be replaced or removed.

The full failure catalog and a pre-publish checklist are in
`references/pitfalls-checklist.md` — run the checklist before declaring the README
done.

## Installing it

Give the person these exact steps (adapt for CLI vs web):

1. Create a new **public** repo named **exactly** their username
   (`<username>/<username>`). GitHub shows a special "you found a secret!" note
   confirming it's the profile repo.
2. Add `README.md` (and an `assets/` folder for any self-hosted images, and
   `.github/workflows/` if using automation).
3. If using automation, set the required repo **secrets** (e.g. `WAKATIME_API_KEY`)
   under Settings → Secrets and variables → Actions.
4. Commit and push to the default branch.
5. Open `github.com/<username>` and confirm it renders. **Preview in both light
   and dark themes** (toggle via GitHub settings or check on a device set to each)
   and on a narrow window for mobile.

## Reference files

- `references/archetypes.md` — the nine styles in depth: definition, who it's for,
  section skeleton, and signature techniques per style. Read when choosing or
  drafting.
- `references/survey-2026.md` — the 520-profile survey: methodology,
  distribution, feature incidence, and quality gates. Read when calibrating a
  recommendation or explaining why less is often better.
- `references/techniques.md` — the building-block catalog with copy-paste snippets
  and adoption notes. Read when assembling the body.
- `references/tools.md` — every third-party service with URL, purpose, and caveats.
  Read before adding any widget.
- `references/pitfalls-checklist.md` — what makes profiles bad + the final
  pre-publish checklist. Read before finishing.
- `assets/templates/` — a starter file per archetype (plus a workflow YAML for the
  automated style). Copy and fill in.
- `scripts/build_widgets.py` — generate consistent widget markdown from flags.
