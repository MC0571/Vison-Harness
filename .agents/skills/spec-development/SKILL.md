---
name: spec-development
description: Use when a confirmed change may alter observable behavior, state, invariants, interfaces, permissions, failures, or compatibility and needs a durable semantic contract. Returns a focused Spec change or a justified no-change result; it does not turn implementation progress into requirements.
license: MIT
---

# Spec Development

交付长期行为约定的必要变化，或明确说明现有 Spec 足够/本次无需修改。

## 何时使用／何时不使用

用于新增行为、明确现有意图、修正错误规格或检查 Spec surface。纯内部重构且可观察行为不变时返回零 Spec 修改；一个 Issue 不等于一个 Spec。

## 输入与环境条件

需要已确认工作范围和可定位的现有语义规格。用户请求与有效产品决定定义应承诺什么；代码只说明当前实现，不能反推需求。未决产品取舍由用户决定。

## 开始前的最少读取

读取请求/工作项的确认范围、相关长期行为约定和相邻语义边界。只读与状态、接口、权限、失败或兼容变化有关的部分。

## 执行步骤与关键分支

1. 判断是否改变可观察行为、状态、不变量、接口、权限、失败、兼容或必要非功能保证。
2. 分类为新行为、明确现有意图、修正错误规格或纯内部重构；最后一种直接给出无需修改依据。
3. 按稳定领域/能力/契约语义定位已有规格，不按 Issue 编号、日期或阶段建目录。
4. 从确认请求提炼概念、前置条件、事件、结果、不变量和异常；把模糊要求改成可判断行为。
5. 检查相邻规格的术语、状态、所有权、权限与兼容冲突；未知取舍保持未决，不用实现偏好补答案。
6. 只更新受影响语义，并在授权写入后回读；不写 workflow 状态、负责人、优先级、里程碑或实施进度。

## 按条件加载的本地资源

| 触发条件 | 文件 | 使用目的 |
| --- | --- | --- |
| 判断是否需要 Spec | [Spec surface](references/spec-surface.md) | 区分行为变化与内部重构 |
| 编写或修改行为约定 | [Spec 写作](references/spec-authoring.md) | 形成可判断语义并查冲突 |
| 获准新建且无等价布局 | [行为规格提纲](assets/behavior-spec-outline.md) | 作为可选语义起点 |
| 涉及写入与完成层级 | [共同操作边界](references/common-rules.md) | 区分规格、实现与验收 |

## 输出与完成条件

输出行为改动或无需修改结论、受影响语义边界、实际文件变化和未决决定。只读请求止于建议；无行为变化以零修改完成；关键产品取舍缺失时只阻塞相关条款。规格完成不等于实现或审查通过。

## 异常与停止边界

不把当前代码缺陷写成期望行为，不用技术方案约束产品实现自由。未经授权不改文件，不自动创建 Issue、ADR、代码或 PR。

## 简短输入输出示例

正常：要求“超时后不可回到完成态”。Spec 明确事件、状态转换、不变量和恢复异常，并检查相邻取消语义。

边界：重命名私有函数且对外行为不变，输出“无需 Spec 修改”，不新建文件。
