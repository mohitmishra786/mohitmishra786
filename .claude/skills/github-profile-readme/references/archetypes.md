# Archetypes

Nine profile styles, refreshed from a 2026 survey of 520 verified public profile
READMEs. Pick **one** primary archetype and at most one secondary accent. Each
entry gives the definition, who it suits, the section skeleton (top to bottom),
the signature techniques, and the traps specific to that style. A ready-to-fill
starter for each lives in `../assets/templates/`.

Adoption note: in the 520-profile survey, **Minimalist / Prose-First** was the
largest bucket at 39.6%. Visual, Stats, and Self-Updating profiles were common
secondary clusters, while Persona and Interactive profiles were rare showpieces.
Badges appeared often as components, but standalone badge-wall profiles were not
the dominant style. Flash is memorable when done well and embarrassing when done
badly. Default toward restraint.

| Archetype | 2026 sample share |
|---|---:|
| Minimalist / Prose-First | 39.6% |
| Visual Showcase | 15.2% |
| Stats Dashboard | 14.0% |
| Self-Updating / Automated | 12.7% |
| Badge / Icon Card | 7.9% |
| Code-as-Bio | 3.7% |
| Descriptive Resume | 3.3% |
| Persona / Themed | 1.9% |
| Interactive / Game Mode | 1.7% |

---

## 1. Minimalist / Prose-First

**Template:** `minimalist.md` · **Effort:** low · **Upkeep:** none · **2026
sample:** 39.6%

A restrained, text-first README: a quiet heading, one to three lines of real
prose, a short bullet list, a handful of links. Deliberately skips the wall of
badges and stat cards. The safest, most timeless choice — it flatters senior and
experienced developers, and a clean minimal profile *never* looks bad.

**Best for:** senior devs, designers, OSS maintainers; anyone who values signal
over noise and would rather state their work in a sentence than show 30 badges.
Also use it as the default when a user is vague, busy, senior, or skeptical of
animation and vanity metrics.

**Skeleton:**
1. Greeting + name (H3/H4, optional small wave emoji — not H1, which is loud)
2. One-to-three-line identity statement in plain prose
3. Short bullet list (3–6): what I do / use / learning / ask me about
4. Inline link row (site, X, LinkedIn, email) as text or a few flat badges
5. Optional: GitHub stats tucked inside a collapsible `<details>`
6. Optional sign-off line or quote

**Signature techniques:** heading-as-intro (no banner) · emoji-led bullet facts ·
centered inline link row · stats hidden in `<details>` · `<hr>` as the only
divider · a single small accent at most · flat single-color badges.

**Traps:** scope creep (adding cards/streaks/30-badge walls defeats the point —
hide stats in `<details>` if you must); using H1/H2 for the greeting (too loud,
use H3/H4); rainbow badges (keep one muted palette or plain links); leaving
GitHub's default template comments in.

---

## 2. Badge / Icon Card

**Template:** `badge-card.md` · **Effort:** low · **Upkeep:** low · **2026
sample:** 7.9% standalone; badges appeared in 41.3% of profiles.

Identity carried by tidy rows of shields.io badge chips and brand-logo icons:
social links plus tech stack, scannable at a glance, no writing required, no
GitHub Action needed. Badges are a common building block even when the whole
profile is not a Badge / Icon Card archetype.

**Best for:** people who'd rather not write much but want to communicate stack and
contact clearly; students through sysadmins to researchers (ORCID/ResearchGate
badges).

**Skeleton:**
1. Short greeting / heading ("Hi there 👋" or "whoami")
2. Optional one or two lines of intro prose
3. Social & contact badge row (LinkedIn, X, email, dev.to, Stack Overflow…)
4. Tech-stack badge wall (one logo-badge per language/framework/tool)
5. Optional OS / editor badge row
6. GitHub stats card (often inside `<details>`)
7. Footer: visitor-counter badge

**Signature techniques:** shields.io static badges · clickable social row ·
grouped tech-stack wall · consistent `style` + `logoColor` on every badge ·
centered rows via `<p align="center">` · `cdn.simpleicons.org` glyphs ·
theme-aware icons via `<picture>` · skillicons.dev one-URL stack row.

**Traps:** badge overload (group by category, prune to what you use); mixing badge
styles (`flat-square` + `for-the-badge` + `flat` looks accidental — pick one);
wrong/missing `?logo=` Simple Icons slug (icon silently drops); low contrast (set
`logoColor=white` on dark badges); forgetting URL-encoding (`C%2B%2B` for C++);
dead counter services (prefer komarev).

---

## 3. Stats Dashboard

**Template:** `stats-dashboard.md` · **Effort:** medium · **Upkeep:** low ·
**2026 sample:** 14.0%

A centered hero plus live SVG cards: github-readme-stats, top languages, streak,
trophies. The page broadcasts activity. Powerful for someone genuinely active —
but lapsed activity turns the vanity cards ("No activity tracked") into a
liability, so warn the user.

**Best for:** active daily contributors who want activity to be the headline and
are comfortable wiring third-party image APIs (and ideally self-hosting them).
Use it only when GitHub activity helps the user's story; otherwise keep stats in
`<details>`.

**Skeleton:**
1. Centered header (hero or typing SVG with name + tagline)
2. Social / contact icon row + visitor counter
3. Short about blurb (1–3 lines or emoji bullets)
4. Tech stack (skillicons.dev / devicon / shields)
5. GitHub stats card + top-languages card (side by side)
6. Streak card
7. Optional: activity/coding-time graph, pinned-repo cards, trophies
8. Footer (star CTA, decorative wave)

**Signature techniques:** stats + top-langs cards · streak card · trophy row ·
typing-SVG header · pinned-repo cards · visitor counter — **all sharing one theme
and `hide_border=true`**.

**Traps:** camo image caching (GitHub proxies images; "realtime" looks stale —
cache-bust, don't promise second-by-second); third-party rate limits/502s (public
instances break under load — self-host load-bearing cards); theme drift (one
palette, same theme on every card); stat-card overload (collapse extras in
`<details>`; lead with a human blurb); vanity metrics that show neglect.

---

## 4. Descriptive Resume

**Template:** `descriptive-resume.md` · **Effort:** medium · **Upkeep:** low ·
**2026 sample:** 3.3%

A biography-first README that reads like a narrative resume: About, Skills,
Experience, Projects, Talks, Certifications. Substance and verified links matter
more than flair here. This is the style for someone whose *story* sells them.

**Best for:** job-seekers with real credentials (roles, talks, papers, certs);
ML/community/specialist devs; mentors and speakers; anyone whose accomplishments
matter more than decoration.
It is less common in the wild than its usefulness suggests, so choose it when the
user has proof links and recruiter readability is the goal.

**Skeleton:**
1. Greeting + one-line self-description
2. Social/contact badge row
3. About Me — prose paragraph or emoji bullets
4. Skills — categorized lists (Languages, Frameworks, DBs, Cloud, Tools)
5. Work Experience — table or bullets (role, company, period)
6. Projects / Portfolio — linked list with descriptions
7. Talks / Publications / Research
8. Certifications & Achievements
9. GitHub stats as *supporting* evidence near the end
10. Footer (contact)

**Signature techniques:** greeting + identity line · emoji-bulleted About ·
categorized skills · experience/proficiency tables · collapsible `<details>` for
the exhaustive parts · linked project list · talks/certs blocks · supporting
widgets last.

**Traps:** wall-of-text fatigue (break into headings/bullets); resume dump with no
hierarchy (fold exhaustive parts in `<details>`); stat-widget overload (it
undercuts the writing); **dead/unverifiable links are worse here than anywhere** —
the links are the credibility payload, so verify every cert/talk/project URL;
typos read as careless.

---

## 5. Code-as-Bio

**Template:** `code-as-bio.md` · **Effort:** low · **Upkeep:** low · **2026
sample:** 3.7%

The About section written as a syntactically plausible code snippet — a JS object,
Python class, or CSS rule whose keys are profile facts. A memorable coder flex,
low-maintenance once written. Write it in the language they most identify with.

**Best for:** developers who want their identity to signal "I am a coder" at a
glance, in their language of choice (JS/TS for web, Python for ML/backend, CSS for
front-end).

**Skeleton:**
1. Heading / greeting ("Hi, I'm {{NAME}}!", optional right-aligned hero GIF)
2. One-line role/tagline
3. Social badge row
4. "A little more about me…" header
5. **The signature block:** a fenced code block defining a self-object/class
6. Closing "say hi" line
7. `---`
8. Optional auto-updated stats footer

**Signature techniques:** self-object literal (JS/TS) · self-class with a
`say_hi()` method (Python) · CSS-rule bio (minimalist variant) · `npx` business
card · social badge row · optional auto-updated stats footer.

**Traps:** fake/non-runnable syntax (trailing commas, unquoted identifiers like
`code: [React, Node]` — the audience that likes this *notices*; keep it valid or
knowingly stylized); over-stuffed object (curate to what you'd discuss); going
stale (pair with an auto-updated footer or set a reminder); **code blocks aren't
clickable or alt-accessible** — put real contact links in a badge row *outside*
the block; copy-paste leftovers (scrub every key and URL to their handle).

---

## 6. Self-Updating / Automated

**Template:** `self-updating.md` + `self-updating-workflow.yml` · **Effort:** high
· **Upkeep:** automated · **2026 sample:** 12.7%

Content kept fresh by scheduled GitHub Actions that inject live data (blog posts,
releases, WakaTime, now-playing) between HTML comment markers, so the page reads
like a living dashboard. Only choose this if the person will actually keep their
feeds alive — and understands the 60-day cron caveat.

**Best for:** people who blog/ship/stream regularly and enjoy automation as a
demonstration of skill in itself.
Do not choose it just because the user wants the page to "look alive"; choose it
because they have real feeds and will maintain the workflow.

**Skeleton:**
1. Header / greeting (name, role, tagline)
2. Social/contact badge row
3. Short intro or quick-facts bullets
4. Auto-updated block #1: latest blog posts (between `<!-- BLOG-POST-LIST:START/END -->`)
5. Auto-updated block #2: recent releases / newsletter / TIL (often a multi-column table)
6. Auto-updated activity widget (WakaTime / Spotify / AniList)
7. GitHub stats / top-langs cards
8. Languages & Tools wall (often in `<details>`)
9. Footer: build-status badge + "How this works" link + visitor counter

**Signature techniques:** HTML comment marker injection points · scheduled cron
workflow · blog-post-workflow RSS injection · WakaTime weekly breakdown ·
multi-column table dashboard · build-status badge + "how this works" footer ·
now-playing/activity widgets.

**Traps:** mismatched/missing START/END markers (Action writes nothing); copying a
profile and leaving someone else's username/feed (you advertise their blog —
extremely common); **cron disabled after 60 days of repo inactivity** — do NOT use
keepalive hacks (ToS risk, repos have been disabled); stale feeds advertise
neglect ("No activity tracked"); unset required secrets (`WAKATIME_API_KEY`,
Spotify tokens) fail every run; widget overload + rate-limited endpoints.

---

## 7. Visual Showcase (GIF / Banner / Image)

**Template:** `visual-showcase.md` · **Effort:** medium · **Upkeep:** low ·
**2026 sample:** 15.2%

Visual identity carried by one or a few large assets: an animated hero GIF, a
hand-designed banner, or a skills graphic — almost always centered — wrapped
around the standard intro / stack / about / links skeleton. Friendly, eye-catching,
fast. Works minimal (one GIF + links) or maximal.

**Best for:** designers and visually-minded devs; students and early-career devs
who want a warm first impression and can supply or generate an asset.
The 2026 survey found images in 78.8% of profiles and missing or empty alt text in
47.3%, so this style must be stricter than the wild baseline about accessibility.

**Skeleton:**
1. Centered hero/banner GIF or image (with a one-line title above, optional)
2. Animated greeting heading (waving-hand inline beside "Hi there")
3. One-line intro / tagline
4. Tech stack as image badges (centered)
5. About-me emoji bullets
6. GitHub stats + streak cards
7. Social/contact badge row + visitor counter
8. Optional footer GIF / wave

**Signature techniques:** centered hero GIF/banner · inline animated emoji in the
heading · repo-hosted GIF asset · tech-stack badge wall · center-everything layout
· stats cards · `<samp>` typewriter text · capsule/wave footer.

**Traps:** hotlinked Giphy/imgur GIFs 404 later (host critical assets in-repo);
heavy/multiple GIFs slow load (compress, limit count); **motion + accessibility**
(meaningful alt text, no rapid flashing); no real content behind the animation (a
GIF + 3 badges reads as empty — pair with tagline/stack/links); inconsistent
alignment (pick centered and commit); wrong default branch in raw URLs (404s);
text trapped only inside an image (invisible to search/screen readers).

---

## 8. Persona / Themed (Anime, Retro, Fancy-Font)

**Template:** `persona-themed.md` · **Effort:** medium · **Upkeep:** low ·
**2026 sample:** 1.9%

A strong aesthetic persona — an anime character card, Web 1.0 / GeoCities
nostalgia (guestbook, hit counter, "best viewed in IE"), or Unicode fancy-font
typography. Maximum personality; accept the professionalism/accessibility
tradeoffs knowingly.

**Best for:** those who want a memorable identity statement over corporate polish:
anime/gamer/kawaii identities, web-nostalgia humorists, design-leaning devs who
want styled text with no HTML.
Do not classify ordinary emoji use as Persona / Themed. This style needs a clear
aesthetic premise.

**Skeleton (anime variant):** hero character art (centered or float-right) →
themed greeting → persona one-liner → About as a character stat-block → hobbies =
skills → skills/tools badges → niche-platform links (osu!, Last.fm, Discord) →
kawaii sign-off GIF. **Retro variant:** centered "Welcome" GIF → tagline →
homepage link → `<hr>` → guestbook (via Issues) → sign-off → hit counter → "made
with Notepad" badges. **Fancy-font variant:** Unicode bold-script headline → badge
row → fancy-font section headers over normal-text bodies.

**Signature techniques:** hero/character art · float-right GIF beside text ·
typing-SVG headline · Unicode fancy headings · persona one-liner · character
stat-block · niche/fandom badges · center-everything · guestbook via Issues · `<hr>`
dividers · retro footer badges.

**Traps:** image rot (self-host art; don't hotlink Tumblr/Pinterest); **copyright**
(most hero art is someone's uncredited fan/studio art — prefer own/commissioned/
creditable); persona swamps substance (keep a compact skills/projects block so
recruiters can parse it); **fancy Unicode breaks screen readers and search** (keep
critical info as plain text; reserve fancy for headline/headers); heavy GIFs hurt
load/accessibility; GitHub strips real `<marquee>`/`<blink>`/CSS (fake with
GIF/SVG); stale/unmoderated guestbook invites spam.

---

## 9. Interactive / Game Mode

**Template:** none (showpiece — build bespoke) · **Effort:** high · **Upkeep:**
automated · **2026 sample:** 1.7%

The README is a live, multiplayer experience: chess, Connect Four, a guestbook, an
`npx` card. Visitors make a move via a pre-filled GitHub Issue, and a backend
Action redraws state. A genuine conversation-starter that demonstrates automation
chops — reserve it for engineers who explicitly want a showpiece and will maintain
a small backend script.

**Best for:** engineers comfortable maintaining an Action/state machine who want a
memorable, community-building showpiece rather than a skills list.

**Skeleton:** game title / invitation → whose-turn line → live board (image grid in
a markdown table) → move controls (clickable issue links) → recent-moves log with
@mentions → leaderboard → `<details>` rules/history → short About/contact + "make
your own" link.

**Signature techniques:** move-as-Issue links · image-grid board in a table ·
whose-turn headline · recent-moves log · leaderboard as badges · `<details>` rules
· "make your own" template hook.

**Traps:** move links must open a fresh issue with an **unedited title** (tell
visitors to just hit Submit, or the parser breaks); state lives in the committed
README so concurrent moves race (gate with a single-runner Action or vote queue);
issues-based play needs login; camo caches board images (cache-bust with unique
URLs); emoji/image overload can make GitHub fail to render; the game can bury who
you are (keep a short About/contact block).
