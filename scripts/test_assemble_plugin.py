#!/usr/bin/env python3
"""Regression tests for deterministic Skill and Plugin assembly."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import stat
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ASSEMBLER = load_module("assemble_plugin", ROOT / "scripts" / "assemble_plugin.py")
VALIDATOR = load_module("validate_skills", ROOT / "scripts" / "validate_skills.py")

EXPECTED_SKILLS = set(ASSEMBLER.SOURCE_SKILLS)
REMOVED_ENTRIES = {
    "assumption-validation",
    "issue-shaping",
    "delivery-coordination",
    "simplification",
    "spec-review",
    "code-review",
    "pr-review",
    "review-setup",
}


def tree_state(path: Path) -> dict[str, tuple[bytes, int, int]]:
    return {
        str(item.relative_to(path)): (
            item.read_bytes(),
            item.stat().st_mtime_ns,
            stat.S_IMODE(item.stat().st_mode),
        )
        for item in sorted(path.rglob("*"))
        if item.is_file()
    }


def copy_repo(destination: Path) -> Path:
    root = destination / "repo"
    shutil.copytree(
        ROOT,
        root,
        ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", "*.pyc"),
    )
    return root


class AssemblyTests(unittest.TestCase):
    def test_source_and_package_skill_sets_are_exact(self) -> None:
        source = {
            path.parent.name for path in (ROOT / ".agents/skills").glob("*/SKILL.md")
        }
        package = {
            path.parent.name
            for path in (ROOT / "plugins/vision-harness/skills").glob("*/SKILL.md")
        }
        self.assertEqual(source, EXPECTED_SKILLS | {"method-evaluation"})
        self.assertEqual(package, EXPECTED_SKILLS)
        for name in REMOVED_ENTRIES | {"method-evaluation"}:
            self.assertFalse((ROOT / "plugins/vision-harness/skills" / name).exists())

    def test_shared_resources_follow_explicit_mapping(self) -> None:
        for resource, recipients in ASSEMBLER.SHARED_RESOURCE_MAP.items():
            expected = (ROOT / "skill-resources" / resource).read_bytes()
            for skill in EXPECTED_SKILLS:
                path = ROOT / ".agents/skills" / skill / "references" / resource
                self.assertEqual(path.exists(), skill in recipients, str(path))
                if path.exists():
                    self.assertEqual(path.read_bytes(), expected)

    def test_recursive_copy_preserves_binary_and_executable_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = copy_repo(Path(temp))
            source = root / ".agents/skills/breakdown"
            binary = source / "assets/fixture.bin"
            binary.parent.mkdir(parents=True, exist_ok=True)
            binary.write_bytes(b"\x00\xfffixture\x00")
            script = source / "scripts/fixture.sh"
            script.parent.mkdir(parents=True)
            script.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            script.chmod(0o755)
            cache = source / "__pycache__/fixture.pyc"
            cache.parent.mkdir()
            cache.write_bytes(b"cache")
            (source / "assets/.DS_Store").write_bytes(b"metadata")
            nested_cache = source / "references/__pycache__/cache.md"
            nested_cache.parent.mkdir()
            nested_cache.write_text("# cache\n", encoding="utf-8")
            skill_file = source / "SKILL.md"
            skill_file.write_text(
                skill_file.read_text(encoding="utf-8")
                + "\n[Binary fixture](assets/fixture.bin)\n",
                encoding="utf-8",
            )

            ASSEMBLER.assemble(root)
            packaged = root / "plugins/vision-harness/skills/breakdown"
            self.assertEqual((packaged / "assets/fixture.bin").read_bytes(), binary.read_bytes())
            self.assertEqual(
                stat.S_IMODE((packaged / "scripts/fixture.sh").stat().st_mode), 0o755
            )
            self.assertFalse((packaged / "__pycache__").exists())
            self.assertFalse((packaged / "assets/.DS_Store").exists())
            self.assertFalse((packaged / "references/__pycache__").exists())

    def test_assembly_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = copy_repo(Path(temp))
            ASSEMBLER.assemble(root)
            first = ASSEMBLER.tree_snapshot(root / "plugins/vision-harness")
            ASSEMBLER.assemble(root)
            self.assertEqual(first, ASSEMBLER.tree_snapshot(root / "plugins/vision-harness"))

    def test_check_detects_drift_without_writing(self) -> None:
        def add_old_reference(root: Path) -> None:
            path = root / "plugins/vision-harness/references/old.md"
            path.parent.mkdir(parents=True)
            path.write_text("old\n", encoding="utf-8")

        def change_mode(root: Path) -> None:
            path = root / "plugins/vision-harness/skills/breakdown/SKILL.md"
            path.chmod(path.stat().st_mode | stat.S_IXUSR)

        def change_shared_mode(root: Path) -> None:
            path = root / ".agents/skills/breakdown/references/common-rules.md"
            path.chmod(path.stat().st_mode | stat.S_IXUSR)

        def add_plugin_metadata(root: Path) -> None:
            path = root / "plugins/vision-harness/stale-metadata.txt"
            path.write_text("stale\n", encoding="utf-8")

        mutations = {
            "content": lambda root: (root / "plugins/vision-harness/skills/breakdown/SKILL.md").write_text("drift\n", encoding="utf-8"),
            "extra": lambda root: (root / "plugins/vision-harness/skills/breakdown/extra.txt").write_text("extra\n", encoding="utf-8"),
            "missing": lambda root: (root / "plugins/vision-harness/skills/breakdown/references/issue-shaping.md").unlink(),
            "mode": change_mode,
            "old-root-references": add_old_reference,
            "extra-plugin-metadata": add_plugin_metadata,
            "shared-source": lambda root: (root / ".agents/skills/breakdown/references/common-rules.md").write_text("stale\n", encoding="utf-8"),
            "shared-mode": change_shared_mode,
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                root = copy_repo(Path(temp))
                ASSEMBLER.assemble(root)
                mutate(root)
                before_source = tree_state(root / ".agents/skills")
                before_package = tree_state(root / "plugins/vision-harness")
                with self.assertRaises((SystemExit, ValueError)):
                    ASSEMBLER.check(root)
                self.assertEqual(before_source, tree_state(root / ".agents/skills"))
                self.assertEqual(before_package, tree_state(root / "plugins/vision-harness"))

    def test_source_validation_failure_preserves_existing_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = copy_repo(Path(temp))
            ASSEMBLER.assemble(root)
            package = root / "plugins/vision-harness"
            before = tree_state(package)
            skill = root / ".agents/skills/breakdown/SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8") + "\n[bad](../outside.md)\n", encoding="utf-8")
            with self.assertRaises((SystemExit, ValueError)):
                ASSEMBLER.assemble(root)
            self.assertEqual(before, tree_state(package))

    def test_generated_target_symlink_is_rejected_before_any_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = copy_repo(Path(temp))
            ASSEMBLER.assemble(root)
            package = root / "plugins/vision-harness"
            before = tree_state(package)
            outside = Path(temp) / "outside.txt"
            outside.write_bytes(b"keep me\n")
            target = root / ".agents/skills/breakdown/LICENSE"
            target.unlink()
            try:
                os.symlink(outside, target)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlinks unsupported: {exc}")
            with self.assertRaises((SystemExit, ValueError)):
                ASSEMBLER.assemble(root)
            self.assertEqual(outside.read_bytes(), b"keep me\n")
            self.assertEqual(before, tree_state(package))

    def test_invalid_manifest_preserves_generated_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = copy_repo(Path(temp))
            ASSEMBLER.assemble(root)
            skills = root / "plugins/vision-harness/skills"
            before = tree_state(skills)
            manifest = root / "plugins/vision-harness/plugin.json"
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["$schema"] = "https://agent-plugins.org/schemas/0.9.0/plugin.schema.json"
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises((SystemExit, ValueError)):
                ASSEMBLER.assemble(root)
            self.assertEqual(before, tree_state(skills))

    def test_invalid_portable_name_preserves_generated_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = copy_repo(Path(temp))
            ASSEMBLER.assemble(root)
            skills = root / "plugins/vision-harness/skills"
            before = tree_state(skills)
            manifest = root / "plugins/vision-harness/plugin.json"
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["name"] = "wrong-name"
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises((SystemExit, ValueError)):
                ASSEMBLER.assemble(root)
            self.assertEqual(before, tree_state(skills))

    def test_invalid_openai_extension_preserves_generated_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = copy_repo(Path(temp))
            ASSEMBLER.assemble(root)
            skills = root / "plugins/vision-harness/skills"
            before = tree_state(skills)
            manifest = root / "plugins/vision-harness/plugin.json"
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["extensions"]["com.openai"] = None
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises((SystemExit, ValueError)):
                ASSEMBLER.assemble(root)
            self.assertEqual(before, tree_state(skills))

    def test_portable_manifest_is_root_manifest_and_legacy_manifest_is_unused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = copy_repo(Path(temp))
            ASSEMBLER.assemble(root)
            package = root / "plugins/vision-harness"
            manifest_path = package / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["$schema"],
                "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            )
            self.assertEqual(manifest["name"], "vision-harness")
            self.assertEqual(
                manifest["version"],
                json.loads((ROOT / "plugins/vision-harness/plugin.json").read_text(encoding="utf-8"))["version"],
            )
            self.assertNotIn("skills", manifest)
            self.assertNotIn("interface", manifest)
            self.assertEqual(manifest["extensions"]["com.openai"]["interface"]["displayName"], "Vision Harness")
            self.assertFalse((package / ".codex-plugin").exists())

            legacy = package / ".codex-plugin/plugin.json"
            legacy.parent.mkdir()
            legacy.write_text("{\"name\": \"legacy\"}\n", encoding="utf-8")
            with self.assertRaises((SystemExit, ValueError)):
                ASSEMBLER.check(root)

    def test_marketplace_identity_uses_exact_mc_name_and_display_name(self) -> None:
        marketplace = json.loads(
            (ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
        )
        self.assertEqual(marketplace["name"], "MC")
        self.assertEqual(marketplace["interface"]["displayName"], "MC")

    def test_invalid_marketplace_identity_preserves_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = copy_repo(Path(temp))
            ASSEMBLER.assemble(root)
            package = root / "plugins/vision-harness"
            before = tree_state(package)
            marketplace_path = root / ".agents/plugins/marketplace.json"
            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            marketplace["name"] = "mc0571"
            marketplace["interface"]["displayName"] = "mc0571"
            marketplace_path.write_text(json.dumps(marketplace), encoding="utf-8")
            with self.assertRaises((SystemExit, ValueError)):
                ASSEMBLER.assemble(root)
            self.assertEqual(before, tree_state(package))

    def test_each_skill_exports_standalone_and_matches_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "exports"
            for skill in ASSEMBLER.SOURCE_SKILLS:
                exported = ASSEMBLER.export_skill(skill, output, ROOT)
                VALIDATOR.validate_skill(exported)
                self.assertEqual(
                    ASSEMBLER.tree_snapshot(exported),
                    ASSEMBLER.tree_snapshot(ROOT / "plugins/vision-harness/skills" / skill),
                )
                moved = Path(temp) / "moved" / skill
                moved.parent.mkdir(exist_ok=True)
                shutil.move(exported, moved)
                VALIDATOR.validate_skill(moved)

    def test_export_rejects_unknown_maintainer_nonempty_and_dangerous_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "exports"
            with self.assertRaises(ValueError):
                ASSEMBLER.export_skill("unknown", output, ROOT)
            with self.assertRaises(ValueError):
                ASSEMBLER.export_skill("method-evaluation", output, ROOT)
            output.mkdir()
            target = output / "breakdown"
            target.mkdir()
            (target / "keep.txt").write_text("keep\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                ASSEMBLER.export_skill("breakdown", output, ROOT)
            with self.assertRaises(ValueError):
                ASSEMBLER.export_skill("breakdown", ROOT / ".agents/skills", ROOT)

    def test_existing_eval_contracts_and_removed_entries_are_preserved(self) -> None:
        payload = json.loads((ROOT / "evals/work-entry-routing/cases.json").read_text(encoding="utf-8"))
        cases = payload.get("cases")
        self.assertIsInstance(cases, list)
        self.assertGreaterEqual(len(cases), 12)
        ids = []
        targets = set()
        for case in cases:
            case_id = case.get("id")
            self.assertIsInstance(case_id, str)
            self.assertTrue(case_id.strip())
            ids.append(case_id)
            case_targets = case.get("targets")
            self.assertIsInstance(case_targets, list)
            self.assertTrue(case_targets)
            self.assertTrue(all(isinstance(item, str) and item.strip() for item in case_targets))
            targets.update(case_targets)
            case_input = case.get("input")
            self.assertIsInstance(case_input, dict)
            self.assertIsInstance(case_input.get("user_request"), str)
            self.assertTrue(case_input["user_request"].strip())
            self.assertIsInstance(case_input.get("project_facts"), list)
            self.assertTrue(
                all(isinstance(item, str) and item.strip() for item in case_input["project_facts"])
            )
            oracle = case.get("oracle")
            self.assertIsInstance(oracle, dict)
            self.assertIsInstance(oracle.get("must"), list)
            self.assertTrue(oracle["must"])
            self.assertIsInstance(oracle.get("must_not"), list)
            self.assertTrue(oracle["must_not"])
            self.assertTrue(all(isinstance(item, str) and item.strip() for item in oracle["must"]))
            self.assertTrue(
                all(isinstance(item, str) and item.strip() for item in oracle["must_not"])
            )
            self.assertTrue(set(oracle["must"]).isdisjoint(oracle["must_not"]))
        self.assertEqual(len(ids), len(set(ids)))
        for expected in (
            "routing",
            "stop",
            "continue",
            "review",
            "critical-assumptions",
            "evidence-reuse",
            "agent-config",
            "execution",
        ):
            self.assertIn(expected, targets)

        pairs = payload.get("pairs")
        self.assertIsInstance(pairs, list)
        self.assertGreaterEqual(len(pairs), 4)
        dimensions = []
        case_ids = set(ids)
        for pair in pairs:
            dimension = pair.get("dimension")
            without_condition = pair.get("without_condition")
            with_condition = pair.get("with_condition")
            distinction = pair.get("distinction")
            self.assertIsInstance(dimension, str)
            self.assertTrue(dimension.strip())
            self.assertIn(without_condition, case_ids)
            self.assertIn(with_condition, case_ids)
            self.assertNotEqual(without_condition, with_condition)
            self.assertIsInstance(distinction, str)
            self.assertTrue(distinction.strip())
            dimensions.append(dimension)
        self.assertEqual(len(dimensions), len(set(dimensions)))
        for path in (ROOT / ".agents/skills").glob("*/SKILL.md"):
            text = path.read_text(encoding="utf-8")
            for name in REMOVED_ENTRIES:
                self.assertNotIn(f"../{name}/SKILL.md", text)


if __name__ == "__main__":
    unittest.main()
