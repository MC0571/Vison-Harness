#!/usr/bin/env python3
"""Small deterministic checks for the distribution assembly."""

from __future__ import annotations

import importlib.util
import os
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "assemble_plugin.py"
SPEC = importlib.util.spec_from_file_location("assemble_plugin", MODULE_PATH)
assert SPEC and SPEC.loader
ASSEMBLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ASSEMBLER)


def package_state(package: Path) -> dict[str, tuple[bytes, int]]:
    return {
        str(path.relative_to(package)): (path.read_bytes(), path.stat().st_mtime_ns)
        for path in sorted(package.rglob("*"))
        if path.is_file()
    }


def assert_assembly_is_idempotent(package: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="vision-harness-assembly-test-") as temp_dir:
        working = Path(temp_dir) / "vision-harness"
        shutil.copytree(package, working)
        ASSEMBLER.assemble(working)
        first = ASSEMBLER.snapshot(working)
        ASSEMBLER.assemble(working)
        second = ASSEMBLER.snapshot(working)
        assert first == second


def test_assembly_is_idempotent_without_rewriting_package() -> None:
    before = package_state(ASSEMBLER.PLUGIN)
    assert_assembly_is_idempotent(ASSEMBLER.PLUGIN)
    assert package_state(ASSEMBLER.PLUGIN) == before


def test_package_has_only_the_requested_skills() -> None:
    expected = {
        "using-vision-harness", "project-onboarding", "vision-management",
        "agent-instructions", "breakdown", "assumption-validation",
        "issue-shaping", "delivery-coordination", "spec-development",
        "technical-design", "tdd-development", "simplification", "spec-review",
        "code-review", "pr-review", "change-verification", "release-delivery",
        "project-convergence", "review-setup",
    }
    actual = {
        path.parent.name
        for path in (ASSEMBLER.PLUGIN / "skills").glob("*/SKILL.md")
    }
    assert actual == expected
    assert not (ASSEMBLER.PLUGIN / "skills" / "project-context").exists()
    assert not (ASSEMBLER.PLUGIN / "skills" / "method-evaluation").exists()


def test_breakdown_uses_package_local_references() -> None:
    text = (ASSEMBLER.PLUGIN / "skills" / "breakdown" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "../../references/shared-rules.md" in text
    assert "../../references/breakdown-behavior.md" in text
    assert "../../../" not in text


def test_engineering_skills_use_selected_runtime_rules() -> None:
    expected = {
        "assumption-validation": "#4-",
        "delivery-coordination": "#4-",
        "spec-development": "#7-",
        "technical-design": "#7-",
        "spec-review": "#9-",
        "code-review": "#9-",
        "pr-review": "#9-",
        "review-setup": "#9-",
    }
    for name, anchor in expected.items():
        text = (ASSEMBLER.PLUGIN / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        assert "../../references/engineering-rules.md" + anchor in text
        assert "../../../" not in text
    reference = (ASSEMBLER.PLUGIN / "references" / "engineering-rules.md").read_text(encoding="utf-8")
    for heading in ("## 4. ", "## 7. ", "## 9. "):
        assert heading in reference


def test_check_detects_drift_without_rewriting_package() -> None:
    with tempfile.TemporaryDirectory(prefix="vision-harness-check-") as temp_dir:
        package = Path(temp_dir) / "vision-harness"
        shutil.copytree(ASSEMBLER.PLUGIN, package)
        drifted = package / "skills" / "breakdown" / "SKILL.md"
        before = drifted.read_bytes()
        drifted.write_bytes(before + b"\nintentional drift\n")
        os.utime(drifted, ns=(946684800000000000, 946684800000000000))
        changed = package_state(package)

        assert_assembly_is_idempotent(package)
        assert package_state(package) == changed

        try:
            ASSEMBLER.check_idempotent(package)
        except SystemExit as exc:
            assert "assembly drift" in str(exc)
        else:
            raise AssertionError("drifted package unexpectedly passed --check")
        assert package_state(package) == changed


def test_selected_sections_rejects_missing_or_duplicate_sections() -> None:
    with tempfile.TemporaryDirectory(prefix="vision-harness-sections-") as temp_dir:
        source = Path(temp_dir) / "source.md"
        source.write_text("## Existing\nbody\n", encoding="utf-8")
        try:
            ASSEMBLER.selected_sections(source, ("## Missing",))
        except ValueError as exc:
            assert "must match exactly" in str(exc)
        else:
            raise AssertionError("missing section unexpectedly passed")

        source.write_text("## Existing\none\n## Existing\ntwo\n", encoding="utf-8")
        try:
            ASSEMBLER.selected_sections(source, ("## Existing",))
        except ValueError as exc:
            assert "duplicate source section" in str(exc)
        else:
            raise AssertionError("duplicate section unexpectedly passed")


if __name__ == "__main__":
    test_assembly_is_idempotent_without_rewriting_package()
    test_package_has_only_the_requested_skills()
    test_breakdown_uses_package_local_references()
    test_engineering_skills_use_selected_runtime_rules()
    test_check_detects_drift_without_rewriting_package()
    test_selected_sections_rejects_missing_or_duplicate_sections()
    print("assembly checks passed")
