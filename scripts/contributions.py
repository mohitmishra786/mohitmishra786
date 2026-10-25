"""Build contributions.json and the contribution/activity blocks of the profile README.

Subcommands
-----------
update   Query merged/open PRs (via the `gh` CLI), write contributions.json and
         replace the FEATURED-CONTRIBUTIONS, RECENT-PRS, OPEN-PRS and
         RECENT-OWN-MERGES blocks in the README.
lines    Sum lines added/removed by my merged PRs into other people's repos,
         per PR and file language, into a CSV (used by loc-stats.yml).

Only public repositories are ever queried (`--visibility public`) and any repo
reported as private is dropped again before anything is written, so private
repo names can't reach a committed file even if the token can see them.

`--fixtures DIR` reads merged.json/open.json/own.json/repos.json from DIR
instead of calling `gh` (used by the tests and for offline dry runs).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time
from collections import defaultdict
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from readme_blocks import escape_md, replace_block, truncate  # noqa: E402

SEARCH_PAUSE_SECONDS = 3  # search API allows 30 requests/minute
PR_FIELDS = "repository,title,url,number,closedAt,createdAt,author"


# --------------------------------------------------------------------------- fetch

def gh_json(args: list[str]):
    out = subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
    return json.loads(out) if out.strip() else []


def search_prs(*flags: str, query: str = "") -> list[dict]:
    args = ["search", "prs", *flags, "--visibility", "public", "--json", PR_FIELDS]
    if query:
        args += ["--", query]
    result = gh_json(args)
    time.sleep(SEARCH_PAUSE_SECONDS)
    return result


def fetch_all(user: str, own_limit: int) -> dict:
    not_mine = f"-user:{user}"
    merged = search_prs("--author", user, "--merged", "--sort", "updated", "--order", "desc",
                        "--limit", "300", query=not_mine)
    open_prs = search_prs("--author", user, "--state", "open", "--sort", "created",
                          "--order", "desc", "--limit", "50", query=not_mine)
    own = search_prs("--owner", user, "--merged", "--sort", "updated", "--order", "desc",
                     "--limit", str(max(own_limit * 4, 30)))
    names = sorted({p["repository"]["nameWithOwner"] for p in merged + open_prs})
    repos = []
    for name in names:
        try:
            repos.append(gh_json(["repo", "view", name, "--json",
                                  "nameWithOwner,stargazerCount,description,primaryLanguage,isPrivate,url"]))
        except subprocess.CalledProcessError as e:
            print(f"warning: could not view {name}: {e.stderr.strip()}", file=sys.stderr)
        time.sleep(0.5)
    return {"merged": merged, "open": open_prs, "own": own, "repos": repos}


def load_fixtures(path: str) -> dict:
    data = {}
    for key in ("merged", "open", "own", "repos"):
        with open(os.path.join(path, f"{key}.json"), encoding="utf-8") as f:
            data[key] = json.load(f)
    return data


# --------------------------------------------------------------------------- build

def _repo(pr: dict) -> str:
    return pr["repository"]["nameWithOwner"]


def _is_bot(pr: dict) -> bool:
    author = pr.get("author") or {}
    return author.get("type") == "Bot" or author.get("login", "").endswith("[bot]")


def filter_public(data: dict, cfg: dict) -> dict:
    """Drop excluded repos and anything that is (or can't be confirmed as) public."""
    excluded = {r.lower() for r in cfg["contributions"].get("exclude_repos", [])}
    public = {r["nameWithOwner"].lower(): r for r in data["repos"] if not r.get("isPrivate", True)}

    def keep(pr: dict) -> bool:
        name = _repo(pr).lower()
        return name in public and name not in excluded

    return {
        "merged": [p for p in data["merged"] if keep(p)],
        "open": [p for p in data["open"] if keep(p)],
        # Own repos: the search already ran with --visibility public.
        "own": [p for p in data["own"] if not _is_bot(p)],
        "repos": public,
    }


def build_contributions(data: dict, cfg: dict, user: str, now: str) -> dict:
    c = cfg["contributions"]
    groups: dict[str, list[dict]] = defaultdict(list)
    for pr in data["merged"]:
        groups[_repo(pr)].append(pr)

    featured = [f.lower() for f in c.get("featured_repos", [])]
    summaries = {k.lower(): v for k, v in (c.get("summaries") or {}).items()}
    repos = []
    for name, prs in groups.items():
        prs.sort(key=lambda p: p["closedAt"], reverse=True)
        info = data["repos"][name.lower()]
        latest = prs[0]
        repos.append({
            "repo": info["nameWithOwner"],
            "url": info.get("url") or f"https://github.com/{name}",
            "stars": info.get("stargazerCount", 0),
            "description": info.get("description") or "",
            "language": (info.get("primaryLanguage") or {}).get("name"),
            "merged_prs": len(prs),
            "merged_prs_url": f"https://github.com/{name}/pulls?q="
                              + quote(f"is:pr is:merged author:{user}"),
            "summary": summaries.get(name.lower()) or latest["title"],
            "featured": name.lower() in featured,
            "latest_pr": {
                "number": latest["number"],
                "title": latest["title"],
                "url": latest["url"],
                "merged_at": latest["closedAt"][:10],
            },
        })
    repos.sort(key=lambda r: (r["stars"], r["latest_pr"]["merged_at"]), reverse=True)
    return {
        "generated_at": now,
        "username": user,
        "total_merged_prs": len(data["merged"]),
        "total_repos": len(repos),
        "repos": repos,
    }


def featured_rows(contrib: dict, cfg: dict) -> list[dict]:
    c = cfg["contributions"]
    min_stars, max_items = c.get("min_stars", 0), c.get("max_items", 8)
    featured = [r for r in contrib["repos"] if r["featured"]]
    others = [r for r in contrib["repos"] if not r["featured"] and r["stars"] >= min_stars]
    rows = featured + others[: max(0, max_items - len(featured))]
    rows.sort(key=lambda r: (r["stars"], r["latest_pr"]["merged_at"]), reverse=True)
    return rows


# --------------------------------------------------------------------------- render

def _stars(n: int) -> str:
    return f"{n / 1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def render_featured(rows: list[dict]) -> str:
    if not rows:
        return "_No public contributions to show yet._"
    lines = ["| Repository | What I worked on | Merged PRs | Stars |",
             "|---|---|---:|---:|"]
    for r in rows:
        lines.append(
            f"| [{r['repo']}]({r['url']}) | {escape_md(truncate(r['summary'], 110))} "
            f"| [{r['merged_prs']}]({r['merged_prs_url']}) | {_stars(r['stars'])} |"
        )
    return "\n".join(lines)


def render_pr_list(prs: list[dict], verb: str, date_key: str, limit: int) -> str:
    prs = sorted(prs, key=lambda p: p[date_key], reverse=True)[:limit]
    if not prs:
        return "_Nothing here right now._"
    return "\n".join(
        f"- [{_repo(p)}#{p['number']}]({p['url']}): "
        f"{escape_md(truncate(p['title']))}, {verb} {p[date_key][:10]}"
        for p in prs
    )


def render_blocks(data: dict, contrib: dict, cfg: dict) -> dict[str, str]:
    n = cfg["contributions"].get("recent_items", 5)
    return {
        "FEATURED-CONTRIBUTIONS": render_featured(featured_rows(contrib, cfg)),
        "RECENT-PRS": render_pr_list(data["merged"], "merged", "closedAt", n),
        "OPEN-PRS": render_pr_list(data["open"], "opened", "createdAt", n),
        "RECENT-OWN-MERGES": render_pr_list(data["own"], "merged", "closedAt", n),
    }


# --------------------------------------------------------------------------- lines

EXT_LANG = {
    ".c": "C", ".h": "C/C++ Header", ".cc": "C++", ".cpp": "C++", ".cxx": "C++", ".hpp": "C++",
    ".hh": "C++", ".rs": "Rust", ".go": "Go", ".zig": "Zig", ".py": "Python", ".js": "JavaScript",
    ".jsx": "JavaScript", ".mjs": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript",
    ".mdx": "MDX", ".css": "CSS", ".scss": "SCSS", ".html": "HTML", ".sh": "Shell", ".bash": "Shell",
    ".dart": "Dart", ".java": "Java", ".kt": "Kotlin", ".rb": "Ruby", ".swift": "Swift",
    ".yml": "YAML", ".yaml": "YAML", ".toml": "TOML", ".s": "Assembly", ".S": "Assembly",
    ".bpf.c": "C (BPF)", ".cmake": "CMake", ".sql": "SQL", ".ps1": "PowerShell",
}


def language_of(path: str) -> str:
    base = os.path.basename(path)
    if base.endswith(".bpf.c"):
        return EXT_LANG[".bpf.c"]
    if base in ("Makefile", "makefile", "GNUmakefile"):
        return "Make"
    if base == "CMakeLists.txt":
        return "CMake"
    return EXT_LANG.get(os.path.splitext(base)[1], "Other")


def pr_line_rows(pr: dict, files: list[dict], skip_ext: set[str], max_file_additions: int = 0) -> list[list]:
    per_lang: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for f in files:
        path = f["filename"]
        if os.path.basename(path) != "CMakeLists.txt" and os.path.splitext(path)[1].lower() in skip_ext:
            continue
        if max_file_additions and f.get("additions", 0) > max_file_additions:
            continue  # a single huge added file is almost always generated (exports, bundles)
        acc = per_lang[language_of(path)]
        acc[0] += f.get("additions", 0)
        acc[1] += f.get("deletions", 0)
    return [[_repo(pr), pr["number"], pr["closedAt"][:10], lang, a, d]
            for lang, (a, d) in sorted(per_lang.items())]


def cmd_lines(args, cfg) -> int:
    user = cfg["username"]
    data = load_fixtures(args.fixtures) if args.fixtures else None
    if data is None:
        merged = search_prs("--author", user, "--merged", "--limit", "300", query=f"-user:{user}")
        names = sorted({_repo(p) for p in merged})
        repos = [gh_json(["repo", "view", n, "--json", "nameWithOwner,isPrivate"]) for n in names]
        data = {"merged": merged, "open": [], "own": [], "repos": repos}
    data = filter_public(data, cfg)
    skip = {e.lower() for e in cfg["loc"].get("contrib_exclude_extensions", [])}
    max_file = cfg["loc"].get("contrib_max_file_additions", 0)
    rows = []
    for pr in sorted(data["merged"], key=lambda p: (_repo(p), p["number"])):
        if args.fixtures:
            files = pr.get("files", [])
        else:
            owner_repo = _repo(pr)
            out = subprocess.run(
                ["gh", "api", "--paginate", "--jq", ".[] | {filename, additions, deletions}",
                 f"repos/{owner_repo}/pulls/{pr['number']}/files?per_page=100"],
                check=True, capture_output=True, text=True).stdout
            files = [json.loads(line) for line in out.splitlines() if line.strip()]
        rows.extend(pr_line_rows(pr, files, skip, max_file))
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("Repository,PR,MergedAt,Language,Additions,Deletions\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")
    print(f"wrote {len(rows)} rows for {len(data['merged'])} merged PRs to {args.out}")
    return 0


# --------------------------------------------------------------------------- main

def load_config(path: str) -> dict:
    import yaml  # PyYAML, installed by the workflow (scripts/requirements.txt)

    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def cmd_update(args, cfg) -> int:
    user = cfg["username"]
    n = cfg["contributions"].get("recent_items", 5)
    raw = load_fixtures(args.fixtures) if args.fixtures else fetch_all(user, n)
    data = filter_public(raw, cfg)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    contrib = build_contributions(data, cfg, user, now)

    with open(args.readme, encoding="utf-8") as f:
        readme = f.read()
    updated = readme
    for name, body in render_blocks(data, contrib, cfg).items():
        updated = replace_block(updated, name, body)

    # Only rewrite contributions.json when something other than the timestamp changed,
    # so a no-op run produces an empty diff and no commit.
    if os.path.exists(args.out):
        with open(args.out, encoding="utf-8") as f:
            old = json.load(f)
        if {**old, "generated_at": now} == contrib:
            contrib = old
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(contrib, f, indent=2, ensure_ascii=False)
        f.write("\n")
    if updated != readme:
        with open(args.readme, "w", encoding="utf-8") as f:
            f.write(updated)
    print(f"{contrib['total_merged_prs']} merged PRs across {contrib['total_repos']} public repos; "
          f"README {'updated' if updated != readme else 'unchanged'}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["update", "lines"])
    ap.add_argument("--config", default=".github/profile-config.yml")
    ap.add_argument("--readme", default="README.md")
    ap.add_argument("--out", help="output file (default: contributions.json / loc_results/contrib_lines.csv)")
    ap.add_argument("--fixtures", help="read gh results from this directory instead of calling gh")
    args = ap.parse_args(argv)
    cfg = load_config(args.config)
    if args.command == "update":
        args.out = args.out or "contributions.json"
        return cmd_update(args, cfg)
    args.out = args.out or "loc_results/contrib_lines.csv"
    return cmd_lines(args, cfg)


if __name__ == "__main__":
    sys.exit(main())
