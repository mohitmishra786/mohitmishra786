"""Tests for the profile README scripts. Run: python3 -m unittest discover -s scripts/tests"""
from __future__ import annotations

import csv
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import contributions  # noqa: E402
import loc_report  # noqa: E402
from readme_blocks import escape_md, replace_block, replace_between, truncate  # noqa: E402

FIXTURES = os.path.join(HERE, "fixtures")
def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


BLOCKS = ("FEATURED-CONTRIBUTIONS", "RECENT-PRS", "OPEN-PRS", "RECENT-OWN-MERGES")

CONFIG = {
    "username": "me",
    "contributions": {
        "exclude_repos": ["someone/Hacktoberfest"],
        "featured_repos": ["sched-ext/scx"],
        "min_stars": 5,
        "max_items": 3,
        "recent_items": 2,
        "summaries": {"sched-ext/scx": "Scheduler fixes"},
    },
    "loc": {"contrib_exclude_extensions": [".md", ".json"]},
}


def skeleton_readme() -> str:
    parts = ["# Me", "<!-- BLOG-POST-LIST:START -->x<!-- BLOG-POST-LIST:END -->"]
    parts += [f"<!-- {b}:START -->\nold\n<!-- {b}:END -->" for b in BLOCKS]
    parts += ["<!-- LOC-STATS-START -->\nold\n<!-- LOC-STATS-END -->"]
    return "\n\n".join(parts) + "\n"


class ReadmeBlocksTest(unittest.TestCase):
    def test_replace_is_idempotent(self):
        once = replace_block(skeleton_readme(), "RECENT-PRS", "- a\n- b")
        twice = replace_block(once, "RECENT-PRS", "- a\n- b")
        self.assertEqual(once, twice)
        self.assertIn("<!-- RECENT-PRS:START -->\n- a\n- b\n<!-- RECENT-PRS:END -->", once)
        self.assertIn("<!-- BLOG-POST-LIST:START -->x<!-- BLOG-POST-LIST:END -->", once)

    def test_missing_marker_fails_loudly(self):
        with self.assertRaises(ValueError):
            replace_block("# no markers", "RECENT-PRS", "x")

    def test_duplicate_or_reversed_markers_fail(self):
        dup = skeleton_readme() + "<!-- OPEN-PRS:START --><!-- OPEN-PRS:END -->"
        with self.assertRaises(ValueError):
            replace_block(dup, "OPEN-PRS", "x")
        with self.assertRaises(ValueError):
            replace_between("<!-- B --> <!-- A -->", "<!-- A -->", "<!-- B -->", "x")

    def test_escape_md(self):
        self.assertEqual(escape_md("fix <meta> [GH #36] *now*|x"),
                         r"fix \<meta\> \[GH \#36\] \*now\*\|x")
        self.assertEqual(escape_md("multi\nline\ttitle"), "multi line title")

    def test_truncate(self):
        self.assertEqual(truncate("short", 10), "short")
        long = "word " * 40
        t = truncate(long, 30)
        self.assertLessEqual(len(t), 30)
        self.assertTrue(t.endswith("…"))


class ContributionsTest(unittest.TestCase):
    def setUp(self):
        self.raw = contributions.load_fixtures(FIXTURES)
        self.data = contributions.filter_public(self.raw, CONFIG)
        self.contrib = contributions.build_contributions(self.data, CONFIG, "me", "2026-10-25T00:00:00Z")

    def test_private_and_excluded_repos_never_appear(self):
        out = json.dumps(self.contrib) + json.dumps(
            contributions.render_blocks(self.data, self.contrib, CONFIG))
        self.assertNotIn("secret-org/private-repo", out)
        self.assertNotIn("Hacktoberfest", out)
        # unknown visibility (repo view failed) is treated as private
        self.assertNotIn("ghost/unknown", out)

    def test_grouping_counts_and_latest(self):
        scx = next(r for r in self.contrib["repos"] if r["repo"] == "sched-ext/scx")
        self.assertEqual(scx["merged_prs"], 2)
        self.assertEqual(scx["latest_pr"]["number"], 3934)
        self.assertEqual(scx["summary"], "Scheduler fixes")
        self.assertTrue(scx["featured"])

    def test_featured_rows_sorted_and_capped(self):
        rows = contributions.featured_rows(self.contrib, CONFIG)
        names = [r["repo"] for r in rows]
        self.assertEqual(names, ["sched-ext/scx", "edgcpp/compiler", "small/tutorial"][: len(names)])
        self.assertNotIn("tiny/repo", names)  # 1 star < min_stars and not featured
        self.assertLessEqual(len(rows), 3)
        table = contributions.render_featured(rows)
        self.assertIn("| [sched-ext/scx](https://github.com/sched-ext/scx) | Scheduler fixes | [2](", table)
        self.assertIn("| 2.2k |", table)

    def test_recent_lists_format(self):
        blocks = contributions.render_blocks(self.data, self.contrib, CONFIG)
        lines = blocks["RECENT-PRS"].splitlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(
            lines[0],
            "- [sched-ext/scx#3934](https://github.com/sched-ext/scx/pull/3934): "
            "scx\\_mlfq: Skip the RT drain, merged 2026-10-25")
        self.assertIn("opened 2026-10-24", blocks["OPEN-PRS"])
        self.assertNotIn("dependabot", blocks["RECENT-OWN-MERGES"])  # bots dropped
        self.assertIn("me/tool#7", blocks["RECENT-OWN-MERGES"])

    def test_empty_lists_render_placeholder(self):
        self.assertEqual(contributions.render_pr_list([], "merged", "closedAt", 5),
                         "_Nothing here right now._")

    def test_update_end_to_end_is_idempotent(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        readme = os.path.join(tmp, "README.md")
        out = os.path.join(tmp, "contributions.json")
        cfg_path = os.path.join(tmp, "cfg.json")
        with open(readme, "w") as f:
            f.write(skeleton_readme())
        with open(cfg_path, "w") as f:
            json.dump(CONFIG, f)  # JSON is valid YAML
        argv = ["update", "--config", cfg_path, "--readme", readme, "--out", out, "--fixtures", FIXTURES]
        contributions.main(argv)
        first = read(readme), read(out)
        contributions.main(argv)
        second = read(readme), read(out)
        self.assertEqual(first, second)  # no diff on re-run => no bot commit
        self.assertNotIn("\nold\n", first[0].split("<!-- LOC-STATS-START -->")[0])

    def test_update_fails_when_markers_missing(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        readme = os.path.join(tmp, "README.md")
        cfg_path = os.path.join(tmp, "cfg.json")
        with open(readme, "w") as f:
            f.write("# README without markers\n")
        with open(cfg_path, "w") as f:
            json.dump(CONFIG, f)
        with self.assertRaises(ValueError):
            contributions.main(["update", "--config", cfg_path, "--readme", readme,
                                "--out", os.path.join(tmp, "c.json"), "--fixtures", FIXTURES])

    def test_lines_per_language(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        cfg_path, out = os.path.join(tmp, "cfg.json"), os.path.join(tmp, "lines.csv")
        with open(cfg_path, "w") as f:
            json.dump(CONFIG, f)
        contributions.main(["lines", "--config", cfg_path, "--out", out, "--fixtures", FIXTURES])
        rows = list(csv.DictReader(read(out).splitlines()))
        self.assertNotIn("secret-org/private-repo", {r["Repository"] for r in rows})
        by = {(r["Repository"], r["PR"], r["Language"]): (int(r["Additions"]), int(r["Deletions"])) for r in rows}
        self.assertEqual(by[("sched-ext/scx", "3934", "C (BPF)")], (12, 3))
        self.assertEqual(by[("sched-ext/scx", "3934", "Rust")], (5, 1))
        self.assertNotIn(("sched-ext/scx", "3933", "Other"), by)  # README.md skipped

    def test_lines_skip_huge_generated_files(self):
        pr = {"repository": {"nameWithOwner": "o/r"}, "number": 1, "closedAt": "2021-11-07T00:00:00Z"}
        files = [{"filename": "report.html", "additions": 54122, "deletions": 0},
                 {"filename": "eda.py", "additions": 40, "deletions": 2}]
        rows = contributions.pr_line_rows(pr, files, set(), 5000)
        self.assertEqual(rows, [["o/r", 1, "2021-11-07", "Python", 40, 2]])

    def test_digest_window_grouping_and_privacy(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        cfg_path, out = os.path.join(tmp, "cfg.json"), os.path.join(tmp, "digest")
        with open(cfg_path, "w") as f:
            json.dump(CONFIG, f)
        # Run on Monday 2026-10-26 => covers 2026-10-19 .. 2026-10-25 (ISO week 43).
        contributions.main(["digest", "--config", cfg_path, "--out", out, "--fixtures", FIXTURES,
                            "--end", "2026-10-26"])
        text = read(os.path.join(out, "2026-W43.md"))
        self.assertIn("# Contribution digest: 2026-10-19 to 2026-10-25", text)
        self.assertIn("**3 PRs merged into other people's projects** across 2 repositories, "
                      "and **1 merged into my own repositories**.", text)
        self.assertIn("### [sched-ext/scx](https://github.com/sched-ext/scx) (2)", text)
        self.assertIn("- [#343](https://github.com/edgcpp/compiler/pull/343) move \\<meta\\>", text)
        self.assertNotIn("secret-org", text)      # private, and outside the window
        self.assertNotIn("ghost/unknown", text)   # unknown visibility
        self.assertNotIn("Bump deps", text)       # bot PR in my repo
        self.assertNotIn("small/tutorial", text)  # merged before the window
        self.assertIn("- [2026-W43](2026-W43.md)", read(os.path.join(out, "README.md")))

    def test_digest_empty_week(self):
        data = {"merged": [], "own": []}
        text = contributions.render_digest(data, "2020-01-01", "2020-01-07")
        self.assertEqual(text.count("_None this week._"), 2)
        many = [{"repository": {"nameWithOwner": "me/big"}, "number": i, "title": f"PR {i}",
                 "url": f"https://github.com/me/big/pull/{i}", "closedAt": "2020-01-02T00:00:00Z"}
                for i in range(11)]
        text = contributions.render_digest({"merged": many[:1], "own": many}, "2020-01-01", "2020-01-07")
        self.assertIn("**1 PR merged into other people's projects** across 1 repository,", text)
        self.assertIn("<details><summary>11 PRs</summary>", text)

    def test_language_of(self):
        self.assertEqual(contributions.language_of("scheds/rust/scx_mlfq/src/bpf/main.bpf.c"), "C (BPF)")
        self.assertEqual(contributions.language_of("src/lower.c"), "C")
        self.assertEqual(contributions.language_of("CMakeLists.txt"), "CMake")
        self.assertEqual(contributions.language_of("Makefile"), "Make")


class LocReportTest(unittest.TestCase):
    ROWS = [
        # Repository,Language,Files,Blank,Comment,Code
        ("me/a", "C", 10, 100, 50, 1000),
        ("me/a", "Python", 2, 20, 5, 300),
        ("me/b", "C", 4, 40, 7, 500),
        ("me/b", "Rust", 3, 30, 2, 250),
    ]

    def write_csv(self, tmp, rows):
        path = os.path.join(tmp, "detailed.csv")
        with open(path, "w") as f:
            f.write("Repository,Language,Files,Blank,Comment,Code\n")
            for r in rows:
                f.write(",".join(map(str, r)) + "\n")
        return path

    def test_language_aggregation_uses_code_column(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        langs = {l["language"]: l for l in
                 loc_report.aggregate_languages(loc_report.read_detailed(self.write_csv(tmp, self.ROWS)))}
        self.assertEqual(langs["C"]["code"], 1500)     # $6, not the comment column
        self.assertEqual(langs["C"]["comment"], 57)
        self.assertEqual(langs["C"]["blank"], 140)
        self.assertEqual(langs["C"]["files"], 14)
        self.assertEqual(langs["Python"]["code"], 300)

    def test_report_refuses_unlisted_repos_and_writes_outputs(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        detailed = self.write_csv(tmp, self.ROWS)
        allow = os.path.join(tmp, "allow.json")
        with open(allow, "w") as f:
            json.dump(["me/a"], f)  # me/b missing => refuse
        self.assertEqual(loc_report.main(["--detailed", detailed, "--allowlist", allow,
                                          "--out-dir", tmp]), 1)
        with open(allow, "w") as f:
            json.dump(["me/a", "me/b"], f)
        readme = os.path.join(tmp, "README.md")
        with open(readme, "w") as f:
            f.write(skeleton_readme())
        self.assertEqual(loc_report.main(["--detailed", detailed, "--allowlist", allow,
                                          "--out-dir", tmp, "--readme", readme]), 0)
        summary = read(os.path.join(tmp, "summary.md"))
        self.assertIn("| Language | Files | Code | Comment | Blank |", summary)
        self.assertIn("| C | 14 | 1,500 | 57 | 140 |", summary)
        stats = json.loads(read(os.path.join(tmp, "stats.json")))
        self.assertEqual(stats["total_code_lines"], 2050)
        self.assertIn("2.05k%20lines", read(readme))

    def test_human(self):
        self.assertEqual(loc_report.human(2_049_442), "2.05M")
        self.assertEqual(loc_report.human(1500), "1.5k")
        self.assertEqual(loc_report.human(999), "999")


if __name__ == "__main__":
    unittest.main()
