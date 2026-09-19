#!/usr/bin/env python3
"""Small deterministic checks for the distribution assembly."""

from __future__ import annotations

import importlib.util
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "assemble_plugin.py"
SPEC = importlib.util.spec_from_file_location("assemble_plugin", MODULE_PATH)
assert SPEC and SPEC.loader
ASSEMBLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ASSEMBLER)


def test_assembly_is_idempotent() -> None:
    ASSEMBLER.assemble()
    first = ASSEMBLER.snapshot()
    ASSEMBLER.assemble()
    second = ASSEMBLER.snapshot()
    assert first == second


def test_package_has_only_the_requested_skills() -> None:
    expected = {
        "using-vision-harness",
        "project-onboarding",
        "vision-management",
        "agent-instructions",
        "breakdown",
    }
    actual = {
        path.parent.name
        for path in (ASSEMBLER.PLUGIN / "skills").glob("*/SKILL.md")
    }
    assert actual == expected
    assert not (ASSEMBLER.PLUGIN / "skills" / "project-context").exists()


def test_breakdown_uses_package_local_references() -> None:
    text = (ASSEMBLER.PLUGIN / "skills" / "breakdown" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "../../references/shared-rules.md" in text
    assert "../../references/breakdown-behavior.md" in text
    assert "../../../" not in text


def test_check_detects_drift_without_rewriting_package() -> None:
    with tempfile.TemporaryDirectory(prefix="vision-harness-check-") as temp_dir:
        package = Path(temp_dir) / "vision-harness"
        shutil.copytree(ASSEMBLER.PLUGIN, package)
        drifted = package / "skills" / "breakdown" / "SKILL.md"
        before = drifted.read_bytes()
        drifted.write_bytes(before + b"\nintentional drift\n")
        changed = drifted.read_bytes()

        try:
            ASSEMBLER.check_idempotent(package)
        except SystemExit as exc:
            assert "assembly drift" in str(exc)
        else:
            raise AssertionError("drifted package unexpectedly passed --check")
        assert drifted.read_bytes() == changed


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
    test_assembly_is_idempotent()
    test_package_has_only_the_requested_skills()
    test_breakdown_uses_package_local_references()
    test_check_detects_drift_without_rewriting_package()
    test_selected_sections_rejects_missing_or_duplicate_sections()
    print("assembly checks passed")
