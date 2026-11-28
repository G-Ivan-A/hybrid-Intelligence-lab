#!/usr/bin/env python3
"""Acceptance tests for tools/hub-sync.py (B-239, B-240, ADR-024 I-2, I-3, I-4, I-6, I-7).

A synthetic Hub git repository is built in a temporary directory; every
scenario runs the CLI as a subprocess and observes the spoke through
`git status --porcelain` and the profile bytes.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
CLI = TOOLS / "hub-sync.py"
WRAPPER = TOOLS / "hub-sync-wrapper.sh"
EXTRACTION = TOOLS / "spoke-extraction.py"
PROFILE_TEMPLATE = (ROOT / "templates" / "spoke" / ".hub-profile.json").read_text(encoding="utf-8")
GIT_ENV = {
    "GIT_AUTHOR_NAME": "hub-sync test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "hub-sync test", "GIT_COMMITTER_EMAIL": "test@example.invalid",
    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
}
ISSUE = "https://github.com/example/spoke/issues/1"
HUB_URL = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"
DAY1, DAY2 = "2026-11-20", "2026-12-01"


def git(repo, *args):
    env = dict(os.environ, **GIT_ENV)
    return subprocess.run(["git", "-C", str(repo), *args], check=True, env=env,
                          capture_output=True, text=True).stdout.strip()


def write(root, rel, text, executable=False):
    path = Path(root, rel)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    path.chmod(0o755 if executable else 0o644)


def spec(practices=False, delegated=("docs/local.md",)):
    units = {"genome": {"map": ["templates/spoke/="],
                        "exclude": ["templates/spoke/.hub-profile.json"],
                        "delegated": list(delegated)}}
    if practices:
        units["practice-a"] = {"map": ["templates/practice-a/=practices/a/"]}
        units["practice-b"] = {"map": ["templates/practice-b/=practices/b/"]}
    return json.dumps({"genome_version": "1.0", "placeholders": ["date", "hub_url", "project_name"],
                       "archetypes": {"B": {"profile_template": "templates/spoke/.hub-profile.json",
                                            "units": units}}}, indent=2) + "\n"


def make_hub(root):
    """C1: base genome; C2: two new practices; C3: base genome changes."""
    hub = Path(root, "hub")
    hub.mkdir()
    git(hub, "init", "-q", "-b", "main")
    write(hub, "templates/spoke/AGENTS.md",
          "# {{project_name}}\nupdated: {{date}}\nhub: {{hub_url}}\nrule: v1\n")
    write(hub, "templates/spoke/tools/check.sh", "#!/bin/sh\necho ok\n", executable=True)
    write(hub, "templates/spoke/docs/local.md", "delegated: v1\n")
    write(hub, "templates/spoke/.hub-profile.json", PROFILE_TEMPLATE)
    write(hub, "tools/hub-genome.json", spec())
    git(hub, "add", "-A")
    git(hub, "commit", "-q", "-m", "C1")
    c1 = git(hub, "rev-parse", "HEAD")
    git(hub, "tag", "v1")
    git(hub, "tag", "-a", "v1-annotated", "-m", "annotated")
    git(hub, "branch", "feature")
    git(hub, "branch", "dup")
    git(hub, "tag", "dup")
    write(hub, "templates/practice-a/a.md", "practice A {{date}}\n")
    write(hub, "templates/practice-b/b.md", "practice B\n")
    write(hub, "tools/hub-genome.json", spec(practices=True))
    git(hub, "add", "-A")
    git(hub, "commit", "-q", "-m", "C2")
    c2 = git(hub, "rev-parse", "HEAD")
    write(hub, "templates/spoke/AGENTS.md",
          "# {{project_name}}\nupdated: {{date}}\nhub: {{hub_url}}\nrule: v3\n")
    write(hub, "templates/spoke/docs/local.md", "delegated: v3\n")
    git(hub, "add", "-A")
    git(hub, "commit", "-q", "-m", "C3")
    c3 = git(hub, "rev-parse", "HEAD")
    return hub, c1, c2, c3


def snapshot(root):
    """Files of a tree (without .git) as {path: (bytes, executable)}."""
    out = {}
    for path in sorted(Path(root).rglob("*")):
        rel = path.relative_to(root).as_posix()
        if rel == ".git" or rel.startswith(".git/") or not path.is_file():
            continue
        out[rel] = (path.read_bytes(), bool(path.stat().st_mode & 0o100))
    return out


class HubSyncTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.hub, cls.c1, cls.c2, cls.c3 = make_hub(cls._tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.spoke = self.new_spoke("spoke")

    def new_spoke(self, name):
        spoke = self.tmp / name
        spoke.mkdir()
        git(spoke, "init", "-q")
        return spoke

    def run_cli(self, *args, spoke=None, day=DAY1, env=None, wrapper=False):
        spoke = spoke or self.spoke
        full_env = dict(os.environ, HUB_SYNC_TODAY=day)
        full_env.pop("HUB_SYNC_FAIL_AFTER_WRITES", None)
        full_env.update(env or {})
        if wrapper:
            full_env["HUB_SYNC_TOOL"] = str(CLI)
            command = ["bash", str(WRAPPER)]
        else:
            command = [sys.executable, str(CLI)]
        return subprocess.run(command + list(args), cwd=spoke, env=full_env,
                              capture_output=True, text=True)

    def sync(self, ref, *extra, spoke=None, day=DAY1, env=None, wrapper=False, expect=0):
        args = ["sync", "--hub", str(self.hub), "--target", ".", "--ref", ref,
                "--project-name", "demo", *extra]
        if not (Path(spoke or self.spoke) / ".hub-profile.json").exists():
            args += ["--archetype", "B"]
        run = self.run_cli(*args, spoke=spoke, day=day, env=env, wrapper=wrapper)
        self.assertEqual(run.returncode, expect, run.stdout + run.stderr)
        return run

    def commit(self, spoke=None):
        spoke = spoke or self.spoke
        git(spoke, "add", "-A")
        git(spoke, "commit", "-q", "--allow-empty", "-m", "sync")

    def porcelain(self, spoke=None):
        return git(spoke or self.spoke, "status", "--porcelain", "--untracked-files=all")

    def profile(self, spoke=None):
        return json.loads(((spoke or self.spoke) / ".hub-profile.json").read_text(encoding="utf-8"))

    def set_profile(self, profile, spoke=None):
        path = (spoke or self.spoke) / ".hub-profile.json"
        path.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def synced(self, ref, *extra, day=DAY1):
        self.sync(ref, *extra, day=day)
        self.commit()

    # ------------------------------------------------------------ I-2

    def test_success_writes_four_field_pin_of_applied_commit(self):
        run = self.sync(self.c1)
        pin = self.profile()["last_sync"]
        self.assertEqual(pin, {"hub_sha": self.c1, "date": DAY1, "scope": "genome",
                               "tool": "tools/hub-sync.py@1.1.0"})
        files = snapshot(self.spoke)
        self.assertEqual(files["AGENTS.md"][0].decode(),
                         "# demo\nupdated: 2026-11-20\n"
                         "hub: https://github.com/G-Ivan-A/hybrid-Intelligence-lab\nrule: v1\n")
        self.assertTrue(files["tools/check.sh"][1])
        self.assertEqual(self.profile()["archetype"], "B")
        self.assertEqual(json.loads(run.stdout)["status"], "synced")
        verify = self.run_cli("verify", "--hub", str(self.hub))
        self.assertEqual(verify.returncode, 0, verify.stderr)

    def test_failure_after_prepared_files_keeps_previous_pin_and_snapshot(self):
        self.synced(self.c1)
        before = snapshot(self.spoke)
        for writes in ("0", "1", "2"):
            run = self.sync(self.c3, day=DAY2, env={"HUB_SYNC_FAIL_AFTER_WRITES": writes},
                            expect=1)
            self.assertIn("rolled back", run.stderr)
            self.assertEqual(self.porcelain(), "")
            self.assertEqual(snapshot(self.spoke), before)

    def test_failure_on_first_sync_leaves_no_files(self):
        self.sync(self.c1, env={"HUB_SYNC_FAIL_AFTER_WRITES": "2"}, expect=1)
        self.assertEqual(snapshot(self.spoke), {})
        self.assertEqual(sorted(p.name for p in self.spoke.iterdir()), [".git"])

    def test_historical_record_migrates_without_invented_values(self):
        old = {"hub_commit": "54face1618f74154ae0f072bc3e5bfb3c4817754", "date": "2026-06-01"}
        profile = json.loads(PROFILE_TEMPLATE)
        profile["last_sync"] = old
        self.set_profile(profile)
        self.sync(self.c1)
        result = self.profile()
        self.assertEqual(result["sync_history"], [old])
        self.assertEqual(result["last_sync"]["hub_sha"], self.c1)

    def test_invalid_profile_is_refused_before_writes(self):
        profile = json.loads(PROFILE_TEMPLATE)
        profile["archetype"] = "Z"
        self.set_profile(profile)
        self.commit()
        run = self.sync(self.c1, expect=2)
        self.assertIn("profile_invalid", run.stderr)
        self.assertEqual(self.porcelain(), "")

    # ------------------------------------------------------------ I-3

    def test_sha_light_and_annotated_tag_give_same_pin(self):
        results = []
        for ref in (self.c1, "v1", "v1-annotated", "refs/tags/v1"):
            spoke = self.new_spoke(f"s-{len(results)}")
            run = self.sync(ref, spoke=spoke)
            results.append((json.loads(run.stdout)["hub_sha"], snapshot(spoke)))
            resolved = self.run_cli("resolve", "--hub", str(self.hub), "--ref", ref)
            self.assertEqual(resolved.stdout.strip(), self.c1)
        for result in results[1:]:
            self.assertEqual(result, results[0])
        self.assertEqual(results[0][0], self.c1)

    def test_floating_ambiguous_and_unresolvable_refs_are_refused(self):
        self.synced(self.c1)
        refs = ["main", "feature", "dup", "HEAD", "FETCH_HEAD", "@", "HEAD~1", "v1^{commit}",
                "main@{0}", "v1:AGENTS.md", self.c1[:12], "0" * 40, "missing-tag",
                "origin/main", "", "v1..dup", "refs/heads/main"]
        for ref in refs:
            with self.subTest(ref=ref):
                run = self.sync(ref, day=DAY2, expect=2)
                self.assertTrue(run.stderr.startswith("hub-sync: "), run.stderr)
                self.assertEqual(run.stdout, "")
                self.assertEqual(self.porcelain(), "")
        fresh = self.new_spoke("fresh")
        for ref in ("main", "missing-tag", "f" * 40):
            with self.subTest(fresh=ref):
                self.sync(ref, spoke=fresh, expect=2)
                self.assertEqual(snapshot(fresh), {})

    # ------------------------------------------------------------ I-4 and repeat sync

    def test_direct_call_and_wrapper_give_same_result_and_status(self):
        cases = [(self.c1, 0), ("main", 2)]
        for ref, code in cases:
            with self.subTest(ref=ref):
                direct, wrapped = self.new_spoke(f"d-{code}"), self.new_spoke(f"w-{code}")
                a = self.sync(ref, spoke=direct, expect=code)
                b = self.sync(ref, spoke=wrapped, wrapper=True, expect=code)
                self.assertEqual((a.returncode, a.stdout, a.stderr),
                                 (b.returncode, b.stdout, b.stderr))
                self.assertEqual(snapshot(direct), snapshot(wrapped))

    def test_wrapper_without_hub_location_fails_with_usage_status(self):
        env = dict(os.environ)
        env.pop("HUB_SYNC_HUB", None)
        env.pop("HUB_SYNC_TOOL", None)
        run = subprocess.run(["bash", str(WRAPPER), "sync"], env=env, capture_output=True,
                             text=True, cwd=self.spoke)
        self.assertEqual(run.returncode, 2)

    def test_manual_choice_of_one_of_two_new_practices(self):
        self.synced(self.c1)
        run = self.sync(self.c2, "--scope", "practice-a", day=DAY2)
        files = snapshot(self.spoke)
        self.assertIn("practices/a/a.md", files)
        self.assertEqual(files["practices/a/a.md"][0], b"practice A 2026-12-01\n")
        self.assertFalse(any(p.startswith("practices/b/") for p in files))
        self.assertEqual(self.profile()["last_sync"]["scope"], "genome+practice-a")
        self.assertEqual(json.loads(run.stdout)["selected"], "practice-a")

    def test_incompatible_base_file_outside_scope_keeps_pin_and_empty_diff(self):
        self.synced(self.c2, "--scope", "genome,practice-a")
        run = self.sync(self.c3, "--scope", "practice-a", day=DAY2, expect=1)
        problems = {p["path"]: p["action"] for p in json.loads(run.stdout)["problems"]}
        self.assertEqual(problems, {"AGENTS.md": "incompatible", "docs/local.md": "incompatible"})
        self.assertEqual(self.porcelain(), "")
        self.assertEqual(self.profile()["last_sync"]["hub_sha"], self.c2)
        self.sync(self.c3, "--scope", "genome", day=DAY2)
        self.assertEqual(self.profile()["last_sync"]["scope"], "genome+practice-a")
        self.assertIn(b"rule: v3", snapshot(self.spoke)["AGENTS.md"][0])

    def test_repeat_sync_on_another_date_changes_nothing(self):
        self.synced(self.c1)
        pin = (self.spoke / ".hub-profile.json").read_bytes()
        for ref in (self.c1, "v1-annotated"):
            run = self.sync(ref, "--scope", "genome", day=DAY2)
            self.assertEqual(self.porcelain(), "")
            self.assertEqual((self.spoke / ".hub-profile.json").read_bytes(), pin)
            report = json.loads(run.stdout)
            self.assertEqual((report["changes"], report["profile_changed"]), (0, False))
            self.assertEqual(report["date"], DAY1)

    def test_local_edit_in_managed_area_stops_the_sync(self):
        self.synced(self.c1)
        write(self.spoke, "AGENTS.md", "local edit\n")
        self.commit()
        run = self.sync(self.c3, day=DAY2, expect=1)
        problems = {p["path"]: p["action"] for p in json.loads(run.stdout)["problems"]}
        self.assertEqual(problems, {"AGENTS.md": "conflict"})
        self.assertEqual(self.porcelain(), "")

    def test_first_sync_requires_base_unit_and_known_units(self):
        self.sync(self.c2, "--scope", "practice-a", expect=2)
        self.sync(self.c2, "--scope", "genome,unknown", expect=2)
        self.assertEqual(snapshot(self.spoke), {})

    def test_plan_writes_nothing(self):
        run = self.run_cli("plan", "--hub", str(self.hub), "--ref", "v1", "--archetype", "B")
        self.assertEqual(run.returncode, 0, run.stderr)
        report = json.loads(run.stdout)
        self.assertEqual(report["status"], "planned")
        self.assertEqual(report["changes"], 3)
        self.assertEqual(snapshot(self.spoke), {})

    def test_verify_reports_drift(self):
        self.synced(self.c1)
        write(self.spoke, "docs/local.md", "edited\n")
        run = self.run_cli("verify", "--hub", str(self.hub))
        self.assertEqual(run.returncode, 1)
        self.assertEqual(json.loads(run.stdout)["problems"][0]["path"], "docs/local.md")

    # ------------------------------------------------------------ I-6

    def deviate(self, path, declared_by, issue=ISSUE):
        profile = self.profile()
        entry = {"path": path, "reason": "local decision", "declared_by": declared_by}
        if issue:
            entry["issue"] = issue
        profile["deviations"] = [entry]
        self.set_profile(profile)

    def test_project_deviation_keeps_delegated_local_edit(self):
        self.synced(self.c1)
        write(self.spoke, "docs/local.md", "project text\n")
        self.deviate("docs/local.md", "project")
        self.commit()
        self.sync(self.c3, day=DAY2)
        self.assertEqual((self.spoke / "docs/local.md").read_text(), "project text\n")
        self.assertIn(b"rule: v3", snapshot(self.spoke)["AGENTS.md"][0])
        self.assertEqual(self.run_cli("verify", "--hub", str(self.hub)).returncode, 0)

    def test_project_deviation_outside_delegation_does_not_exempt(self):
        self.synced(self.c1)
        write(self.spoke, "AGENTS.md", "project text\n")
        self.deviate("AGENTS.md", "project")
        self.commit()
        self.sync(self.c3, day=DAY2, expect=1)
        self.assertEqual(self.porcelain(), "")

    def test_owner_deviation_keeps_local_edit(self):
        self.synced(self.c1)
        write(self.spoke, "AGENTS.md", "owner decision\n")
        self.deviate("AGENTS.md", "owner")
        self.commit()
        self.sync(self.c3, day=DAY2)
        self.assertEqual((self.spoke / "AGENTS.md").read_text(), "owner decision\n")

    def test_deviation_without_issue_does_not_exempt(self):
        self.synced(self.c1)
        write(self.spoke, "docs/local.md", "project text\n")
        self.deviate("docs/local.md", "project", issue=None)
        self.commit()
        run = self.sync(self.c3, day=DAY2, expect=2)
        self.assertIn("deviation_invalid", run.stderr)
        self.assertEqual(self.porcelain(), "")


class RealGenomeTest(unittest.TestCase):
    """tools/hub-genome.json of this Hub against the working-tree templates."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.hub = Path(cls._tmp.name, "hub")
        shutil.copytree(ROOT / "templates", cls.hub / "templates")
        (cls.hub / "tools").mkdir()
        shutil.copy2(TOOLS / "hub-genome.json", cls.hub / "tools" / "hub-genome.json")
        cls.spec = json.loads((TOOLS / "hub-genome.json").read_text())
        for template in (ROOT / "templates").rglob("*.md"):
            for view, rel in re.findall(r"\{\{hub_url\}\}/(blob|tree)/\{\{hub_sha\}\}/([^\s)#`]+)",
                                        template.read_text(encoding="utf-8")):
                rel = rel.rstrip(".")
                original, copy = ROOT / rel, cls.hub / rel
                if copy.exists():
                    continue
                if view == "tree":
                    original, copy = original / "README.md", copy / "README.md"
                copy.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(original, copy)
        git(cls.hub, "init", "-q")
        git(cls.hub, "add", "-A")
        git(cls.hub, "commit", "-q", "-m", "hub")
        cls.sha = git(cls.hub, "rev-parse", "HEAD")
        git(cls.hub, "tag", "release")
        git(cls.hub, "commit", "-q", "--allow-empty", "-m", "next revision")
        cls.next_sha = git(cls.hub, "rev-parse", "HEAD")

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def run_tool(self, command, target, *extra, day=DAY1):
        env = dict(os.environ, HUB_SYNC_TODAY=day)
        return subprocess.run([sys.executable, str(command), *extra], cwd=target, env=env,
                              capture_output=True, text=True)

    def test_archetype_b_matches_e1_genome_and_replaces_it(self):
        e1 = Path(self._tmp.name, "e1")
        canonical = Path(self._tmp.name, "canonical")
        for path in (e1, canonical):
            path.mkdir()
        # E1 of ops/hub-project-extraction-contract.md
        manifest = Path(self._tmp.name, "genome.tsv")
        unit = self.spec["archetypes"]["B"]["units"]["genome"]
        maps = [part for mapping in unit["map"] for part in ("--map", mapping)]
        steps = [
            ["manifest", "--sha", self.sha, *maps, "-o", str(manifest)],
            ["materialize", "--manifest", str(manifest), "--target", str(e1),
             "--substitute", "project_name=demo",
             "--substitute", "hub_url=https://github.com/G-Ivan-A/hybrid-Intelligence-lab",
             "--substitute", f"date={DAY1}"],
        ]
        for step in steps:
            run = self.run_tool(EXTRACTION, e1, "--hub", str(self.hub), *step)
            self.assertEqual(run.returncode, 0, run.stderr)
        profile = json.loads((e1 / ".hub-profile.json").read_text(encoding="utf-8"))
        profile["last_sync"] = {"hub_sha": self.sha, "date": DAY1, "scope": "genome",
                                "tool": "tools/spoke-extraction.py@" + self.sha[:12]}
        (e1 / ".hub-profile.json").write_text(
            json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        run = self.run_tool(CLI, canonical, "sync", "--hub", str(self.hub), "--ref", self.sha,
                            "--archetype", "B", "--project-name", "demo")
        self.assertEqual(run.returncode, 0, run.stderr)
        e1_files, canonical_files = snapshot(e1), snapshot(canonical)
        e1_files.pop(".hub-profile.json")
        canonical_profile = canonical_files.pop(".hub-profile.json")
        self.assertEqual(canonical_files, e1_files)
        self.assertEqual(json.loads(canonical_profile[0])["last_sync"]["tool"],
                         "tools/hub-sync.py@1.1.0")
        check = subprocess.run(["bash", str(canonical / "tools" / "validate-agents-bootstrap.sh"),
                                str(canonical)], capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

        # first canonical sync of an E1 spoke: files stay, the pin moves to the tool
        run = self.run_tool(CLI, e1, "sync", "--hub", str(self.hub), "--ref", self.sha,
                            "--project-name", "demo")
        self.assertEqual(run.returncode, 0, run.stderr)
        report = json.loads(run.stdout)
        self.assertEqual((report["changes"], report["profile_changed"]), (0, True))

    def sync(self, target, ref, archetype=None, day=DAY1):
        extra = ["--archetype", archetype] if archetype else []
        return self.run_tool(CLI, target, "sync", "--hub", str(self.hub), "--ref", ref,
                             *extra, day=day)

    def verify(self, target):
        return self.run_tool(CLI, target, "verify", "--hub", str(self.hub))

    def assert_pinned_hub_links(self, target, sha):
        links = {}
        for path, (data, _) in snapshot(target).items():
            if not path.endswith(".md"):
                continue
            content = data.decode("utf-8")
            self.assertNotIn("{{hub_sha}}", content, path)
            urls = re.findall(re.escape(HUB_URL) + r"/(blob|tree)/([^/]+)/([^\s)#`]+)", content)
            if urls:
                links[path] = urls
            for view, ref, destination in urls:
                self.assertEqual(ref, sha, f"{path}: {destination}")
                destination = destination.rstrip(".")
                kind = git(self.hub, "cat-file", "-t", f"{sha}:{destination}")
                self.assertEqual(kind, view, f"{path}: {destination}")
        return links

    def test_no_floating_links_after_sync(self):
        target = Path(self._tmp.name, "pinned-links")
        target.mkdir()
        run = self.sync(target, "release", "B")
        self.assertEqual(run.returncode, 0, run.stderr)
        pin = json.loads((target / ".hub-profile.json").read_text())["last_sync"]
        self.assertEqual(pin["hub_sha"], self.sha)
        links = self.assert_pinned_hub_links(target, self.sha)
        self.assertEqual(len(links["AGENTS.md"]), 13)  # 12 blob links and one tree link
        self.assertEqual(len(links["README.md"]), 1)

        run = self.sync(target, self.next_sha, day=DAY2)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assert_pinned_hub_links(target, self.next_sha)
        check = self.verify(target)
        self.assertEqual(check.returncode, 0, check.stderr + check.stdout)

        for name in ("AGENTS.md", "README.md"):
            with self.subTest(name=name):
                document = target / name
                original = document.read_text()
                document.write_text(original.replace(f"/blob/{self.next_sha}/", "/blob/main/", 1))
                check = self.verify(target)
                self.assertEqual(check.returncode, 1, check.stderr)
                self.assertEqual(json.loads(check.stdout)["problems"][0]["path"], name)
                document.write_text(original)

    def test_archetype_b_installs_ops_and_preserves_project_starters(self):
        target = Path(self._tmp.name, "project-starters")
        target.mkdir()
        for path in ("README.md", ".github/workflows/ci.yml", "ops/backlog.md"):
            write(target, path, f"Project content at {path}\n")
        before = snapshot(target)
        run = self.sync(target, self.sha, "B")
        self.assertEqual(run.returncode, 0, run.stderr)
        run = self.sync(target, self.next_sha, day=DAY2)
        self.assertEqual(run.returncode, 0, run.stderr)
        files = snapshot(target)
        for path, state in before.items():
            self.assertEqual(files[path], state, path)
        for path in ("ops/backlog-instruction.md", "ops/artifact-map.md",
                     "ai-governance/ai-governance.md", "ai-rules/AI_SESSION_HANDOVER_PROMPT.md"):
            self.assertIn(path, files)
        self.assertEqual(list(target.glob("AI_*.md")), [])
        check = self.verify(target)
        self.assertEqual(check.returncode, 0, check.stderr + check.stdout)
        run = self.sync(target, self.next_sha, day=DAY1)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(snapshot(target), files)

    def test_archetype_d_genome_builds(self):
        target = Path(self._tmp.name, "htom")
        target.mkdir()
        run = self.run_tool(CLI, target, "sync", "--hub", str(self.hub), "--ref", self.sha,
                            "--archetype", "D", "--project-name", "demo")
        self.assertEqual(run.returncode, 0, run.stderr)
        files = snapshot(target)
        self.assertIn("AGENTS.md", files)
        self.assertNotIn("init.sh", files)
        self.assertEqual(json.loads(files[".hub-profile.json"][0])["archetype"], "D")
        self.assertFalse([p for p, (data, _) in files.items() if b"{{date}}" in data])
        self.assert_pinned_hub_links(target, self.sha)
        self.assertIn("ops/artifact-map.md", files)
        structure = target / "tools/validate-repository-structure.sh"
        command = ["bash", str(structure)]
        check = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        pointers = {
            "AI_GOVERNANCE.md": "ai-governance/ai-governance.md",
            "AI_QUICK_RULES.md": "ai-rules/ai-quick-rules.md",
            "AI_SESSION_HANDOVER_PROMPT.md": "ai-rules/AI_SESSION_HANDOVER_PROMPT.md",
        }
        self.assertEqual({p.name for p in target.glob("AI_*.md")}, set(pointers))
        for pointer, canonical in pointers.items():
            self.assertIn(b"Generated by the Hub genome", files[pointer][0])
            self.assertIn(canonical.encode(), files[pointer][0])
            self.assertGreater(len(files[canonical][0]), len(files[pointer][0]))

        legacy_copy = target / "governance/AI_GOVERNANCE.md"
        legacy_copy.parent.mkdir()
        shutil.copyfile(target / pointers[legacy_copy.name], legacy_copy)
        check = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(check.returncode, 1, check.stdout + check.stderr)
        self.assertIn("governance/AI_GOVERNANCE.md duplicates the contract", check.stderr)
        legacy_copy.unlink()

        shutil.copyfile(target / pointers["AI_GOVERNANCE.md"], target / "AI_GOVERNANCE.md")
        check = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(check.returncode, 1, check.stdout + check.stderr)
        self.assertIn("AI_GOVERNANCE.md must be a generated pointer", check.stderr)
        check = self.verify(target)
        self.assertEqual(check.returncode, 1, check.stderr)
        self.assertEqual(json.loads(check.stdout)["problems"][0]["path"], "AI_GOVERNANCE.md")

    def test_archetypes_without_genome_are_refused(self):
        target = Path(self._tmp.name, "c")
        target.mkdir()
        run = self.run_tool(CLI, target, "sync", "--hub", str(self.hub), "--ref", self.sha,
                            "--archetype", "C")
        self.assertEqual(run.returncode, 2)
        self.assertEqual(list(target.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
