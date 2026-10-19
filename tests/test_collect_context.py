import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/change-handoff/scripts/collect_context.py"
SPEC = importlib.util.spec_from_file_location("collect_context", SCRIPT)
context = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(context)


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.autocrlf", "false")

    def git(self, *args):
        return subprocess.check_output(
            ["git", "-C", str(self.repo), *args], stderr=subprocess.PIPE
        ).decode("utf-8").strip()

    def write(self, name, text):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def commit(self, message):
        self.git("add", "--all")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")

    def test_multiple_commits_keep_explicit_base(self):
        self.write("a.txt", "a\n")
        base = self.commit("base")
        self.write("a.txt", "b\n")
        self.commit("middle")
        self.write("b.txt", "c\n")
        head = self.commit("final")
        result = context.collect(self.repo, base)
        self.assertEqual((result["base"], result["head"]), (base, head))
        self.assertEqual(result["committed_changes"], [
            {"status": "M", "path": "a.txt"},
            {"status": "A", "path": "b.txt"},
        ])
        self.assertFalse(result["has_uncommitted_changes"])

    def test_staged_unstaged_untracked_and_read_only(self):
        name = "space 中文.txt"
        self.write(name, "base\n")
        base = self.commit("base")
        self.write(name, "staged\n")
        self.git("add", "--", name)
        self.write(name, "unstaged\n")
        self.write("new file.txt", "do not read this content\n")
        index_before = (self.repo / ".git/index").read_bytes()
        status_before = self.git("status", "--porcelain=v1")
        result = context.collect(self.repo, base)
        self.assertEqual(result["staged_changes"], [{"status": "M", "path": name}])
        self.assertEqual(result["unstaged_changes"], [{"status": "M", "path": name}])
        self.assertEqual(result["untracked_paths"], ["new file.txt"])
        self.assertTrue(result["has_uncommitted_changes"])
        self.assertNotIn("do not read this content", json.dumps(result))
        self.assertEqual(index_before, (self.repo / ".git/index").read_bytes())
        self.assertEqual(status_before, self.git("status", "--porcelain=v1"))
        self.assertEqual(base, self.git("rev-parse", "HEAD"))

    def test_no_base_does_not_imply_empty_comparison(self):
        self.write("a", "base")
        self.commit("base")
        result = context.collect(self.repo)
        self.assertIsNone(result["base"])
        self.assertIsNone(result["committed_changes"])

    def test_unborn_head(self):
        self.write("staged.txt", "new")
        self.git("add", "--", "staged.txt")
        result = context.collect(self.repo)
        self.assertIsNone(result["head"])
        self.assertEqual(result["staged_changes"], [
            {"status": "A", "path": "staged.txt"}
        ])

    def test_missing_or_option_like_base_fails(self):
        self.write("a", "base")
        self.commit("base")
        for ref in ("unavailable-ref", "--all", ""):
            with self.subTest(ref=ref), self.assertRaises(context.ContextError):
                context.collect(self.repo, ref)

    def test_ignored_files_are_omitted(self):
        self.write(".gitignore", "private/\n")
        self.commit("ignore")
        self.write("private/secret.txt", "private")
        result = context.collect(self.repo)
        self.assertEqual(result["untracked_paths"], [])
        self.assertFalse(result["has_uncommitted_changes"])

    def test_deleted_paths_and_nested_invocation(self):
        self.write("nested/a.txt", "a")
        self.write("keep.txt", "b")
        base = self.commit("base")
        (self.repo / "nested/a.txt").unlink()
        result = context.collect(self.repo / "nested", base)
        self.assertEqual(result["unstaged_changes"], [
            {"status": "D", "path": "nested/a.txt"}
        ])

    def test_conflict_is_explicit(self):
        self.write("a", "base\n")
        self.commit("base")
        initial_branch = self.git("symbolic-ref", "--short", "HEAD")
        self.git("checkout", "-qb", "other")
        self.write("a", "other\n")
        self.commit("other")
        self.git("checkout", "-q", initial_branch)
        self.write("a", "current\n")
        self.commit("current")
        merge = subprocess.run(["git", "-C", str(self.repo), "merge", "other"],
                               capture_output=True)
        self.assertNotEqual(merge.returncode, 0)
        self.assertEqual(context.collect(self.repo)["unmerged_paths"], ["a"])

    def test_cli_emits_json_and_structured_error(self):
        self.write("a", "base")
        self.commit("base")
        success = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.repo)],
                                 capture_output=True, text=True)
        self.assertEqual(success.returncode, 0)
        self.assertEqual(json.loads(success.stdout)["schema_version"], 1)
        failure = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.repo),
                                  "--base", "missing"], capture_output=True, text=True)
        self.assertEqual(failure.returncode, 1)
        self.assertIn("error", json.loads(failure.stderr))
        self.assertEqual(failure.stdout, "")


if __name__ == "__main__":
    unittest.main()
