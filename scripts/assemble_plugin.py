#!/usr/bin/env python3
"""Assemble or export self-contained Vision Harness Skills."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_skills as validator  # noqa: E402


SOURCE_SKILLS = validator.SOURCE_SKILLS
SHARED_RESOURCE_MAP = validator.SHARED_RESOURCE_MAP
PLUGIN_RELATIVE = Path("plugins/vision-harness")
def _ignored(_directory: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if validator.is_development_artifact(Path(name))
    }


def _copytree(source: Path, destination: Path) -> None:
    shutil.copytree(
        source,
        destination,
        copy_function=shutil.copy2,
        ignore=_ignored,
        symlinks=False,
    )


def _validate_inputs(root: Path) -> None:
    source_root = root / ".agents" / "skills"
    plugin = root / PLUGIN_RELATIVE
    shared_root = root / "skill-resources"
    for path in (
        root / ".agents",
        source_root,
        root / "plugins",
        plugin,
        shared_root,
    ):
        validator.reject_symlinks(path)
    for name in SOURCE_SKILLS:
        skill_file = source_root / name / "SKILL.md"
        if not skill_file.is_file():
            raise validator.ValidationError(f"missing source Skill: {skill_file}")
    for filename in SHARED_RESOURCE_MAP:
        path = root / "skill-resources" / filename
        if not path.is_file():
            raise validator.ValidationError(f"missing shared resource source: {path}")
    for path in (
        root / "LICENSE",
        root / ".agents/plugins/marketplace.json",
        root / PLUGIN_RELATIVE / ".codex-plugin/plugin.json",
        root / PLUGIN_RELATIVE / "README.md",
    ):
        if not path.is_file():
            raise validator.ValidationError(f"missing assembly input: {path}")
        if path.is_symlink():
            raise validator.ValidationError(f"assembly input may not be a symbolic link: {path}")
    validator.validate_manifests(root)


def _sync_source_generated(root: Path) -> None:
    license_source = root / "LICENSE"
    shared_root = root / "skill-resources"
    for name in SOURCE_SKILLS:
        skill = root / ".agents" / "skills" / name
        references = skill / "references"
        references.mkdir(parents=True, exist_ok=True)
        for filename, recipients in SHARED_RESOURCE_MAP.items():
            target = references / filename
            if name in recipients:
                shutil.copy2(shared_root / filename, target)
            elif target.exists():
                target.unlink()
        shutil.copy2(license_source, skill / "LICENSE")


def _source_generated_drift(root: Path) -> list[str]:
    drift: list[str] = []
    license_source = root / "LICENSE"
    license_bytes = license_source.read_bytes()
    license_mode = stat.S_IMODE(license_source.stat().st_mode) & 0o111
    shared_names = set(SHARED_RESOURCE_MAP)
    for name in SOURCE_SKILLS:
        skill = root / ".agents" / "skills" / name
        license_path = skill / "LICENSE"
        if (
            not license_path.is_file()
            or license_path.read_bytes() != license_bytes
            or stat.S_IMODE(license_path.stat().st_mode) & 0o111 != license_mode
        ):
            drift.append(str(license_path))
        for filename, recipients in SHARED_RESOURCE_MAP.items():
            target = skill / "references" / filename
            if name in recipients:
                source = root / "skill-resources" / filename
                if (
                    not target.is_file()
                    or target.read_bytes() != source.read_bytes()
                    or stat.S_IMODE(target.stat().st_mode) & 0o111
                    != stat.S_IMODE(source.stat().st_mode) & 0o111
                ):
                    drift.append(str(target))
            elif target.exists():
                drift.append(str(target))
        references = skill / "references"
        if references.is_dir():
            for path in references.glob("*.md"):
                if path.name in shared_names and name not in SHARED_RESOURCE_MAP[path.name]:
                    drift.append(str(path))
    return sorted(set(drift))


def _build_staging(root: Path, staging: Path) -> Path:
    package = staging / "vision-harness"
    package.mkdir()
    shutil.copy2(root / PLUGIN_RELATIVE / "README.md", package / "README.md")
    shutil.copy2(root / "LICENSE", package / "LICENSE")
    (package / ".codex-plugin").mkdir()
    shutil.copy2(
        root / PLUGIN_RELATIVE / ".codex-plugin/plugin.json",
        package / ".codex-plugin/plugin.json",
    )
    skills = package / "skills"
    skills.mkdir()
    license_bytes = (root / "LICENSE").read_bytes()
    for name in SOURCE_SKILLS:
        destination = skills / name
        _copytree(root / ".agents" / "skills" / name, destination)
        validator.validate_skill(destination, expected_license=license_bytes)
    return package


def tree_snapshot(
    root: Path, *, exclude_development: bool = False
) -> dict[str, tuple[str, int]]:
    if not root.is_dir():
        return {}
    return {
        str(path.relative_to(root)): (
            hashlib.sha256(path.read_bytes()).hexdigest(),
            stat.S_IMODE(path.stat().st_mode) & 0o111,
        )
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and not (
            exclude_development
            and validator.is_development_artifact(path.relative_to(root))
        )
    }


def _tree_differences(
    actual: Path,
    expected: Path,
    *,
    actual_excludes_development: bool = False,
    expected_excludes_development: bool = False,
) -> list[str]:
    actual_state = tree_snapshot(actual, exclude_development=actual_excludes_development)
    expected_state = tree_snapshot(expected, exclude_development=expected_excludes_development)
    differences = []
    for relative in sorted(set(actual_state) | set(expected_state)):
        if relative not in actual_state:
            differences.append(f"missing: {actual / relative}")
        elif relative not in expected_state:
            differences.append(f"extra: {actual / relative}")
        elif actual_state[relative][0] != expected_state[relative][0]:
            differences.append(f"content differs: {actual / relative}")
        elif actual_state[relative][1] != expected_state[relative][1]:
            differences.append(f"executable mode differs: {actual / relative}")
    return differences


def assemble(root: Path = ROOT) -> None:
    root = Path(root).resolve()
    _validate_inputs(root)
    _sync_source_generated(root)
    validator.validate_source(root)

    plugin = root / PLUGIN_RELATIVE
    plugin.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".vision-harness-stage-", dir=plugin.parent) as temp:
        staged = _build_staging(root, Path(temp))
        differences = []
        for name in SOURCE_SKILLS:
            differences.extend(
                _tree_differences(
                    staged / "skills" / name,
                    root / ".agents" / "skills" / name,
                    expected_excludes_development=True,
                )
            )
        if differences:
            raise validator.ValidationError("invalid staged Skill tree: " + "; ".join(differences))

        incoming = staged / "skills"
        current = plugin / "skills"
        backup = Path(temp) / "previous-skills"
        if current.exists():
            os.replace(current, backup)
        try:
            os.replace(incoming, current)
        except Exception:
            if backup.exists() and not current.exists():
                os.replace(backup, current)
            raise
        if backup.exists():
            shutil.rmtree(backup)
        shutil.copy2(staged / "LICENSE", plugin / "LICENSE")
        obsolete = plugin / "references"
        if obsolete.exists():
            shutil.rmtree(obsolete)

    validator.validate_package(root)
    print(f"assembled {len(SOURCE_SKILLS)} self-contained Skills: {plugin}")


def check(root: Path = ROOT) -> None:
    root = Path(root).resolve()
    _validate_inputs(root)
    drift = _source_generated_drift(root)
    if drift:
        raise SystemExit("generated source drift: " + ", ".join(drift))
    validator.validate_source(root)
    plugin = root / PLUGIN_RELATIVE
    with tempfile.TemporaryDirectory(prefix="vision-harness-check-") as temp:
        expected = _build_staging(root, Path(temp))
        differences = _tree_differences(plugin, expected)
    if differences:
        raise SystemExit("plugin assembly drift:\n" + "\n".join(differences))
    validator.validate_package(root)
    print(f"read-only assembly check passed: {len(tree_snapshot(plugin))} files")


def _unsafe_output(output: Path, root: Path) -> bool:
    resolved = output.resolve(strict=False)
    repository = root.resolve()
    return resolved == repository or resolved.is_relative_to(repository) or repository.is_relative_to(resolved)


def export_skill(name: str, output: Path, root: Path = ROOT) -> Path:
    root = Path(root).resolve()
    if name == "method-evaluation" or name not in SOURCE_SKILLS:
        raise ValueError(f"Skill is not exportable: {name}")
    output = Path(output)
    if _unsafe_output(output, root):
        raise ValueError(f"output may not point into or contain the repository: {output}")
    validator.validate_source(root)
    validator.validate_package(root)
    source = root / ".agents" / "skills" / name
    packaged = root / PLUGIN_RELATIVE / "skills" / name
    if tree_snapshot(source, exclude_development=True) != tree_snapshot(packaged):
        raise ValueError(f"source Skill does not match packaged Skill: {name}")
    target = output.resolve(strict=False) / name
    if target.exists():
        if target.is_dir() and not any(target.iterdir()):
            target.rmdir()
        else:
            raise ValueError(f"export target already exists and is not empty: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    _copytree(source, target)
    validator.validate_skill(target)
    if tree_snapshot(target) != tree_snapshot(packaged):
        shutil.rmtree(target)
        raise ValueError(f"export differs from packaged Skill: {name}")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="read-only source and package drift check")
    parser.add_argument("--export-skill", metavar="NAME", help="export one ordinary Skill")
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
            target = export_skill(args.export_skill, args.output, ROOT)
            print(f"exported Skill: {target}")
        elif args.output:
            parser.error("--output requires --export-skill")
        else:
            assemble(ROOT)
    except (validator.ValidationError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
