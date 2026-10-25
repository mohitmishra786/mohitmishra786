#!/usr/bin/env python3
"""Generate consistent, theme-matched GitHub profile-README widget markdown.

Emits the fiddly bits (social badge row, stats cards, tech stack, typing SVG) with
one shared theme and badge style, so you don't hand-assemble error-prone URLs.
Output is plain markdown/HTML you paste into your README — review before shipping.

Examples
--------
  python build_widgets.py --username octocat --theme tokyonight \\
    --socials linkedin:octocat,x:octocat,email:o@cat.dev,website:https://octo.dev \\
    --stats --top-langs --stack py,ts,go,docker,react,postgres

  python build_widgets.py --username octocat --typing "Engineer;Open sourcerer;Coffee->code"

Notes
-----
- Stack uses skillicons.dev slugs (see https://skillicons.dev). One row, consistent.
- --stats/--top-langs/--streak share the same --theme and use hide_border=true.
- Streak/top-langs are activity vanity metrics: only show what you'll keep feeding.
- This tool only builds markup; it never verifies your links render. Preview both
  light and dark themes and check every URL before publishing.
"""
from __future__ import annotations

import argparse
from urllib.parse import quote

# label -> (shields color hex, simple-icons slug). Override colors as you like.
SOCIAL = {
    "linkedin": ("0077B5", "linkedin", "https://www.linkedin.com/in/{v}/"),
    "x": ("000000", "x", "https://x.com/{v}"),
    "twitter": ("1DA1F2", "twitter", "https://twitter.com/{v}"),
    "github": ("181717", "github", "https://github.com/{v}"),
    "email": ("D14836", "gmail", "mailto:{v}"),
    "website": ("222222", "googlechrome", "{v}"),
    "devto": ("0A0A0A", "devdotto", "https://dev.to/{v}"),
    "medium": ("12100E", "medium", "https://medium.com/@{v}"),
    "youtube": ("FF0000", "youtube", "{v}"),
    "discord": ("5865F2", "discord", "{v}"),
    "instagram": ("E4405F", "instagram", "https://instagram.com/{v}"),
    "stackoverflow": ("F58025", "stackoverflow", "{v}"),
}


def social_row(spec: str, style: str) -> str:
    lines = []
    for pair in [p for p in spec.split(",") if p.strip()]:
        key, _, val = pair.partition(":")
        key = key.strip().lower()
        if key not in SOCIAL:
            lines.append(f"<!-- unknown social '{key}' skipped -->")
            continue
        color, slug, href_tpl = SOCIAL[key]
        href = href_tpl.format(v=val.strip())
        nice = {"linkedin": "LinkedIn", "x": "X", "github": "GitHub", "devto": "DevTo",
                "youtube": "YouTube", "stackoverflow": "StackOverflow"}
        label = nice.get(key, key.capitalize())
        badge = (
            f"https://img.shields.io/badge/-{label}-{color}"
            f"?style={style}&logo={slug}&logoColor=white"
        )
        lines.append(f'  <a href="{href}"><img src="{badge}" alt="{label}"></a>')
    return '<p align="center">\n' + "\n".join(lines) + "\n</p>"


def stats_card(user: str, theme: str) -> str:
    return (
        f'  <img height="165" src="https://github-readme-stats.vercel.app/api'
        f'?username={user}&show_icons=true&hide_border=true&theme={theme}" '
        f'alt="{user}\'s GitHub stats" />'
    )


def top_langs(user: str, theme: str) -> str:
    return (
        f'  <img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/'
        f'?username={user}&layout=compact&hide_border=true&theme={theme}" '
        f'alt="Top languages" />'
    )


def streak(user: str, theme: str) -> str:
    return (
        f'  <img src="https://github-readme-streak-stats.herokuapp.com/'
        f'?user={user}&hide_border=true&theme={theme}" alt="Contribution streak" />'
    )


def stack_row(slugs: str) -> str:
    icons = ",".join(s.strip() for s in slugs.split(",") if s.strip())
    return (
        '<p align="center">\n'
        f'  <img src="https://skillicons.dev/icons?i={icons}" alt="tech stack" />\n'
        "</p>"
    )


def typing(lines: str) -> str:
    encoded = quote(lines, safe=";")
    first = lines.split(";")[0]
    return (
        '<p align="center">\n'
        f'  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=24'
        f'&center=true&vCenter=true&width=600&lines={encoded}" alt="{first}" />\n'
        "</p>"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--username", required=True)
    ap.add_argument("--theme", default="tokyonight", help="shared github-readme-stats theme")
    ap.add_argument("--style", default="flat-square", choices=["flat-square", "for-the-badge", "flat"])
    ap.add_argument("--socials", help="comma list like linkedin:user,email:a@b.com,website:https://...")
    ap.add_argument("--stack", help="comma skillicons slugs, e.g. py,ts,go,docker")
    ap.add_argument("--stats", action="store_true", help="github stats card")
    ap.add_argument("--top-langs", action="store_true", help="top-languages card")
    ap.add_argument("--streak", action="store_true", help="streak card (vanity metric)")
    ap.add_argument("--typing", help="semicolon-separated lines for an animated typing headline")
    args = ap.parse_args()

    out: list[str] = []
    if args.typing:
        out.append(typing(args.typing))
    if args.socials:
        out.append(social_row(args.socials, args.style))
    if args.stack:
        out.append(stack_row(args.stack))

    cards = []
    if args.stats:
        cards.append(stats_card(args.username, args.theme))
    if args.top_langs:
        cards.append(top_langs(args.username, args.theme))
    if cards:
        out.append('<p align="center">\n' + "\n".join(cards) + "\n</p>")
    if args.streak:
        out.append('<p align="center">\n' + streak(args.username, args.theme) + "\n</p>")

    if not out:
        ap.error("nothing to generate — pass at least one of --socials/--stack/--stats/--top-langs/--streak/--typing")
    print("\n\n".join(out))


if __name__ == "__main__":
    main()
