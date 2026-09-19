#!/usr/bin/env python3
"""Assemble the self-contained Vision Harness distribution package."""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "vision-harness"

SOURCE_SKILLS = (
    "using-vision-harness",
    "project-onboarding",
    "vision-management",
    "agent-instructions",
    "breakdown",
)

REFERENCE_SECTIONS = {
    "shared-rules.md": (
        ROOT / "METHOD.md",
        (
            "## 1. ",
            "## 3. ",
            "## 5. ",
            "## 6. ",
            "## 8. ",
            "## 10. ",
            "## 11. ",
            "## 12. ",
        ),
    ),
    "vision-behavior.md": (
        ROOT / "specs" / "vision" / "spec.md",
        (
            "## 输入与适用事实",
            "## 可观察的对话行为",
            "## 充分性与结束结果",
            "## 修订与副作用",
        ),
    ),
    "project-context-behavior.md": (
        ROOT / "specs" / "project-context" / "spec.md",
        (
            "## 适用职责",
            "## 来源与上下文正确性",
            "## 新会话与授权有效性",
            "## 按缺口接入与规则维护",
            "## 条件交接与分发隔离",
        ),
    ),
    "breakdown-behavior.md": (
        ROOT / "specs" / "breakdown" / "spec.md",
        (
            "## 用途与边界",
            "## 输入与当前依据",
            "## 对象含义",
            "## 初始拆解",
            "## 下一批次细化",
            "## 已有规划审查与修订",
            "## 获准写入与失败处理",
            "## 输出与结束",
        ),
    ),
}

SKILL_REFERENCE_REWRITES = {
    "../../../METHOD.md": "../../references/shared-rules.md",
    "../../../specs/vision/spec.md": "../../references/vision-behavior.md",
    "../../../specs/project-context/spec.md": "../../references/project-context-behavior.md",
    "../../../specs/breakdown/spec.md": "../../references/breakdown-behavior.md",
}

RUNTIME_LINK_REWRITES = {
    "../../METHOD.md": "shared-rules.md",
    "../vision/spec.md": "vision-behavior.md",
    "../project-context/spec.md": "project-context-behavior.md",
    "../breakdown/spec.md": "breakdown-behavior.md",
}

MARKDOWN_LINK_RE = re.compile(r"\[([^]]+)\]\(([^)]+)\)")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def selected_sections(source: Path, headings: tuple[str, ...]) -> str:
    lines = read_text(source).splitlines()
    selected: list[str] = []
    current: list[str] = []
    wanted = set(headings)

    def flush() -> None:
        if current:
            selected.extend(current)

    for line in lines:
        if line.startswith("## "):
            flush()
            current = [line] if any(line.startswith(prefix) for prefix in wanted) else []
            continue
        if current:
            current.append(line)
    flush()
    if not selected:
        raise ValueError(f"no configured sections found in {source}")
    return "\n".join(selected).strip()


def rewrite_runtime_links(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        label, target = match.groups()
        path, separator, anchor = target.partition("#")
        if path in RUNTIME_LINK_REWRITES:
            rewritten = RUNTIME_LINK_REWRITES[path]
            return f"[{label}]({rewritten}{separator}{anchor})"
        if path.startswith("."):
            return label
        return match.group(0)

    return MARKDOWN_LINK_RE.sub(replace, text)


def runtime_reference(filename: str, source: Path, headings: tuple[str, ...]) -> str:
    title = filename.removesuffix(".md").replace("-", " ").title()
    body = rewrite_runtime_links(selected_sections(source, headings))
    return (
        f"# {title}\n\n"
        "This runtime reference is generated from the repository's accepted method and behavior "
        "sources. It is intentionally self-contained; edit the source documents and rerun the "
        "assembly instead of hand-editing this file.\n\n"
        f"{body}\n"
    )


def write_utf8(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def assemble() -> None:
    if not PLUGIN.is_dir():
        raise SystemExit(f"missing plugin scaffold: {PLUGIN}")

    generated_dirs = (PLUGIN / "skills", PLUGIN / "references")
    for directory in generated_dirs:
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True)

    for skill_name in SOURCE_SKILLS:
        source = ROOT / ".agents" / "skills" / skill_name / "SKILL.md"
        if not source.is_file():
            raise SystemExit(f"missing source Skill: {source}")
        content = read_text(source)
        for old, new in SKILL_REFERENCE_REWRITES.items():
            content = content.replace(old, new)
        if "../../../" in content or "../../../../" in content:
            raise ValueError(f"unconverted source path in {source}")
        write_utf8(PLUGIN / "skills" / skill_name / "SKILL.md", content)

    for filename, (source, headings) in REFERENCE_SECTIONS.items():
        write_utf8(PLUGIN / "references" / filename, runtime_reference(filename, source, headings))

    shutil.copyfile(ROOT / "LICENSE", PLUGIN / "LICENSE")
    assert_package_links()


def assert_package_links() -> None:
    for path in sorted(PLUGIN.rglob("*.md")):
        text = read_text(path)
        if "../../../" in text or "../../../../" in text:
            raise ValueError(f"package path escapes root: {path}")
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = match.group(2).split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).resolve().is_file():
                raise ValueError(f"broken package link in {path}: {target}")


def snapshot() -> dict[str, str]:
    paths = sorted(
        path
        for path in PLUGIN.rglob("*")
        if path.is_file() and ".git" not in path.parts
    )
    return {
        str(path.relative_to(PLUGIN)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
    }


def check_idempotent() -> None:
    assemble()
    first = snapshot()
    assemble()
    second = snapshot()
    if first != second:
        raise SystemExit("plugin assembly is not deterministic")
    print(f"deterministic assembly passed: {len(second)} package files")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="assemble twice and fail if the package changes between runs",
    )
    args = parser.parse_args()
    check_idempotent() if args.check else assemble()


if __name__ == "__main__":
    main()
