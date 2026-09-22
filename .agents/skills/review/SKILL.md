---
name: review
description: Use when a Spec, implementation, or PR needs a candidate-bound judgment. Separates requirement fidelity from engineering quality, challenges potential findings with counterevidence, and returns actionable defects or a clean limited result without modifying a review-only candidate.
license: MIT
---

# Review

对准确 Spec、Code 或 PR 候选形成独立、有依据、有范围的判断。高质量审查不是问题数量，而是发现真实问题并过滤伪问题。

## 何时使用／何时不使用

Spec、Code、PR 三种对象可直接请求，不要求固定三轮审查或多个 Agent。只审查时不改候选；同时获准修复时先固定原候选判断，再转入独立实施步骤。

## 输入与开始前的最少读取

固定对象、版本、比较基线和本轮范围，读取原始规格/diff/PR、适用规则及直接相关的调用与证据。作者摘要只作导航。完整对象审查与差异审查分别声明范围，不把已有无关问题自动归给本次变更。

## 工作方法

1. 辨认审查对象与要作的判断，确认当前候选，避免混用旧 head 和新证据。
2. Spec 检查确认目标、可判断行为、不变量、失败与相邻语义，尝试构造“符合字面却不满足结果”的反例。
3. Code 同时看要求忠实度与工程质量：是否遗漏、错误实现或未经要求扩大行为；是否破坏责任、兼容、安全、错误传播和必要测试。两类问题不互相抵消。
4. PR 核对当前 head 的范围、实现、有效审查、检查、目标分支与关闭语义。复用未受影响的结论，不机械重做全部分析。
5. 在输出 finding 前尝试反证：触发条件真实可达吗？已有保护是否已处理？违反的是有效要求还是个人偏好？原问题是否属于当前范围？无法成立的删除或收窄为未决疑点。
6. 实质问题给出位置、条件、机制、影响、依据、严重程度和最小修复方向；结构问题说明该移动哪项责任、消除哪种负担，不仅说“太复杂”。
7. 分开阻断、非阻断建议和未检查范围。无实质问题是正常结果，证据有限则限制总体结论，不为体现工作量制造意见。

## 按条件加载的本地资源

| 条件 | 文件 | 用途 |
| --- | --- | --- |
| 审查行为约定 | [Spec 审查](references/spec-review.md) | 语义、反例与确认范围 |
| 审查实现 | [Code 审查](references/code-review.md) | 要求忠实度与工程质量 |
| 审查 PR | [PR 审查](references/pr-review.md) | 候选与交付范围 |
| 判断疑点是否值得报告 | [Finding 校准](references/finding-validation.md) | 反证、严重性与最小修复 |
| 结构与复杂度判断 | [复杂度控制](references/complexity-control.md) | 区分必要边界与多余负担 |
| 判断已有证据适用性 | [证据规则](references/evidence-rules.md) | 范围化继承与限制 |
| 需要结构化输出 | [审查模板](assets/review-report.md) | 可选报告起点 |
| 只读、评论或写入边界 | [共同操作边界](references/common-rules.md) | 授权和安全操作 |

## 输出与完成条件

报告准确候选、实质 finding、建议、证据限制和总体判断。没有可成立的阻断可返回通过或有限无阻断结论；未运行的检查不能冒称通过。审查完成不授予验收、合并或发布权限。

## 停止与例外

候选变化只重审受影响部分；基线或 diff 无法固定时不批准未知对象。检查命令可能修改候选或外部系统时先按权限处理；正常获准的检查不需逐条仪式性确认。未经授权不写评论、不改文件、不提交、不合并、不发布。

## 示例

发现解码后的路径可能越界：先核对后续 containment 检查是否存在、实际入口能否到达，再给触发输入和影响。已有完整保护则删除该疑点；未运行安装检查就限制安装结论，不凑另一条问题。
