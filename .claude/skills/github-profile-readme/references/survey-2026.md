# 2026 Profile README Survey

This reference summarizes a live GitHub API survey run on 2026-06-15. Use it to
calibrate defaults when a user asks for a "good", "better", "modern", or
"standout" GitHub profile README but does not already have a strong style in
mind.

## Method

- Verified sample: 520 public profile README repositories where the owner login
  matched the repo name and `GET /repos/{login}/{login}/readme` returned content.
- Candidate sources: 181 profiles from
  `abhisheknaiidu/awesome-github-profile-readme` plus 339 profiles found through
  GitHub user search among followed and active public users.
- Classification: heuristic, source-level README analysis. Hybrids were assigned
  to the strongest visible lead. Treat the percentages as directional product
  guidance, not a census of all GitHub users.
- Primary online sources used: GitHub's profile README docs, the curated awesome
  profile README index, and the live profile README repositories fetched through
  the GitHub API.

## Archetype mix

| Archetype | Count | Share | What to infer |
|---|---:|---:|---|
| Minimalist / Prose-First | 206 | 39.6% | This is the safest default, not a fallback. Mature profiles often skip the widget stack. |
| Visual Showcase | 79 | 15.2% | Images and GIFs are common, but they need alt text and durable hosting. |
| Stats Dashboard | 73 | 14.0% | Stats cards are mainstream enough to support, but should not crowd out identity. |
| Self-Updating / Automated | 66 | 12.7% | Automation is a real archetype, but only for users with live feeds and upkeep tolerance. |
| Badge / Icon Card | 41 | 7.9% | Standalone badge-wall profiles are less common than badges used as components. |
| Code-as-Bio | 19 | 3.7% | Memorable niche; correctness of the code block matters. |
| Descriptive Resume | 17 | 3.3% | Less common in the wild, but high value for job-seekers with real proof links. |
| Persona / Themed | 10 | 1.9% | Deliberate persona profiles are rare; do not force this style from light emoji use. |
| Interactive / Game Mode | 9 | 1.7% | Showpiece tier only. Requires maintenance and working issue/action mechanics. |

## Feature incidence

| Feature | Count | Share | Guidance |
|---|---:|---:|---|
| Any image | 410 | 78.8% | Visuals are normal, but every image still needs meaningful alt text. |
| Centered HTML layout | 223 | 42.9% | Center art, badges, and stat rows; keep dense prose left-aligned. |
| Any shields/badge image | 215 | 41.3% | Badge rows are common as components; keep one badge style. |
| Any stats-family widget | 196 | 37.7% | Good supporting evidence for active users; poor default for quiet/senior profiles. |
| Missing or empty image alt text | 246 | 47.3% | Accessibility is the largest obvious quality gap in the sample. |
| Ten or more images | 213 | 41.0% | Common, but often noisy. Collapse or prune unless visuals are the lead. |
| No email, LinkedIn, or X/Twitter link | 213 | 41.0% | Always add at least one direct contact path when the user provides one. |
| Two or more stats widgets | 149 | 28.7% | Visible widget stacks are common enough to audit for overload. |
| Visitor counter | 114 | 21.9% | Optional flourish; it can backfire when the count is low or the service breaks. |
| Top languages card | 112 | 21.5% | Pair with the main stats card only when activity is part of the story. |
| Hard-coded raw/blob branch URL | 92 | 17.7% | Verify `main` vs `master`; branch errors silently break assets. |
| Streak card | 57 | 11.0% | Vanity metric. Use only when the user wants activity as the story. |
| Trophy row | 41 | 7.9% | Mostly decorative. Collapse or omit by default. |
| Mixed badge styles | 34 | 6.5% | Relatively rare but visibly sloppy; keep one style. |
| Blog/RSS feed block | 30 | 5.8% | Use only with a real feed and workflow setup. |
| Typing SVG | 29 | 5.6% | Recognizable but not universal. Keep it short and accessible. |
| Dark-mode `<picture>` variant | 17 | 3.3% | Underused quality marker for black/dark brand glyphs and custom art. |

## Design implications

Default to a crisp profile before a maximal one. If the user is vague, start with
Minimalist / Prose-First or Badge / Icon Card, then add only the components that
support their goal.

Treat Visual, Stats, and Self-Updating as explicit choices. They work when the
person's work, activity, or content cadence supports them. They look thin when
used to compensate for missing substance.

Make contact obvious. A profile that looks polished but gives no direct next step
fails a core visitor workflow.

Audit images hard. The sample shows lots of image use and poor alt-text hygiene.
Generated output should be better than the wild baseline: self-host important
assets, provide alt text, avoid borrowed profile assets, and preview light/dark.

Use `<details>` more than the wild does. Only 9.0% of sampled profiles used
collapsible sections, but it is the cleanest way to offer optional stats, long
skill lists, talks, certifications, and automation logs without burying the intro.

Keep widget defaults conservative:

- Visible by default: one contact row, one compact tech row or grouped list, and
  at most the stats + top-languages pair when activity matters.
- Collapse or omit by default: streak, trophies, visitor counters, snake graphs,
  exhaustive badge walls, and secondary activity widgets.
- Require explicit maintenance tolerance for: blog feeds, WakaTime, Spotify,
  now-playing cards, generated art branches, and issue-driven games.

## Quality gates

Before finalizing any generated README, check:

- The first screen states who the person is, what they build, and where to go next.
- The chosen archetype is identifiable within the first 15 lines.
- There is one dominant style and no more than one accent.
- Every URL uses the target user's username, feed, branch, and project links.
- Every image has meaningful alt text; no image contains the only copy of the intro.
- A direct contact path exists if the user provided one.
- Visible badges use one style, and long tech lists are grouped or collapsed.
- Dynamic widgets have a maintenance story, required secrets, and exact markers.
