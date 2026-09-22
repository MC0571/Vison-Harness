#!/usr/bin/env python3
"""Validate self-contained Vision Harness Skill sources and packages."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "vision-harness"
PORTABLE_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"

SOURCE_SKILLS = (
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
)

SHARED_RESOURCE_MAP = {
    "common-rules.md": frozenset(SOURCE_SKILLS),
    "critical-assumptions.md": frozenset(
        {"vision-management", "breakdown", "technical-design"}
    ),
    "complexity-control.md": frozenset(
        {"technical-design", "tdd-development", "review", "project-convergence"}
    ),
    "evidence-rules.md": frozenset(
        {"tdd-development", "review", "change-verification", "release-delivery"}
    ),
}

REMOVED_ENTRIES = frozenset(
    {
        "assumption-validation",
        "issue-shaping",
        "delivery-coordination",
        "simplification",
        "spec-review",
        "code-review",
        "pr-review",
        "review-setup",
    }
)

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(
    r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?(?:\+[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?$"
)
EXPLICIT_ANCHOR_RE = re.compile(
    r"<(?:a|[^>]+)\s+(?:id|name)=[\"']([^\"']+)[\"']", re.IGNORECASE
)
MARKDOWN = MarkdownIt("commonmark")
MARKDOWN.validateLink = lambda _url: True
IGNORED_NAMES = {
    ".DS_Store",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
}


class ValidationError(ValueError):
    """A deterministic Skill or package validation failure."""


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValidationError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping
)


def _frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValidationError(f"missing YAML frontmatter: {path}")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValidationError(f"unterminated YAML frontmatter: {path}") from exc
    try:
        metadata = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeyLoader)
    except ValidationError:
        raise
    except yaml.YAMLError as exc:
        raise ValidationError(f"invalid YAML frontmatter in {path}: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ValidationError(f"frontmatter must be a mapping: {path}")
    return metadata, "\n".join(lines[end + 1 :]) + "\n"


def _validate_metadata(metadata: dict, skill: Path) -> None:
    allowed = {
        "name",
        "description",
        "license",
        "compatibility",
        "metadata",
        "allowed-tools",
    }
    unknown = sorted(set(metadata) - allowed)
    if unknown:
        raise ValidationError(f"unknown frontmatter fields in {skill}: {', '.join(unknown)}")

    name = metadata.get("name")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name) or len(name) > 64:
        raise ValidationError(f"invalid Skill name in {skill}: {name!r}")
    if name != skill.name:
        raise ValidationError(f"Skill name does not match directory {skill}: {name!r}")

    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        raise ValidationError(f"invalid Skill description in {skill}")

    license_name = metadata.get("license")
    if license_name != "MIT":
        raise ValidationError(f"license must be 'MIT' in {skill}")

    compatibility = metadata.get("compatibility")
    if compatibility is not None and (
        not isinstance(compatibility, str) or not compatibility or len(compatibility) > 500
    ):
        raise ValidationError(f"invalid compatibility field in {skill}")
    extra = metadata.get("metadata")
    if extra is not None and (
        not isinstance(extra, dict)
        or any(not isinstance(key, str) or not isinstance(value, str) for key, value in extra.items())
    ):
        raise ValidationError(f"metadata must map strings to strings in {skill}")
    allowed_tools = metadata.get("allowed-tools")
    if allowed_tools is not None and not isinstance(allowed_tools, str):
        raise ValidationError(f"allowed-tools must be a string in {skill}")


def is_development_artifact(relative: Path) -> bool:
    return any(part in IGNORED_NAMES for part in relative.parts) or relative.name.endswith(
        (".pyc", ".pyo", ".tmp", ".swp")
    ) or relative.name.startswith(".tmp-")


def reject_symlinks(root: Path) -> None:
    if root.is_symlink():
        raise ValidationError(f"symbolic link is not allowed: {root}")
    if root.is_dir():
        for path in root.rglob("*"):
            if path.is_symlink():
                raise ValidationError(f"symbolic link is not allowed: {path}")


def _tokens_with_children(text: str):
    for token in MARKDOWN.parse(text):
        yield token
        yield from token.children or ()


def _link_targets(text: str) -> list[str]:
    targets: list[str] = []
    for token in _tokens_with_children(text):
        if token.type == "link_open":
            href = token.attrGet("href")
            if href:
                targets.append(href)
        elif token.type == "image":
            src = token.attrGet("src")
            if src:
                targets.append(src)
    return targets


def _slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\-\u0080-\uffff ]", "", text)
    return re.sub(r"[\s-]+", "-", text).strip("-")


def _anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    tokens = MARKDOWN.parse(text)
    anchors = set()
    for token in tokens:
        if token.type in {"html_inline", "html_block"}:
            anchors.update(EXPLICIT_ANCHOR_RE.findall(token.content))
        for child in token.children or ():
            if child.type in {"html_inline", "html_block"}:
                anchors.update(EXPLICIT_ANCHOR_RE.findall(child.content))
    for index, token in enumerate(tokens[:-1]):
        if token.type == "heading_open" and tokens[index + 1].type == "inline":
            anchors.add(_slug(tokens[index + 1].content))
    return anchors


def _resolve_local_link(source: Path, raw_target: str, skill: Path) -> tuple[Path, str] | None:
    parsed = urlsplit(raw_target)
    if parsed.scheme in {"http", "https", "mailto"}:
        if parsed.hostname == "raw.githubusercontent.com" or (
            parsed.hostname == "github.com" and "/raw/" in parsed.path
        ):
            raise ValidationError(
                f"GitHub raw links may not supply Skill runtime methods in {source}: {raw_target}"
            )
        return None
    if parsed.scheme or parsed.netloc or re.match(r"^[A-Za-z]:[\\/]", raw_target):
        raise ValidationError(f"absolute local link is not allowed in {source}: {raw_target}")
    decoded = unquote(parsed.path)
    if not decoded:
        return source, unquote(parsed.fragment)
    if Path(decoded).is_absolute():
        raise ValidationError(f"absolute local link is not allowed in {source}: {raw_target}")
    target = (source.parent / decoded).resolve(strict=False)
    try:
        target.relative_to(skill.resolve())
    except ValueError as exc:
        raise ValidationError(f"local link escapes Skill root in {source}: {raw_target}") from exc
    return target, unquote(parsed.fragment)


def _validate_links(path: Path, skill: Path) -> set[Path]:
    linked: set[Path] = set()
    text = path.read_text(encoding="utf-8")
    for raw_target in _link_targets(text):
        resolved = _resolve_local_link(path, raw_target, skill)
        if resolved is None:
            continue
        target, fragment = resolved
        if not target.exists():
            raise ValidationError(f"local link target does not exist in {path}: {raw_target}")
        if not target.is_file():
            raise ValidationError(f"local link target is not a file in {path}: {raw_target}")
        linked.add(target)
        if fragment and (target.suffix.lower() != ".md" or fragment not in _anchors(target)):
            raise ValidationError(f"missing anchor in {path}: {raw_target}")
    return linked


def validate_skill(skill: Path, *, expected_license: bytes | None = None) -> None:
    skill = Path(skill)
    if not skill.is_dir():
        raise ValidationError(f"Skill directory does not exist: {skill}")
    reject_symlinks(skill)

    skill_file = skill / "SKILL.md"
    if not skill_file.is_file():
        raise ValidationError(f"missing SKILL.md: {skill}")
    metadata, body = _frontmatter(skill_file)
    _validate_metadata(metadata, skill)
    if not body.strip():
        raise ValidationError(f"empty Skill instructions: {skill_file}")

    license_file = skill / "LICENSE"
    if not license_file.is_file():
        raise ValidationError(f"missing LICENSE: {skill}")
    if expected_license is not None and license_file.read_bytes() != expected_license:
        raise ValidationError(f"Skill LICENSE differs from repository LICENSE: {license_file}")

    direct_links = _validate_links(skill_file, skill)
    for path in skill.rglob("*.md"):
        if path != skill_file and not is_development_artifact(path.relative_to(skill)):
            _validate_links(path, skill)

    runtime_files = {
        path.resolve()
        for directory_name in ("references", "assets")
        for path in (skill / directory_name).rglob("*")
        if (skill / directory_name).is_dir()
        and path.is_file()
        and not is_development_artifact(path.relative_to(skill))
    }
    unlinked = sorted(str(path.relative_to(skill.resolve())) for path in runtime_files - direct_links)
    if unlinked:
        raise ValidationError(
            f"runtime resource is not directly linked from {skill_file}: {', '.join(unlinked)}"
        )


def _skill_dirs(root: Path) -> set[str]:
    return {path.parent.name for path in root.glob("*/SKILL.md")}


def validate_source(root: Path = ROOT) -> None:
    root = Path(root)
    skills_root = root / ".agents" / "skills"
    actual = _skill_dirs(skills_root)
    expected = set(SOURCE_SKILLS) | {"method-evaluation"}
    if actual != expected:
        raise ValidationError(
            f"source Skill set differs: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}"
        )
    license_path = root / "LICENSE"
    if not license_path.is_file():
        raise ValidationError(f"missing repository LICENSE: {license_path}")
    license_bytes = license_path.read_bytes()
    shared_names = set(SHARED_RESOURCE_MAP)
    for name in SOURCE_SKILLS:
        skill = skills_root / name
        validate_skill(skill, expected_license=license_bytes)
        actual_shared = {
            path.name
            for path in (skill / "references").glob("*.md")
            if path.name in shared_names
        }
        expected_shared = {
            filename for filename, recipients in SHARED_RESOURCE_MAP.items() if name in recipients
        }
        if actual_shared != expected_shared:
            raise ValidationError(
                f"shared resource set differs in {skill}: "
                f"missing={sorted(expected_shared - actual_shared)}, "
                f"extra={sorted(actual_shared - expected_shared)}"
            )
        for filename in expected_shared:
            source = root / "skill-resources" / filename
            target = skill / "references" / filename
            if not source.is_file() or target.read_bytes() != source.read_bytes():
                raise ValidationError(f"shared resource drift: {target}")


def validate_manifests(root: Path = ROOT) -> None:
    root = Path(root)
    package = root / "plugins" / "vision-harness"
    manifest_path = package / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"invalid plugin manifest: {manifest_path}: {exc}") from exc
    if not isinstance(manifest, dict):
        raise ValidationError(f"plugin manifest must be an object: {manifest_path}")
    if manifest.get("$schema") != PORTABLE_SCHEMA:
        raise ValidationError(f"invalid portable plugin schema: {manifest_path}")
    if manifest.get("name") != "vision-harness":
        raise ValidationError(f"invalid plugin name: {manifest_path}")
    if not isinstance(manifest.get("version"), str) or not VERSION_RE.fullmatch(manifest["version"]):
        raise ValidationError(f"invalid plugin version: {manifest_path}")
    allowed = {
        "$schema",
        "name",
        "version",
        "description",
        "author",
        "homepage",
        "repository",
        "license",
        "keywords",
        "extensions",
    }
    unknown = sorted(set(manifest) - allowed)
    if unknown:
        raise ValidationError(
            f"unknown portable plugin fields in {manifest_path}: {', '.join(unknown)}"
        )
    extensions = manifest.get("extensions")
    if not isinstance(extensions, dict):
        raise ValidationError(f"invalid plugin extensions: {manifest_path}")
    openai_extension = extensions.get("com.openai")
    if not isinstance(openai_extension, dict):
        raise ValidationError(f"invalid OpenAI interface extension: {manifest_path}")
    interface = openai_extension.get("interface")
    if not isinstance(interface, dict):
        raise ValidationError(f"missing OpenAI interface extension: {manifest_path}")
    marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
    try:
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"invalid marketplace manifest: {marketplace_path}: {exc}") from exc
    if not isinstance(marketplace, dict):
        raise ValidationError(f"marketplace manifest must be an object: {marketplace_path}")
    if marketplace.get("name") != "MC":
        raise ValidationError(f"marketplace name must be 'MC': {marketplace_path}")
    marketplace_interface = marketplace.get("interface")
    if (
        not isinstance(marketplace_interface, dict)
        or marketplace_interface.get("displayName") != "MC"
    ):
        raise ValidationError(f"marketplace display name must be 'MC': {marketplace_path}")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or any(not isinstance(item, dict) for item in plugins):
        raise ValidationError(f"marketplace plugins must be an array of objects: {marketplace_path}")
    matching = [item for item in plugins if item.get("name") == "vision-harness"]
    if len(matching) != 1 or matching[0].get("source", {}).get("path") != "./plugins/vision-harness":
        raise ValidationError(f"marketplace path does not match package: {marketplace_path}")


def _same_tree(left: Path, right: Path) -> bool:
    def state(root: Path, exclude_development: bool):
        return {
            str(path.relative_to(root)): (path.read_bytes(), path.stat().st_mode & 0o111)
            for path in root.rglob("*")
            if path.is_file()
            and not (
                exclude_development and is_development_artifact(path.relative_to(root))
            )
        }

    return state(left, True) == state(right, False)


def validate_package(root: Path = ROOT) -> None:
    root = Path(root)
    package = root / "plugins" / "vision-harness"
    skills_root = package / "skills"
    actual = _skill_dirs(skills_root)
    expected = set(SOURCE_SKILLS)
    if actual != expected:
        raise ValidationError(
            f"package Skill set differs: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}"
        )
    if (package / "references").exists():
        raise ValidationError(f"obsolete plugin root references remain: {package / 'references'}")

    license_path = root / "LICENSE"
    package_license = package / "LICENSE"
    if not license_path.is_file() or not package_license.is_file():
        raise ValidationError(f"missing repository or plugin LICENSE: {license_path}, {package_license}")
    license_bytes = license_path.read_bytes()
    if package_license.read_bytes() != license_bytes:
        raise ValidationError(f"plugin LICENSE differs from repository LICENSE: {package_license}")
    for name in SOURCE_SKILLS:
        packaged = skills_root / name
        validate_skill(packaged, expected_license=license_bytes)
        source = root / ".agents" / "skills" / name
        if not _same_tree(source, packaged):
            raise ValidationError(f"source and package Skill directories differ: {name}")
    for name in REMOVED_ENTRIES | {"method-evaluation"}:
        if (skills_root / name).exists():
            raise ValidationError(f"maintainer or removed Skill leaked into package: {name}")

    validate_manifests(root)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--source", action="store_true", help="validate source Skill directories")
    modes.add_argument("--package", action="store_true", help="validate the assembled Plugin")
    modes.add_argument("--skill", type=Path, help="validate one standalone absolute Skill path")
    args = parser.parse_args()
    try:
        if args.source:
            validate_source(ROOT)
            label = "source skills"
        elif args.package:
            validate_package(ROOT)
            label = "package skills"
        else:
            if not args.skill.is_absolute():
                raise ValidationError("--skill requires an absolute path")
            validate_skill(args.skill)
            label = str(args.skill)
    except ValidationError as exc:
        raise SystemExit(str(exc)) from exc
    print(f"validated: {label}")


if __name__ == "__main__":
    main()
