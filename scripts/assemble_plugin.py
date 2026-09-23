#!/usr/bin/env python3
"""Synchronize shared Skill resources and export standalone Skills."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_skills as validator  # noqa: E402

SOURCE_SKILLS = validator.SOURCE_SKILLS
SHARED_RESOURCE_MAP = validator.SHARED_RESOURCE_MAP


def _validate_inputs(root: Path) -> None:
    for path in (root / "skills", root / "skill-resources"):
        validator.reject_symlinks(path)
    for name in SOURCE_SKILLS:
        skill_file = root / "skills" / name / "SKILL.md"
        if not skill_file.is_file():
            raise validator.ValidationError(f"missing Skill: {skill_file}")
    for filename in SHARED_RESOURCE_MAP:
        source = root / "skill-resources" / filename
        if not source.is_file():
            raise validator.ValidationError(f"missing shared resource: {source}")
    for path in (root / "LICENSE", root / "plugin.json", root / ".agents/plugins/marketplace.json"):
        if not path.is_file() or path.is_symlink():
            raise validator.ValidationError(f"missing or linked assembly input: {path}")
    validator.validate_manifests(root)


def _generated_drift(root: Path) -> list[str]:
    drift = []
    for name in SOURCE_SKILLS:
        skill = root / "skills" / name
        targets = {}
        for filename, recipients in SHARED_RESOURCE_MAP.items():
            target = skill / "references" / filename
            if name in recipients:
                targets[str(target.relative_to(skill))] = root / "skill-resources" / filename
            elif target.exists():
                drift.append(str(target))
        for relative, source in targets.items():
            target = skill / relative
            if not target.is_file() or target.read_bytes() != source.read_bytes() or (
                stat.S_IMODE(target.stat().st_mode) & 0o111
            ) != (stat.S_IMODE(source.stat().st_mode) & 0o111):
                drift.append(str(target))
    return sorted(drift)


def assemble(root: Path = ROOT) -> None:
    root = Path(root).resolve()
    _validate_inputs(root)
    for name in SOURCE_SKILLS:
        skill = root / "skills" / name
        references = skill / "references"
        references.mkdir(parents=True, exist_ok=True)
        for filename, recipients in SHARED_RESOURCE_MAP.items():
            target = references / filename
            if name in recipients:
                shutil.copy2(root / "skill-resources" / filename, target)
            elif target.exists():
                target.unlink()
    validator.validate_package(root)
    print(f"synchronized {len(SOURCE_SKILLS)} self-contained Skills: {root / 'skills'}")


def check(root: Path = ROOT) -> None:
    root = Path(root).resolve()
    _validate_inputs(root)
    drift = _generated_drift(root)
    if drift:
        raise validator.ValidationError("generated Skill drift: " + ", ".join(drift))
    validator.validate_package(root)
    print(f"read-only Skill and Plugin check passed: {len(SOURCE_SKILLS)} Skills")


def tree_snapshot(root: Path, *, exclude_development: bool = False) -> dict[str, tuple[str, int]]:
    return {
        str(path.relative_to(root)): (
            hashlib.sha256(path.read_bytes()).hexdigest(),
            stat.S_IMODE(path.stat().st_mode) & 0o111,
        )
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and not (exclude_development and validator.is_development_artifact(path.relative_to(root)))
    }


def export_skill(name: str, output: Path, root: Path = ROOT) -> Path:
    root = Path(root).resolve()
    if name not in SOURCE_SKILLS:
        raise ValueError(f"Skill is not exportable: {name}")
    output = Path(output).resolve(strict=False)
    if output == root or output.is_relative_to(root) or root.is_relative_to(output):
        raise ValueError(f"output may not point into or contain the repository: {output}")
    check(root)
    source = root / "skills" / name
    target = output / name
    if target.exists():
        if target.is_dir() and not any(target.iterdir()):
            target.rmdir()
        else:
            raise ValueError(f"export target already exists and is not empty: {target}")
    license_target = output / "LICENSE"
    if license_target.exists() and (
        not license_target.is_file() or license_target.read_bytes() != (root / "LICENSE").read_bytes()
    ):
        raise ValueError(f"export LICENSE differs from repository LICENSE: {license_target}")
    output.mkdir(parents=True, exist_ok=True)
    if not license_target.exists():
        shutil.copy2(root / "LICENSE", license_target)
    shutil.copytree(
        source,
        target,
        copy_function=shutil.copy2,
        ignore=lambda _directory, names: {
            item for item in names if validator.is_development_artifact(Path(item))
        },
    )
    validator.validate_skill(target)
    if tree_snapshot(target) != tree_snapshot(source, exclude_development=True):
        shutil.rmtree(target)
        raise validator.ValidationError(f"export differs from Skill source: {name}")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="read-only Skill and Plugin check")
    parser.add_argument("--export-skill", metavar="NAME", help="export one standalone Skill")
    parser.add_argument("--output", type=Path, help="parent directory for --export-skill")
    args = parser.parse_args()
    try:
        if args.check:
            if args.export_skill or args.output:
                parser.error("--check cannot be combined with export options")
            check(ROOT)
        elif args.export_skill:
            if args.output is None:
                parser.error("--export-skill requires --output")
            print(f"exported Skill: {export_skill(args.export_skill, args.output, ROOT)}")
        elif args.output:
            parser.error("--output requires --export-skill")
        else:
            assemble(ROOT)
    except (validator.ValidationError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
