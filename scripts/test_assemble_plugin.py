#!/usr/bin/env python3
"""Regression checks for shared Skill and Plugin packaging."""

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


ASSEMBLER = load_module("assemble_plugin", ROOT / "scripts/assemble_plugin.py")
VALIDATOR = load_module("validate_skills", ROOT / "scripts/validate_skills.py")
EXPECTED_SKILLS = set(ASSEMBLER.SOURCE_SKILLS)
REMOVED_ENTRIES = {
    "assumption-validation", "issue-shaping", "delivery-coordination",
    "simplification", "spec-review", "code-review", "pr-review", "review-setup",
    "method-evaluation",
}


def copy_repo(destination: Path) -> Path:
    root = destination / "repo"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", "*.pyc"))
    return root


class AssemblyTests(unittest.TestCase):
    def test_one_skill_tree_serves_source_and_plugin(self) -> None:
        self.assertEqual(
            {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")},
            EXPECTED_SKILLS,
        )
        self.assertTrue((ROOT / "plugin.json").is_file())
        self.assertTrue((ROOT / "LICENSE").is_file())
        self.assertFalse((ROOT / "plugins/vision-harness/skills").exists())
        self.assertFalse((ROOT / ".agents/skills").exists())
        for name in EXPECTED_SKILLS:
            self.assertFalse((ROOT / "skills" / name / "LICENSE").exists())
            self.assertNotIn("license:", (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8"))
        for name in REMOVED_ENTRIES:
            self.assertFalse((ROOT / "skills" / name).exists())

    def test_shared_resources_follow_mapping(self) -> None:
        for resource, recipients in ASSEMBLER.SHARED_RESOURCE_MAP.items():
            expected = (ROOT / "skill-resources" / resource).read_bytes()
            for name in EXPECTED_SKILLS:
                target = ROOT / "skills" / name / "references" / resource
                self.assertEqual(target.exists(), name in recipients, str(target))
                if target.exists():
                    self.assertEqual(target.read_bytes(), expected)

    def test_check_detects_shared_drift_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = copy_repo(Path(temp))
            target = root / "skills/breakdown/references/common-rules.md"
            target.write_text("stale\n", encoding="utf-8")
            before = target.read_bytes()
            with self.assertRaises(ValueError):
                ASSEMBLER.check(root)
            self.assertEqual(target.read_bytes(), before)
            ASSEMBLER.assemble(root)
            ASSEMBLER.check(root)
            self.assertEqual(target.read_bytes(), (root / "skill-resources/common-rules.md").read_bytes())

    def test_invalid_manifest_prevents_generated_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = copy_repo(Path(temp))
            target = root / "skills/breakdown/references/common-rules.md"
            target.write_text("stale\n", encoding="utf-8")
            manifest = root / "plugin.json"
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["name"] = "wrong-name"
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ValueError):
                ASSEMBLER.assemble(root)
            self.assertEqual(target.read_text(encoding="utf-8"), "stale\n")

    def test_generated_target_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = copy_repo(Path(temp))
            outside = Path(temp) / "outside.txt"
            outside.write_bytes(b"keep me\n")
            target = root / "skills/breakdown/references/common-rules.md"
            target.unlink()
            try:
                os.symlink(outside, target)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlinks unsupported: {exc}")
            with self.assertRaises(ValueError):
                ASSEMBLER.assemble(root)
            self.assertEqual(outside.read_bytes(), b"keep me\n")

    def test_export_preserves_content_mode_and_standalone_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = copy_repo(Path(temp))
            source = root / "skills/breakdown"
            binary = source / "assets/fixture.bin"
            binary.parent.mkdir(parents=True, exist_ok=True)
            binary.write_bytes(b"\x00\xfffixture\x00")
            script = source / "scripts/fixture.sh"
            script.parent.mkdir(parents=True)
            script.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            script.chmod(0o755)
            (source / "__pycache__").mkdir()
            (source / "__pycache__/fixture.pyc").write_bytes(b"cache")
            skill_file = source / "SKILL.md"
            skill_file.write_text(skill_file.read_text(encoding="utf-8") + "\n[Binary fixture](assets/fixture.bin)\n", encoding="utf-8")
            exported = ASSEMBLER.export_skill("breakdown", Path(temp) / "exports", root)
            VALIDATOR.validate_skill(exported)
            self.assertEqual((exported.parent / "LICENSE").read_bytes(), (root / "LICENSE").read_bytes())
            self.assertFalse((exported / "LICENSE").exists())
            self.assertEqual((exported / "assets/fixture.bin").read_bytes(), binary.read_bytes())
            self.assertEqual(stat.S_IMODE((exported / "scripts/fixture.sh").stat().st_mode), 0o755)
            self.assertFalse((exported / "__pycache__").exists())
            self.assertEqual(
                ASSEMBLER.tree_snapshot(exported),
                ASSEMBLER.tree_snapshot(source, exclude_development=True),
            )

    def test_export_rejects_unknown_and_unsafe_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "exports"
            with self.assertRaises(ValueError):
                ASSEMBLER.export_skill("unknown", output, ROOT)
            output.mkdir()
            target = output / "breakdown"
            target.mkdir()
            (target / "keep.txt").write_text("keep\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                ASSEMBLER.export_skill("breakdown", output, ROOT)
            with self.assertRaises(ValueError):
                ASSEMBLER.export_skill("breakdown", ROOT / "skills", ROOT)
            conflict = Path(temp) / "conflict"
            conflict.mkdir()
            (conflict / "LICENSE").write_text("different\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                ASSEMBLER.export_skill("breakdown", conflict, ROOT)
            self.assertEqual((conflict / "LICENSE").read_text(encoding="utf-8"), "different\n")
            self.assertFalse((conflict / "breakdown").exists())

    def test_portable_manifest_and_marketplace_target_root(self) -> None:
        VALIDATOR.validate_manifests(ROOT)
        manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["$schema"], VALIDATOR.PORTABLE_SCHEMA)
        self.assertNotIn("skills", manifest)
        self.assertEqual(marketplace["name"], "MC-SKILL")
        self.assertEqual(marketplace["interface"]["displayName"], "MC-SKILL")
        self.assertEqual(marketplace["plugins"][0]["source"]["path"], "./")

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
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            text = path.read_text(encoding="utf-8")
            for name in REMOVED_ENTRIES:
                self.assertNotIn(f"../{name}/SKILL.md", text)


if __name__ == "__main__":
    unittest.main()
