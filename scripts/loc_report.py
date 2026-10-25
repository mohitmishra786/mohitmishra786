"""Aggregate cloc results into the LOC summary files and the README LOC block.

Input  (loc_results/detailed_results.csv):
    Repository,Language,Files,Blank,Comment,Code   (one row per repo+language)
Also reads:
    --allowlist  JSON list of repos that may be published (public, owned, non-fork);
                 the script refuses to run if the CSV contains anything else.
    --status     CSV "Repository,Status,Reason" from the clone/cloc loop (optional).
    --contrib    CSV from `contributions.py lines` (optional).
Writes language_summary.csv, repo_summary.csv, summary.md, stats.json, badge.md
into --out-dir and (with --readme) replaces the LOC-STATS block.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from readme_blocks import replace_between  # noqa: E402

LOC_START = "<!-- LOC-STATS-START -->"
LOC_END = "<!-- LOC-STATS-END -->"


def read_detailed(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ("Files", "Blank", "Comment", "Code"):
            r[k] = int(r[k])
    return rows


def aggregate_languages(rows: list[dict]) -> list[dict]:
    """Per-language totals. Code comes from the Code column (not Comment)."""
    acc: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        c = acc[r["Language"]]
        c["files"] += r["Files"]
        c["blank"] += r["Blank"]
        c["comment"] += r["Comment"]
        c["code"] += r["Code"]
    out = [{"language": lang, **c} for lang, c in acc.items()]
    out.sort(key=lambda x: (-x["code"], x["language"]))
    return out


def aggregate_repos(rows: list[dict]) -> list[dict]:
    acc: Counter = Counter()
    for r in rows:
        acc[r["Repository"]] += r["Code"]
    return [{"repo": k, "code": v} for k, v in sorted(acc.items(), key=lambda kv: (-kv[1], kv[0]))]


def aggregate_contrib(path: str | None) -> dict | None:
    if not path or not os.path.exists(path):
        return None
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    langs: dict[str, Counter] = defaultdict(Counter)
    repos: dict[str, Counter] = defaultdict(Counter)
    prs = set()
    for r in rows:
        a, d = int(r["Additions"]), int(r["Deletions"])
        langs[r["Language"]].update(added=a, removed=d)
        repos[r["Repository"]].update(added=a, removed=d)
        prs.add((r["Repository"], r["PR"]))
    def order(m):
        return sorted(({"name": k, **v} for k, v in m.items()), key=lambda x: (-x["added"], x["name"]))
    return {
        "prs": len(prs),
        "added": sum(v["added"] for v in langs.values()),
        "removed": sum(v["removed"] for v in langs.values()),
        "languages": order(langs),
        "repos": order(repos),
    }


def fmt(n: int) -> str:
    return f"{n:,}"


def human(n: int) -> str:
    for div, suffix in ((1_000_000, "M"), (1_000, "k")):
        if n >= div:
            return f"{n / div:.2f}".rstrip("0").rstrip(".") + suffix
    return str(n)


def render_summary(langs, repos, contrib, status_counts, generated) -> str:
    total = Counter()
    for l in langs:
        total.update({k: l[k] for k in ("files", "blank", "comment", "code")})
    out = [
        f"_As of {generated}. Counts own public, non-fork, non-archived repositories "
        "(cloc, excluding data/docs formats and vendored/build directories)._",
        "",
        "| Metric | Count |",
        "|--------|------:|",
        f"| Repositories counted | {len(repos)} |",
        f"| Empty repositories skipped | {status_counts.get('empty', 0)} |",
        f"| Failed repositories | {status_counts.get('failed', 0)} |",
        f"| Files | {fmt(total['files'])} |",
        f"| Code lines | {fmt(total['code'])} |",
        f"| Comment lines | {fmt(total['comment'])} |",
        f"| Blank lines | {fmt(total['blank'])} |",
        "",
        "**Top 15 languages by code lines**",
        "",
        "| Language | Files | Code | Comment | Blank |",
        "|----------|------:|-----:|--------:|------:|",
    ]
    for l in langs[:15]:
        out.append(f"| {l['language']} | {fmt(l['files'])} | {fmt(l['code'])} "
                   f"| {fmt(l['comment'])} | {fmt(l['blank'])} |")
    out += ["", "**Top 20 repositories by code lines**", "",
            "| Repository | Code |", "|------------|-----:|"]
    for r in repos[:20]:
        out.append(f"| [{r['repo']}](https://github.com/{r['repo']}) | {fmt(r['code'])} |")
    if contrib:
        out += [
            "",
            f"**Lines changed in my {contrib['prs']} merged PRs to other people's public repos**: "
            f"+{fmt(contrib['added'])} / -{fmt(contrib['removed'])} "
            "_(from the PR file diffs; data, docs, lockfiles and notebooks excluded)_",
            "",
            "| Language | Added | Removed |", "|----------|------:|--------:|",
        ]
        for l in contrib["languages"][:10]:
            out.append(f"| {l['name']} | {fmt(l['added'])} | {fmt(l['removed'])} |")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--detailed", default="loc_results/detailed_results.csv")
    ap.add_argument("--allowlist", required=True, help="JSON list of publishable full repo names")
    ap.add_argument("--status", help="CSV Repository,Status,Reason")
    ap.add_argument("--contrib", help="CSV from contributions.py lines")
    ap.add_argument("--out-dir", default="loc_results")
    ap.add_argument("--readme", help="README to update between LOC-STATS markers")
    args = ap.parse_args(argv)

    rows = read_detailed(args.detailed)
    with open(args.allowlist, encoding="utf-8") as f:
        allowed = {n.lower() for n in json.load(f)}
    leaked = sorted({r["Repository"] for r in rows if r["Repository"].lower() not in allowed})
    if leaked:
        # Don't print the names: they might be private.
        print(f"refusing to publish: {len(leaked)} repositories in the CSV are not on the "
              "public allowlist", file=sys.stderr)
        return 1

    status_counts: Counter = Counter()
    if args.status and os.path.exists(args.status):
        with open(args.status, newline="", encoding="utf-8") as f:
            status_counts.update(r["Status"] for r in csv.DictReader(f))

    langs = aggregate_languages(rows)
    repos = aggregate_repos(rows)
    contrib = aggregate_contrib(args.contrib)
    now = dt.datetime.now(dt.timezone.utc)
    generated = now.strftime("%Y-%m-%d")
    total_code = sum(l["code"] for l in langs)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "language_summary.csv"), "w", encoding="utf-8") as f:
        f.write("Language,Files,Blank,Comment,Code\n")
        for l in langs:
            f.write(f"{l['language']},{l['files']},{l['blank']},{l['comment']},{l['code']}\n")
    with open(os.path.join(args.out_dir, "repo_summary.csv"), "w", encoding="utf-8") as f:
        for r in repos:
            f.write(f"{r['repo']},{r['code']}\n")
    summary = render_summary(langs, repos, contrib, status_counts, generated)
    with open(os.path.join(args.out_dir, "summary.md"), "w", encoding="utf-8") as f:
        f.write(summary)
    stats = {
        "generated_at": generated,
        "total_repositories": len(repos),
        "total_code_lines": total_code,
        "total_files": sum(l["files"] for l in langs),
        "languages": langs[:15],
        "top_repos": repos[:20],
        "contributions": contrib,
    }
    with open(os.path.join(args.out_dir, "stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
        f.write("\n")
    badge = (f"![Lines of code in my public repos: {fmt(total_code)}]"
             f"(https://img.shields.io/badge/code%20in%20my%20public%20repos-{human(total_code)}%20lines-blue)")
    if contrib:
        badge += (f" ![Lines added in merged PRs to other projects: {fmt(contrib['added'])}]"
                  f"(https://img.shields.io/badge/added%20via%20merged%20PRs%20to%20other%20projects-"
                  f"{human(contrib['added'])}%20lines-green)")
    with open(os.path.join(args.out_dir, "badge.md"), "w", encoding="utf-8") as f:
        f.write(badge + "\n")

    if args.readme:
        with open(args.readme, encoding="utf-8") as f:
            readme = f.read()
        block = f"\n{badge}\n\n<details>\n<summary>Lines-of-code details</summary>\n\n{summary}\n</details>\n"
        updated = replace_between(readme, LOC_START, LOC_END, block)
        with open(args.readme, "w", encoding="utf-8") as f:
            f.write(updated)
    print(f"total code lines: {total_code} across {len(repos)} repos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
