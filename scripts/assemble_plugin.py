#!/usr/bin/env python3
"""Assemble the self-contained Vision Harness distribution package."""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "vision-harness"

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

# method-evaluation is a maintainer entry, not part of the ordinary distribution.
REFERENCE_SECTIONS = {
    "shared-rules.md": (
        ROOT / "METHOD.md",
        (
            "## 1. 先确认本轮任务和授权",
            "## 5. 正确读取和安全修改项目事实",
            "## 12. 方法必须同时防止草率和过度治理",
        ),
    ),
    "planning-methods.md": (
        ROOT / "METHOD.md",
        (
            "## 3. 保留完整目标，但明确本次交付",
            "## 4. 维护依赖，并设计有效的推进方式",
        ),
    ),
    "agent-config-methods.md": (
        ROOT / "METHOD.md",
        ("## 6. 维护 Agent 工作约定和审查规则",),
    ),
    "spec-design-methods.md": (
        ROOT / "METHOD.md",
        ("## 7. 按变化维护 Spec、架构和决策",),
    ),
    "implementation-methods.md": (
        ROOT / "METHOD.md",
        ("## 8. 用 TDD 实施，同时抑制没有依据的复杂度",),
    ),
    "review-methods.md": (
        ROOT / "METHOD.md",
        ("## 9. 按对象组织审查，而不是机械增加审查轮次",),
    ),
    "evidence-methods.md": (
        ROOT / "METHOD.md",
        ("## 10. 用适用证据判断完成和交付",),
    ),
    "convergence-methods.md": (
        ROOT / "METHOD.md",
        ("## 11. 根据新事实继续、调整或停止",),
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
    "review-behavior.md": (
        ROOT / "specs" / "review" / "spec.md",
        (
            "## 适用对象与授权边界",
            "## 证据与候选",
            "## 三类审查",
            "## 结果与后续",
        ),
    ),
}

SKILL_REFERENCE_REWRITES = {
    "../../../METHOD.md#1-先确认本轮任务和授权":
        "../../references/shared-rules.md#1-先确认本轮任务和授权",
    "../../../METHOD.md#3-保留完整目标但明确本次交付":
        "../../references/planning-methods.md#3-保留完整目标但明确本次交付",
    "../../../METHOD.md#4-维护依赖并设计有效的推进方式":
        "../../references/planning-methods.md#4-维护依赖并设计有效的推进方式",
    "../../../METHOD.md#6-维护-agent-工作约定和审查规则":
        "../../references/agent-config-methods.md#6-维护-agent-工作约定和审查规则",
    "../../../METHOD.md#7-按变化维护-spec架构和决策":
        "../../references/spec-design-methods.md#7-按变化维护-spec架构和决策",
    "../../../METHOD.md#8-用-tdd-实施同时抑制没有依据的复杂度":
        "../../references/implementation-methods.md#8-用-tdd-实施同时抑制没有依据的复杂度",
    "../../../METHOD.md#9-按对象组织审查而不是机械增加审查轮次":
        "../../references/review-methods.md#9-按对象组织审查而不是机械增加审查轮次",
    "../../../METHOD.md#10-用适用证据判断完成和交付":
        "../../references/evidence-methods.md#10-用适用证据判断完成和交付",
    "../../../METHOD.md#11-根据新事实继续调整或停止":
        "../../references/convergence-methods.md#11-根据新事实继续调整或停止",
    "../../../specs/vision/spec.md":
        "../../references/vision-behavior.md",
    "../../../specs/project-context/spec.md":
        "../../references/project-context-behavior.md",
    "../../../specs/breakdown/spec.md":
        "../../references/breakdown-behavior.md",
    "../../../specs/review/spec.md":
        "../../references/review-behavior.md",
}

RUNTIME_LINK_REWRITES = {
    "../../METHOD.md": "shared-rules.md",
    "../vision/spec.md": "vision-behavior.md",
    "../project-context/spec.md": "project-context-behavior.md",
    "../breakdown/spec.md": "breakdown-behavior.md",
    "../review/spec.md": "review-behavior.md",
}

MARKDOWN_LINK_RE = re.compile(r"\[([^]]+)\]\(([^)]+)\)")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def selected_sections(source: Path, headings: tuple[str, ...]) -> str:
    lines = read_text(source).splitlines()
    configured = list(headings)
    if len(configured) != len(set(configured)):
        raise ValueError(f"duplicate configured section in {source}")

    actual_headings = [line for line in lines if line.startswith("## ")]
    for heading in configured:
        matches = [line for line in actual_headings if line == heading]
        if not matches:
            candidates = [line for line in actual_headings if line.startswith(heading)]
            detail = f"; similar headings: {candidates}" if candidates else ""
            raise ValueError(
                f"configured section must match exactly in {source}: {heading}{detail}"
            )
        if len(matches) > 1:
            raise ValueError(f"duplicate source section in {source}: {heading}")

    selected: list[str] = []
    current: list[str] = []
    wanted = set(configured)

    def flush() -> None:
        if current:
            selected.extend(current)

    for line in lines:
        if line.startswith("## "):
            flush()
            current = [line] if line in wanted else []
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
        "This runtime reference is generated from the repository's accepted method "
        "and behavior sources. It is intentionally self-contained; edit the source "
        "documents and rerun the assembly instead of hand-editing this file.\n\n"
        f"{body}\n"
    )


def write_utf8(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def assemble(destination: Path = PLUGIN) -> None:
    if not destination.is_dir():
        raise SystemExit(f"missing plugin destination: {destination}")

    generated_dirs = (destination / "skills", destination / "references")
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
        write_utf8(destination / "skills" / skill_name / "SKILL.md", content)

    for filename, (source, headings) in REFERENCE_SECTIONS.items():
        write_utf8(
            destination / "references" / filename,
            runtime_reference(filename, source, headings),
        )

    shutil.copyfile(ROOT / "LICENSE", destination / "LICENSE")
    assert_package_links(destination)


def assert_package_links(package: Path = PLUGIN) -> None:
    for path in sorted(package.rglob("*.md")):
        text = read_text(path)
        if "../../../" in text or "../../../../" in text:
            raise ValueError(f"package path escapes root: {path}")
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = match.group(2).split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).resolve().is_file():
                raise ValueError(f"broken package link in {path}: {target}")


def snapshot(package: Path = PLUGIN) -> dict[str, str]:
    paths = sorted(
        path
        for path in package.rglob("*")
        if path.is_file() and ".git" not in path.parts
    )
    return {
        str(path.relative_to(package)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
    }


def check_idempotent(package: Path = PLUGIN) -> None:
    if not package.is_dir():
        raise SystemExit(f"missing plugin package: {package}")
    assert_package_links(package)

    with tempfile.TemporaryDirectory(prefix="vision-harness-assembly-") as temp_dir:
        expected = Path(temp_dir) / package.name
        shutil.copytree(package, expected)
        assemble(expected)
        first = snapshot(expected)
        current = snapshot(package)
        if current != first:
            changed = sorted(
                path
                for path in set(current) | set(first)
                if current.get(path) != first.get(path)
            )
            raise SystemExit(f"plugin assembly drift: {', '.join(changed)}")

        assemble(expected)
        second = snapshot(expected)
        if first != second:
            raise SystemExit("plugin assembly is not deterministic")
    print(f"deterministic assembly passed: {len(first)} package files")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "compare the package with an independent deterministic assembly "
            "without rewriting it"
        ),
    )
    args = parser.parse_args()
    check_idempotent() if args.check else assemble()


if __name__ == "__main__":
    main()
