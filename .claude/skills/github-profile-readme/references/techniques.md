# Technique catalog

Copy-pasteable building blocks with placeholders (`{{LIKE_THIS}}`). Adoption notes
come from the 2026 survey of 520 verified public profile READMEs unless a block
says it was not separately measured. Use the numbers to tell common/safe from
niche/flashy. Replace **every** placeholder, and never leave another person's
handle, feed, branch, or theme in a pasted block. For the services these depend on
and their caveats, see `tools.md`.

General rule GitHub markdown enforces: **CSS is ignored.** Only `<p align="center">`,
`<div align="center">`, HTML tables, `width`/`height` attributes, and `<br>`
actually affect layout. `<marquee>`, `<blink>`, and `style="..."` are stripped.

## Contents
- [Centered wrapper](#centered-wrapper)
- [Social badge row](#social-badge-row)
- [Emoji identity bullets](#emoji-identity-bullets)
- [Hero image / GIF banner](#hero-image--gif-banner)
- [GitHub stats cards](#github-stats-cards)
- [Tech-stack badge wall](#tech-stack-badge-wall)
- [skillicons.dev row](#skilliconsdev-row)
- [Collapsible details](#collapsible-details)
- [Code-as-bio block](#code-as-bio-block)
- [Theme-aware image](#theme-aware-image)
- [Visitor counter](#visitor-counter)
- [Typing-SVG headline](#typing-svg-headline)
- [Streak / trophy cards](#streak--trophy-cards)
- [Auto-update markers + Action](#auto-update-markers--action)
- [Two-column table dashboard](#two-column-table-dashboard)
- [Move-as-Issue link](#move-as-issue-link)

---

## Centered wrapper
*42.9% adoption.* GitHub honors `<p align="center">` / `<div align="center">` for
alignment — reserve it for art, headers, and badge rows. Keep dense prose
left-aligned; centered paragraphs are hard to read.
```html
<p align="center">
  <!-- badges, image, or stats row -->
</p>
```

## Social badge row
Contact rows are common but inconsistent: 45.6% of sampled profiles linked
LinkedIn, 35.2% linked X/Twitter, and 21.5% exposed email. Wrap each badge in a
link. Pick one `style` and set `logoColor` so logos stay visible on dark chips.
```markdown
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/{{LINKEDIN}}/)
[![X](https://img.shields.io/badge/-X-000000?style=flat-square&logo=x&logoColor=white)](https://x.com/{{HANDLE}})
[![Email](https://img.shields.io/badge/-Email-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:{{EMAIL}})
```

## Emoji identity bullets
Common default-scaffold pattern, but not separately measured in the 2026 survey.
Use only when the bullets are specific. Keep 3–6 lines; delete any unfilled
placeholder.
```markdown
- 🔭 I'm currently working on **{{CURRENT_PROJECT}}**
- 🌱 I'm currently learning **{{LEARNING}}**
- 💬 Ask me about **{{TOPICS}}**
- 📥 Reach me at [{{EMAIL}}](mailto:{{EMAIL}})
```

## Hero image / GIF banner
*78.8% used at least one image; 24.0% used GIF/WebP media.* Host critical assets
in-repo (raw URL, correct branch) rather than hotlinking Giphy/imgur. Always set
`alt` and a width cap. The survey found missing or empty alt text in 47.3% of
sampled profiles, so this is where generated output can beat the baseline.
```html
<p align="center">
  <img src="https://github.com/{{USERNAME}}/{{USERNAME}}/raw/{{BRANCH}}/assets/{{FILE}}" alt="{{DESCRIPTIVE_ALT}}" width="100%" />
</p>
```

## GitHub stats cards
*37.7% used a stats-family widget; 21.5% used top-langs.* Pass the **same `theme`
plus `hide_border=true`** to every card for coherence. The public instance
rate-limits — self-host for anything load-bearing.
```html
<p align="center">
  <img height="165" src="https://github-readme-stats.vercel.app/api?username={{USERNAME}}&show_icons=true&hide_border=true&theme={{THEME}}" alt="{{NAME}}'s GitHub stats" />
  <img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username={{USERNAME}}&layout=compact&hide_border=true&theme={{THEME}}" alt="Top languages" />
</p>
```

## Tech-stack badge wall
Badges appeared in 41.3% of sampled profiles, but 23.5% had 10 or more badge
images. Group by category, prune to what you actually use, and avoid turning
every tool ever touched into a visible chip. `?logo=` must be the exact Simple
Icons slug or the icon silently drops. A blank line starts a new row.
```markdown
**Languages**

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)

**Tools**

![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
```

## skillicons.dev row
*2.5% adoption, but the lowest-effort whole-stack row:* one URL, consistent icons. A
good lightweight alternative to a 12-badge wall.
```html
<p align="center">
  <img src="https://skillicons.dev/icons?i=py,ts,go,docker,react,postgres" alt="tech stack" />
</p>
```

## Collapsible details
*9.0% adoption, underused.* The clean way to offer depth without burying the human
intro. Use for secondary stats, long work history, extra widgets, exhaustive tech
lists, and automation logs.
```html
<details>
  <summary>📈 GitHub Stats</summary>
  <br>
  <img src="https://github-readme-stats.vercel.app/api?username={{USERNAME}}&show_icons=true&hide_border=true&theme={{THEME}}" alt="stats" />
</details>
```

## Code-as-bio block
*3.7% Code-as-Bio archetype; 9.6% used at least one code fence.*
Keep it valid (quoted strings, no undeclared identifiers) or knowingly stylized —
the audience that likes this notices broken syntax. Links inside code blocks are
**not** clickable, so keep real contact links in a badge row outside.
```javascript
const {{USERNAME}} = {
  name: "{{NAME}}",
  role: "{{ROLE}}",
  code: ["TypeScript", "Python", "Go"],
  askMeAbout: ["web dev", "system design"],
  currentFocus: "{{CURRENT_FOCUS}}"
};
```

## Theme-aware image
*Only 3.3% adoption, but a quality marker.* Black brand glyphs (GitHub, X, Threads,
Apple) vanish on GitHub dark mode without this. Worth adding for any dark logo.
```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://cdn.simpleicons.org/{{SLUG}}/white">
  <img alt="{{BRAND}}" height="32" src="https://cdn.simpleicons.org/{{SLUG}}">
</picture>
```

## Visitor counter
*21.9% adoption.* A harmless social-proof flourish. Prefer maintained endpoints
(komarev) over dead ones (pufler.dev, glitch). A low count can read as neglect.
```markdown
![Profile views](https://komarev.com/ghpvc/?username={{USERNAME}}&label=Profile%20views&color=0e75b6&style=flat-square)
```

## Typing-SVG headline
*5.6% adoption despite being well-known — use sparingly.* Keep 3–5 short lines,
~1000ms pause. Carry the intro in `alt` (the animation is invisible to screen
readers); tune colors for both themes.
```html
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&center=true&vCenter=true&width=600&lines={{LINE_1}};{{LINE_2}};{{LINE_3}}" alt="{{LINE_1}}" />
</p>
```

## Streak / trophy cards
*11.0% streak, 7.9% trophy.* Vanity metrics that embarrass you when activity drops
("No activity tracked"). Only feature what you'll keep feeding. Theme-match to
your other cards.
```html
<img src="https://github-readme-streak-stats.herokuapp.com/?user={{USERNAME}}&hide_border=true&theme={{THEME}}" alt="contribution streak" />
<img src="https://github-profile-trophy.vercel.app/?username={{USERNAME}}&theme={{THEME}}&no-frame=true&row=1" alt="trophies" />
```

## Auto-update markers + Action
*12.7% Self-Updating archetype; 5.8% blog/RSS block.* START/END text must match
the Action's expected markers *exactly*. Cron workflows are disabled after 60 days
of repo inactivity — do **not** use keepalive hacks (ToS risk). Set required
secrets. See
`../assets/templates/self-updating-workflow.yml`.
```markdown
### 📝 Latest blog posts
<!-- BLOG-POST-LIST:START -->
<!-- BLOG-POST-LIST:END -->

<!-- .github/workflows/blog.yml: on schedule cron, uses gautamkrishnar/blog-post-workflow with feed_list: {{RSS_URL}} -->
```

## Two-column table dashboard
*15.6% adoption.* Turns a long scroll into a scannable dashboard and splits big
badge walls into labeled groups. Wide tables overflow on mobile — test the narrow
view.
```html
<table><tr>
<td valign="top" width="50%">

### {{COL_A_TITLE}}
{{COL_A_CONTENT}}

</td><td valign="top" width="50%">

### {{COL_B_TITLE}}
{{COL_B_CONTENT}}

</td></tr></table>
```

## Move-as-Issue link
*2.7% used issue links; 1.7% classified as Interactive / Game Mode.*
Zero-code visitor input: a pre-filled Issue whose title an Action parses. Tell
visitors to submit the title **unedited** or the parser breaks. Powers games and
guestbooks; the visitor must be logged in.
```markdown
[{{ACTION_LABEL}}](https://github.com/{{USERNAME}}/{{USERNAME}}/issues/new?title={{ENCODED_MOVE}}&body=Just+press+Submit+new+issue.)
```
