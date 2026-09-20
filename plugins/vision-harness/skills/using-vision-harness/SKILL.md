---
name: using-vision-harness
description: Identify the current project task, recover only the facts and authorization it needs, and choose a suitable Vision Harness method without acting as a router or scheduler.
---

# Using Vision Harness

Use this entry when a new request or a fresh session needs to determine what work is actually being requested. Read the [project-context behavior rules](../../references/project-context-behavior.md) and [shared operating rules](../../references/shared-rules.md) before choosing a method. It returns a bounded handoff to the relevant work; it does not perform that work.

Before choosing a method, do the following in order:

1. Identify the consumer project, working directory, current request, and the requested stopping point. Treat the installed package as method material, not as the consumer project's product facts.
2. Classify the request: high-level discussion, vision work, project onboarding, planning, implementation, review, verification, or delivery. Choose only the smallest applicable method.
3. Read the consumer project's authoritative sources needed for that choice: its `AGENTS.md`, `VISION.md` or equivalent, relevant Spec, current work item, and real tool/configuration entry points. Do not scan unrelated history merely because it exists.
4. Separate confirmed decisions, proposals, assumptions, unknowns, deferred work, evidence, and authorization. A review result, CI status, tool access, or issue state is not write permission.
5. State the next method, the allowed action, the facts still missing, and the stop boundary. If a required method is not installed, say so instead of pretending that it ran.

The output should make this handoff explicit:

```text
Task: what this request asks for
Sources: authoritative files/objects and versions actually read
Authorization: read, discuss, write, or another exact scope
Method: the next direct Skill or bounded action
Missing: only facts that change the next decision
Stop: where this entry returns control
```

Rules:

- This is a recognition and handoff entry, not a dispatcher, workflow engine, state store, or automatic permission grant.
- A clear existing issue can go directly to its work Skill; do not repeat onboarding or vision discovery when the facts are already sufficient.
- This package provides this entry and eighteen work Skills. Select from the task map below and read the chosen Skill before following its method. If the installed candidate lacks the selected file, report that limitation rather than inventing a successful handoff. `method-evaluation` is a separate maintainer entry and is not included in the ordinary package.
- Directly called work Skills must repeat their own authorization and shared-rule checks. Never use this entry as the sole safety gate.
- Recommendations remain recommendations. Do not turn silence, readiness, a parent issue, or a passing review into a product decision or implementation authorization.
- If the request is advice-only, stop after the bounded advice. Do not create files, issues, plans, or commits.
- If the request is authorized implementation, the authorization still ends at its stated boundary; merge, release, and unrelated project changes require their own authorization.
- A fresh session must recover from persistent consumer-project facts. Do not rely on an old transcript, hidden handoff, source checkout, or an uninstalled copy of a Skill.
- When a user changes a premise, reopen only the affected decision and retain unaffected facts. When facts are sufficient, stop rather than inventing more ceremony.

## 按任务选择，不执行固定流水线

以下链接只在对应工作需要时读取，不预加载全部 Skill。入口完成识别后交出当前范围、来源、权限与停止位置；各工作入口仍核对自己的动作，但不重复上游全仓调查。

| 当前任务 | 工作方法 |
| --- | --- |
| 新项目或已有项目接入 | [project-onboarding](../project-onboarding/SKILL.md) |
| 愿景讨论、检查与修订 | [vision-management](../vision-management/SKILL.md) |
| 可能改变当前路线的未知 | [assumption-validation](../assumption-validation/SKILL.md) |
| 整体规划与下一批滚动细化 | [breakdown](../breakdown/SKILL.md) |
| 整理单项范围与完成条件 | [issue-shaping](../issue-shaping/SKILL.md) |
| 多项依赖、并行与整合 | [delivery-coordination](../delivery-coordination/SKILL.md) |
| 定义或改变长期行为 | [spec-development](../spec-development/SKILL.md) |
| 实施方案、结构与长期取舍 | [technical-design](../technical-design/SKILL.md) |
| 明确行为实施或缺陷处理 | [tdd-development](../tdd-development/SKILL.md) |
| 设计、代码或流程简化 | [simplification](../simplification/SKILL.md) |
| 仅审查候选规格 | [spec-review](../spec-review/SKILL.md) |
| 仅审查实现 | [code-review](../code-review/SKILL.md) |
| 判断当前 PR 推进条件 | [pr-review](../pr-review/SKILL.md) |
| 获取或审计变更证据 | [change-verification](../change-verification/SKILL.md) |
| 构件交付、发布或工作收尾 | [release-delivery](../release-delivery/SKILL.md) |
| 整体偏离与长期纠偏 | [project-convergence](../project-convergence/SKILL.md) |
| 根或局部 Agent 指引维护 | [agent-instructions](../agent-instructions/SKILL.md) |
| 审查规则与宿主入口维护 | [review-setup](../review-setup/SKILL.md) |

已有明确缺陷直接进入缺陷处理；只审查不自动修复；只交付构件不自动发布。用户已明确要求实现完整范围时，不擅自缩为一个试验切片，也不把额外的全局 Eval 变成开工条件。必要的实现检查随工作完成，未运行的验证如实说明。
