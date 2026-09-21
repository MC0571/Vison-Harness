#!/usr/bin/env python3
"""Regression tests for standalone Skill validation."""

from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_skills", ROOT / "scripts" / "validate_skills.py"
)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def make_skill(root: Path, body: str, extra: dict[str, bytes] | None = None) -> Path:
    skill = root / "sample-skill"
    skill.mkdir()
    skill.joinpath("SKILL.md").write_text(
        "---\nname: sample-skill\n"
        "description: Use when a sample workflow needs a deterministic result.\n"
        "license: MIT\n---\n\n# Sample\n\n" + body,
        encoding="utf-8",
    )
    skill.joinpath("LICENSE").write_text("MIT\n", encoding="utf-8")
    for relative, content in (extra or {}).items():
        path = skill / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    return skill


class SkillValidationTests(unittest.TestCase):
    def assert_invalid(self, skill: Path, needle: str) -> None:
        with self.assertRaises(VALIDATOR.ValidationError) as caught:
            VALIDATOR.validate_skill(skill)
        self.assertIn(needle, str(caught.exception))

    def test_valid_skill_and_reference_link(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill = make_skill(
                Path(temp),
                "Read [guide](references/guide.md#steps).\n",
                {"references/guide.md": b"# Guide\n\n## Steps\n\nDo it.\n"},
            )
            VALIDATOR.validate_skill(skill)

    def test_invalid_yaml_and_duplicate_keys_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill = make_skill(Path(temp), "Done.\n")
            skill.joinpath("SKILL.md").write_text(
                "---\nname: sample-skill\nname: duplicate\ndescription: broken\n---\nbody\n",
                encoding="utf-8",
            )
            self.assert_invalid(skill, "duplicate YAML key")
        with tempfile.TemporaryDirectory() as temp:
            skill = make_skill(Path(temp), "Done.\n")
            skill.joinpath("SKILL.md").write_text(
                "---\nname: [unterminated\ndescription: broken\n---\nbody\n",
                encoding="utf-8",
            )
            self.assert_invalid(skill, "invalid YAML frontmatter")

    def test_missing_encoded_escape_and_absolute_dependencies_are_rejected(self) -> None:
        cases = {
            "missing": "[missing](references/missing.md)",
            "escape": "[escape](references/%2e%2e/%2e%2e/METHOD.md)",
            "absolute": "[method](/tmp/provider/METHOD.md)",
            "file-url": "[method](file:///tmp/provider/METHOD.md)",
            "file-localhost-url": "[method](file://localhost/tmp/provider/METHOD.md)",
            "file-server-url": "[method](file://server/share/METHOD.md)",
            "ftp-url": "[method](ftp://server/share/METHOD.md)",
        }
        for label, body in cases.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                skill = make_skill(Path(temp), body + "\n")
                self.assert_invalid(skill, "local link")

    def test_http_and_https_links_are_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill = make_skill(
                Path(temp),
                "[http](http://example.com/guide) [https](https://example.com/guide)\n",
            )
            VALIDATOR.validate_skill(skill)

    def test_github_raw_runtime_dependency_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill = make_skill(
                Path(temp),
                "[method](https://raw.githubusercontent.com/example/repo/main/METHOD.md)\n",
            )
            self.assert_invalid(skill, "GitHub raw links")

    def test_external_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            outside = root / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            skill = make_skill(root, "[linked](references/linked.md)\n")
            refs = skill / "references"
            refs.mkdir()
            try:
                os.symlink(outside, refs / "linked.md")
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlinks unsupported: {exc}")
            self.assert_invalid(skill, "symbolic link")

    def test_missing_anchor_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill = make_skill(
                Path(temp),
                "[guide](references/guide.md#missing)\n",
                {"references/guide.md": b"# Guide\n"},
            )
            self.assert_invalid(skill, "missing anchor")

    def test_real_html_anchor_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill = make_skill(
                Path(temp),
                "[guide](references/guide.md#real)\n",
                {"references/guide.md": b'<a id="real"></a>\n'},
            )
            VALIDATOR.validate_skill(skill)

    def test_code_examples_do_not_count_as_html_anchors(self) -> None:
        cases = {
            "fence": '```html\n<a id="missing"></a>\n```\n',
            "inline": 'Use `<a id="missing"></a>` as an example.\n',
        }
        for label, example in cases.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                skill = make_skill(
                    Path(temp),
                    "[guide](references/guide.md#missing)\n",
                    {"references/guide.md": example.encode()},
                )
                self.assert_invalid(skill, "missing anchor")

    def test_fenced_examples_are_ignored_but_reference_links_are_checked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill = make_skill(
                Path(temp),
                "```markdown\n[fiction](../../METHOD.md)\n```\n\nUse [real][guide].\n\n[guide]: references/guide.md\n",
                {"references/guide.md": b"# Guide\n"},
            )
            VALIDATOR.validate_skill(skill)
            skill.joinpath("references/guide.md").unlink()
            self.assert_invalid(skill, "does not exist")

    def test_unlinked_runtime_resource_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill = make_skill(
                Path(temp), "Done.\n", {"references/hidden.md": b"# Hidden\n"}
            )
            self.assert_invalid(skill, "not directly linked")


if __name__ == "__main__":
    unittest.main()
