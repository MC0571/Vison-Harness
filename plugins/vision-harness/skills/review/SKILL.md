---
name: review
description: Use when a Spec, code change, or pull request needs an independent, candidate-bound review for correctness, regression, safety, scope, and evidence. Returns actionable findings or a clean limited judgment; review-only work never edits, commits, merges, or releases the candidate.
license: MIT
---

# Review

交付对准确 Spec、Code 或 PR 候选的独立、有依据、有限范围判断。

## 何时使用／何时不使用

三种对象模式：Spec、Code、PR。只审查时不修复候选；用户同时授权修复，也应先固定并形成原候选判断，再单独实施。不要从作者摘要直接生成结论。

## 输入与环境条件

需要审查对象、准确版本/比较基线和本轮范围。产品取舍缺失时指出而不代替用户决定。验证命令若会写入且未授权，报告缺口而不偷偷运行。

## 开始前的最少读取

固定 head、base 或文件版本；读取原始 Spec/diff/PR 内容、适用规则和与判断直接相关的调用关系/证据。旧审查只有在候选未影响其结论时才复用。

## 执行步骤与关键分支

1. 识别 Spec、Code 或 PR 对象，记录候选和比较基线。
2. Spec：检查确认范围、行为可判断性、异常/不变量、相邻语义冲突和未经确认的产品取舍；构造“符合字面却违反用户结果”的反例。
3. Code：沿真实 diff、入口和必要调用关系检查正确性、回归、边界、安全、错误传播和测试；复杂度问题必须有已确认需求/风险依据，不把风格偏好写成缺陷。
4. PR：核对当前 head 的范围、实现、证据、既有审查有效性、目标分支和关闭语义；不因“另有人审过”跳过当前必要检查。
5. 每个问题写位置、发生条件、机制、影响、依据、严重程度和最小修复方向；阻断与非阻断建议分开。
6. 没有发现阻断时正常返回；存在实质未验证范围时收窄总体判断。

## 按条件加载的本地资源

| 触发条件 | 文件 | 使用目的 |
| --- | --- | --- |
| 审查行为 Spec | [Spec 审查](references/spec-review.md) | 检查语义、反例和产品取舍 |
| 审查代码候选 | [Code 审查](references/code-review.md) | 沿 diff 与调用关系找回归 |
| 审查 Pull Request | [PR 审查](references/pr-review.md) | 核对 head、证据和关闭语义 |
| 检查无依据复杂度 | [复杂度控制](references/complexity-control.md) | 区分缺陷与风格偏好 |
| 复用或审计证据 | [证据规则](references/evidence-rules.md) | 限定证据适用范围 |
| 需要结构化报告 | [审查报告模板](assets/review-report.md) | 区分阻断、建议和限制 |
| 核对只读/写入边界 | [共同操作边界](references/common-rules.md) | 防止审查越权修改 |

## 输出与完成条件

输出绑定准确候选的问题清单、非阻断建议、证据限制和总体判断。无问题是正常完成；只读模式不产生候选变更；工具受限时明确未检查范围。审查通过不等于验收、合并或发布授权。

## 异常与停止边界

候选变化后只重审受影响部分。无法读取完整 diff 或基线不明时限制结论。未经授权不写评论、不修改文件、不提交、不合并、不发布。

## 简短输入输出示例

正常：指出 `parser.py:42` 对编码路径先解码后未再做 containment 检查，可越界读取；给出触发输入、影响、依据和最小修复方向。

边界：当前 PR 无阻断但未运行安装测试，输出“代码审查未发现阻断；安装行为未验证”，不凑问题。
