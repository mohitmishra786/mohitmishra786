# Pitfalls & pre-publish checklist

## What makes profile READMEs bad

Ordered roughly by how often it happens in the wild.

1. **AI-slop generic copy.** "Passionate developer who loves coding" wastes the
   most valuable lines on the page. The identity statement must be specific to what
   this person actually builds. This single thing separates a designed profile from
   a generated one.
2. **Copy-paste leftovers.** Another person's username, RSS feed, or stats URL left
   in a copied block — the most common genre mistake. Scrub every handle and URL.
3. **Leftover GitHub default-template scaffold.** The `<!-- special repository -->`
   comment and unfilled "🔭 I'm working on …" bullets signal an unfinished profile.
4. **Broken dark-mode images.** Black brand glyphs and dark-only banners disappear
   on GitHub's dark theme — use `<picture>` with a `prefers-color-scheme` variant.
   Always preview both themes.
5. **Wrong default branch in raw image URLs** (`main` vs `master`) silently 404s the
   hero image.
6. **Dead third-party services.** pufler.dev, glitch visitor-badge, hits.dwyl, old
   heroku endpoints leave broken-image icons. Prefer maintained services; self-host
   load-bearing assets.
7. **Widget overload / theme drift.** Stacking stats + streak + trophy + activity +
   snake + visitor + icon wall slows load, looks thrown-together, and buries the
   human. Pick a few; pass one consistent theme.
8. **No actual substance.** A hero GIF plus three badges and nothing else reads as
   empty. Pair any decoration with a real intro, links, and contact path.
9. **Accessibility misses.** Missing alt text; fancy-Unicode headings that screen
   readers spell out as gibberish; motion-heavy GIFs; intro text trapped only inside
   an image (invisible to search and assistive tech). In the 2026 survey, 47.3% of
   sampled profiles had at least one missing or empty image alt.
10. **Vanity metrics that backfire.** Streaks and "code time" cards showing "No
    activity tracked" advertise neglect.
11. **Mobile / centering fragility.** Wide HTML tables and fixed pixel widths overflow
    on phones; a stray unclosed tag silently left-aligns or hides content.
12. **No obvious next step.** A profile can look polished and still fail because
    visitors cannot find an email, LinkedIn, X/Twitter, website, or project link
    worth clicking. Add a direct path when the user provides one.
13. **Stale automation.** Cron workflows disabled after 60 days of inactivity (do
    NOT use keepalive hacks — ToS risk), or an empty blog/WakaTime/Spotify feed that
    loudly says "No activity."
14. **Dead or placeholder links.** 404 cert/talk/project links and empty `#` hrefs
    are worst on sparse profiles where every line carries weight.
15. **Fake code in Code-as-Bio.** Trailing commas and unquoted identifiers undercut
    the flex for the exact audience that notices.

## Pre-publish checklist

Run this before declaring the README done.

- [ ] Repo is named exactly `<username>/<username>`, public, with `README.md` on the
      default branch, and it actually renders on the profile page.
- [ ] The first screen states who you are and what you build in plain, specific prose
      — no "passionate developer" filler.
- [ ] The chosen archetype is obvious in the first 15 lines, and there is no more
      than one secondary accent.
- [ ] Every link is real and verified (GitHub, site, socials, `mailto:`); no `#`, no
      placeholders, no 404s.
- [ ] A clear contact or next-step path exists if the user provided one.
- [ ] Exactly one coherent style with at most one accent; not a pile of competing
      widgets.
- [ ] One consistent badge style and one shared card theme throughout; `hide_border`
      set on stat cards.
- [ ] Every `<img>` has meaningful alt text; intro/identity text exists as real text,
      not only inside an image.
- [ ] Dark and light themes both previewed; black brand glyphs use `<picture>` dark
      variants; nothing disappears or clashes.
- [ ] Raw image URLs use the correct default branch; critical assets are self-hosted
      in-repo, not hotlinked from volatile CDNs.
- [ ] Tech/skills list is pruned to what you actually use and grouped, not a 30-logo
      wall.
- [ ] No leftover GitHub default-template comments and no other person's
      username/feed/stats URLs anywhere.
- [ ] Any dynamic widgets currently render (not rate-limited/broken) and rely on
      maintained services; vanity metrics shown only if you'll keep feeding them.
- [ ] If automation is used: markers match the Action exactly, required secrets are
      set, the workflow runs, and there is no keepalive ToS hack.
- [ ] Mobile/narrow view checked — no overflowing wide tables or fixed-width overflow.
- [ ] A clear contact path exists, and the page tells the visitor where to go next.
