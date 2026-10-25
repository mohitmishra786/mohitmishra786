"""Replace generated blocks between <!-- NAME:START --> / <!-- NAME:END --> markers.

Used by the profile workflows. Replacement is idempotent and fails loudly when
a marker pair is missing, duplicated, or out of order, so a broken README is
never silently committed.

CLI: python3 scripts/readme_blocks.py README.md NAME path/to/content.md
"""
from __future__ import annotations

import re
import sys

_MD_SPECIAL = re.compile(r"([\\`*_{}\[\]<>()#|!~])")


def escape_md(text: str) -> str:
    """Escape characters that would change the meaning of inline markdown/HTML."""
    text = " ".join(text.split())  # collapse newlines/tabs from PR titles
    return _MD_SPECIAL.sub(r"\\\1", text)


def truncate(text: str, limit: int = 90) -> str:
    """Truncate to `limit` characters on a word boundary, adding an ellipsis."""
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rstrip()
    space = cut.rfind(" ")
    if space > limit // 2:
        cut = cut[:space]
    return cut.rstrip(" ,;:-") + "…"


def replace_block(readme: str, name: str, content: str) -> str:
    return replace_between(readme, f"<!-- {name}:START -->", f"<!-- {name}:END -->", content)


def replace_between(readme: str, start: str, end: str, content: str) -> str:
    if readme.count(start) != 1 or readme.count(end) != 1:
        raise ValueError(
            f"expected exactly one {start} and one {end} in README "
            f"(found {readme.count(start)} and {readme.count(end)})"
        )
    i = readme.index(start) + len(start)
    j = readme.index(end)
    if j < i:
        raise ValueError(f"{end} appears before {start}")
    body = content.strip("\n")
    return readme[:i] + "\n" + body + "\n" + readme[j:]


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__, file=sys.stderr)
        return 2
    readme_path, name, content_path = argv[1:]
    with open(readme_path, encoding="utf-8") as f:
        readme = f.read()
    with open(content_path, encoding="utf-8") as f:
        content = f.read()
    updated = replace_block(readme, name, content)
    if updated != readme:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"{name}: updated")
    else:
        print(f"{name}: unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
