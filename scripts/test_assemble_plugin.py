#!/usr/bin/env python3
"""Small deterministic checks for the distribution assembly."""

from __future__ import annotations

import importlib.util
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


if __name__ == "__main__":
    test_assembly_is_idempotent()
    test_package_has_only_the_requested_skills()
    test_breakdown_uses_package_local_references()
    print("assembly checks passed")
