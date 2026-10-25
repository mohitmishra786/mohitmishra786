# Tools & services reference

The third-party services that power profile-README widgets. **Read the caveat
before using one** — several popular services are dead or rate-limited and leave
broken-image icons on the profile, which looks worse than not having the widget at
all. For anything load-bearing, prefer maintained services and self-host critical
assets.

| Service | URL | Use it for | Caveat |
|---|---|---|---|
| **Shields.io** | shields.io | Social-link chips, tech badges, dynamic badges via `/badge/-LABEL-HEX?style=...&logo=SLUG&logoColor=white` | Third-party CDN. `?logo=` needs the exact Simple Icons slug or the icon silently drops. Set `logoColor` explicitly. Pick ONE `style` (`flat-square` or `for-the-badge`) across the whole README. |
| **Simple Icons** | simpleicons.org | 2000+ monochrome brand SVGs; powers shields `?logo=` slugs; bare icons via `cdn.simpleicons.org/<slug>` (and `/<slug>/white` for dark mode) | Black glyphs vanish on GitHub dark theme unless you use the `/white` variant in a `<picture>`. Verify slugs against the catalog. |
| **github-readme-stats** | github.com/anuraghazra/github-readme-stats | Live stats card, top-languages card, pinned-repo cards; themeable, no workflow | Public Vercel instance rate-limits and 502s under load → broken images. Self-host for load-bearing use. Match username casing exactly. Use one built-in theme across cards; `transparent` is the safest light/dark default when the user has no strong theme preference. |
| **github-readme-streak-stats** | github.com/DenverCoder1/github-readme-streak-stats | Current/longest contribution-streak card | Vanity metric that shows neglect when streaks lapse; the heroku instance can go down. Theme-match it. |
| **github-profile-trophy** | github.com/ryo-ma/github-profile-trophy | Achievement trophy row from live stats | Decorative; easy to over-add. Use `no-frame=true` + a matching theme or it clashes. |
| **readme-typing-svg** | github.com/DenverCoder1/readme-typing-svg | Animated typing/erasing SVG headline, configured via URL params | 5.6% adoption in the 2026 survey: recognizable, not universal. Separate lines with semicolons, encode spaces, and set width to fit the longest line. Put the intro in `alt` because the animation is invisible to screen readers/search. Tune colors for both themes. |
| **blog-post-workflow** | github.com/gautamkrishnar/blog-post-workflow | GitHub Action: inject latest blog/RSS/dev.to/YouTube items between comment markers on a cron | Marker text must match exactly. Prefer `@v1` or a pinned SHA over `@master` when drafting workflows. Cron auto-disables after 60 days of repo inactivity (no keepalive hacks — ToS risk). A stale/empty feed advertises neglect. |
| **waka-readme** | github.com/athul/waka-readme | GitHub Action: weekly WakaTime coding-time bar chart into the README | Requires `WAKATIME_API_KEY` secret. Empty/low activity reads as "No activity." |
| **skillicons.dev** | skillicons.dev | One-URL icon row for a whole tech stack (`i=py,ts,go,docker,...`) | Third-party endpoint; limited to its icon set. Can't easily link individual icons. |
| **komarev profile views** | github.com/antonkomarev/github-profile-views-counter | Live profile-view counter badge | Prefer this over dead counters (pufler.dev, glitch visitor-badge, hits.dwyl) which leave broken images. A low count can read as neglect. |
| **capsule-render** | github.com/kyechan99/capsule-render | Generated waving/gradient header & footer banners | Third-party Vercel service; decorative only. Set a height + alt; don't use as sole content. |
| **Platane/snk** | github.com/Platane/snk | Action that animates the contribution graph being eaten by a snake (light/dark SVG) | 3.8% adoption in the 2026 survey; needs an Action that commits the SVG to an output branch. Pure decoration. |
| **GitHub raw / repo assets** | raw.githubusercontent.com | Self-host GIFs, banners, custom SVGs in `assets/`, referenced via raw URL | Match the actual default branch (`main` vs `master`) or the image 404s. The most durable hosting — prefer it over Giphy/imgur for anything important. |
| **awesome-github-profile-readme** | github.com/abhisheknaiidu/awesome-github-profile-readme | Curated gallery to browse for layout/widget ideas | Inspiration only — copying wholesale and leaving someone else's username/feed is the #1 genre mistake. |
| **GitHub profile README docs** | docs.github.com | Official setup and rendering rules for the special `<username>/<username>` repo | Use as the source of truth for mechanics: public same-name repo, root `README.md` with content, managed user account limitation, and old pre-July-2020 repo caveat. |

## Theme keywords (github-readme-stats family)

Common shared `theme=` values that read well in both light and dark: `tokyonight`,
`dark`, `radical`, `merko`, `gruvbox`, `transparent`, `github_dark`, `catppuccin_mocha`.
Whichever you pick, use the **same one on every card** and add `hide_border=true`.
When the profile otherwise has no strong visual theme, prefer `transparent` so the
cards blend into both GitHub light and dark themes.

## Choosing between badge styles

`flat-square` reads clean and compact (good for dense rows and minimalist/badge
profiles). `for-the-badge` is bold and uppercase (good for a small number of
prominent chips). Never mix them in one README.
