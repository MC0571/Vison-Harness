#!/usr/bin/env python3
"""Deterministic checks for distribution assembly and entry boundaries."""

from __future__ import annotations

import importlib.util
import json
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

EXPECTED_SKILLS = {
    "using-vision-harness",
    "project-onboarding",
    "vision-management",
    "breakdown",
    "spec-development",
    "technical-design",
    "tdd-development",
    "review",
    "change-verification",
    "release-delivery",
    "project-convergence",
    "agent-instructions",
}

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

EXPECTED_REFERENCES = {
    "shared-rules.md",
    "planning-methods.md",
    "agent-config-methods.md",
    "spec-design-methods.md",
    "implementation-methods.md",
    "review-methods.md",
    "evidence-methods.md",
    "convergence-methods.md",
    "vision-behavior.md",
    "project-context-behavior.md",
    "breakdown-behavior.md",
    "review-behavior.md",
}


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


def test_package_skill_boundary() -> None:
    actual = {
        path.parent.name
        for path in (ASSEMBLER.PLUGIN / "skills").glob("*/SKILL.md")
    }
    assert actual == EXPECTED_SKILLS
    for name in REMOVED_ENTRIES | {"method-evaluation", "project-context"}:
        assert not (ASSEMBLER.PLUGIN / "skills" / name).exists()


def test_runtime_references_are_focused_and_complete() -> None:
    actual = {
        path.name
        for path in (ASSEMBLER.PLUGIN / "references").glob("*.md")
    }
    assert actual == EXPECTED_REFERENCES
    assert "engineering-rules.md" not in actual

    expected_links = {
        "breakdown": ("planning-methods.md",),
        "spec-development": ("spec-design-methods.md",),
        "technical-design": (
            "spec-design-methods.md",
            "planning-methods.md",
            "implementation-methods.md",
        ),
        "tdd-development": ("implementation-methods.md", "evidence-methods.md"),
        "review": (
            "review-behavior.md",
            "review-methods.md",
            "evidence-methods.md",
        ),
        "change-verification": ("evidence-methods.md",),
        "project-convergence": ("convergence-methods.md",),
        "agent-instructions": ("agent-config-methods.md",),
    }
    for skill, references in expected_links.items():
        text = (
            ASSEMBLER.PLUGIN / "skills" / skill / "SKILL.md"
        ).read_text(encoding="utf-8")
        for reference in references:
            assert f"../../references/{reference}" in text
        assert "../../../" not in text


def test_removed_entries_do_not_leak_into_runtime_skill_links() -> None:
    linked = []
    for path in (ASSEMBLER.PLUGIN / "skills").glob("*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        for name in REMOVED_ENTRIES:
            if f"../{name}/SKILL.md" in text:
                linked.append((path.name, name))
    assert not linked


def test_review_is_one_entry_with_three_objects() -> None:
    text = (
        ASSEMBLER.PLUGIN / "skills" / "review" / "SKILL.md"
    ).read_text(encoding="utf-8")
    for object_name in ("Spec", "Code", "PR"):
        assert object_name in text
    assert "不自动修改被审查对象" in text


def test_work_entry_routing_eval_is_paired_and_unique() -> None:
    path = ROOT / "evals" / "work-entry-routing" / "cases.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload.get("cases")
    assert isinstance(cases, list)
    assert len(cases) >= 12

    ids = []
    targets = set()
    for case in cases:
        case_id = case.get("id")
        assert isinstance(case_id, str) and case_id.strip()
        ids.append(case_id)

        case_targets = case.get("targets")
        assert isinstance(case_targets, list) and case_targets
        assert all(isinstance(target, str) and target.strip() for target in case_targets)
        targets.update(case_targets)

        case_input = case.get("input")
        assert isinstance(case_input, dict)
        user_request = case_input.get("user_request")
        project_facts = case_input.get("project_facts")
        assert isinstance(user_request, str) and user_request.strip()
        assert isinstance(project_facts, list)
        assert all(isinstance(fact, str) and fact.strip() for fact in project_facts)

        oracle = case.get("oracle")
        assert isinstance(oracle, dict)
        must = oracle.get("must")
        must_not = oracle.get("must_not")
        assert isinstance(must, list) and must
        assert isinstance(must_not, list) and must_not
        assert all(isinstance(item, str) and item.strip() for item in must)
        assert all(isinstance(item, str) and item.strip() for item in must_not)
        assert set(must).isdisjoint(must_not)

    assert len(ids) == len(set(ids))
    case_ids = set(ids)

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
        assert expected in targets

    pairs = payload.get("pairs")
    assert isinstance(pairs, list) and len(pairs) >= 4
    dimensions = []
    for pair in pairs:
        dimension = pair.get("dimension")
        without_condition = pair.get("without_condition")
        with_condition = pair.get("with_condition")
        distinction = pair.get("distinction")
        assert isinstance(dimension, str) and dimension.strip()
        assert isinstance(without_condition, str) and without_condition in case_ids
        assert isinstance(with_condition, str) and with_condition in case_ids
        assert without_condition != with_condition
        assert isinstance(distinction, str) and distinction.strip()
        dimensions.append(dimension)
    assert len(dimensions) == len(set(dimensions))

def test_check_detects_drift_without_rewriting_package() -> None:
    with tempfile.TemporaryDirectory(prefix="vision-harness-check-") as temp_dir:
        package = Path(temp_dir) / "vision-harness"
        shutil.copytree(ASSEMBLER.PLUGIN, package)
        drifted = package / "skills" / "breakdown" / "SKILL.md"
        before = drifted.read_bytes()
        drifted.write_bytes(before + b"\nintentional drift\n")
        os.utime(
            drifted,
            ns=(946684800000000000, 946684800000000000),
        )
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

        source.write_text(
            "## Existing\none\n## Existing\ntwo\n",
            encoding="utf-8",
        )
        try:
            ASSEMBLER.selected_sections(source, ("## Existing",))
        except ValueError as exc:
            assert "duplicate source section" in str(exc)
        else:
            raise AssertionError("duplicate section unexpectedly passed")


if __name__ == "__main__":
    test_assembly_is_idempotent_without_rewriting_package()
    test_package_skill_boundary()
    test_runtime_references_are_focused_and_complete()
    test_removed_entries_do_not_leak_into_runtime_skill_links()
    test_review_is_one_entry_with_three_objects()
    test_work_entry_routing_eval_is_paired_and_unique()
    test_check_detects_drift_without_rewriting_package()
    test_selected_sections_rejects_missing_or_duplicate_sections()
    print("assembly checks passed")
