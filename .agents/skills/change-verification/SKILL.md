---
name: change-verification
description: Use to execute checks, reuse evidence, or audit a precise candidate against a concrete promise. Derives discriminating checks from failure modes and observation points, reports scoped outcomes and uncovered areas, and does not repair the candidate or inflate low-level checks into whole-product completion.
license: MIT
---

# Vision-Harness: Change Verification

交付与当前承诺匹配、绑定准确候选的证据及未覆盖范围，而不是通过数量。

## 何时使用／何时不使用

直接执行、证据复用、证据审计是并列模式。实现工作自行完成基本测试；需要进一步取证或判断现有证据时使用本入口。只读审计不自动运行命令，本技能不默认修代码。

## 输入与开始前的最少读取

固定要支持的结论、候选、环境与允许副作用。读取相关变更、原始证据和真实检查入口。根据内容影响而非扩展名判断：指令 Markdown 可能改变行为，普通文案则未必。

## 工作方法

1. 将当前承诺拆成需要判断的结果，找出会违反它的具体失败方式；不扩展成全产品验收。
2. 为每种重要失败选择能观察它的边界，再选择足以区分正确与错误的最小检查。跨组件承诺不能只靠局部 mock 或格式检查。
3. 核对已有证据的对象、版本、环境、入口和覆盖。说明当前变化为何影响或不影响其前提，只补失效与真正缺失部分。
4. 选择与风险相称的检查集合，说明必要覆盖与剩余限制；不为“更稳妥”重复同类低信息检查。
5. 直接执行前核对真实命令、目录、环境和副作用；保存退出码、关键输出、构件身份与候选，不只记录“成功”。
6. 失败先区分产品、设置、环境和权限。重试须有识别出的暂时原因或设置变化；不靠随机重跑抹掉失败，不降低断言。
7. 对照承诺报告 pass、fail、blocked、not-run、not-applicable，以及执行/继承/审计方式。继承的通过不是本轮又执行了一次。

## 按条件加载的本地资源

| 条件 | 文件 | 用途 |
| --- | --- | --- |
| 从承诺选择检查 | [验证选择](references/verification-selection.md) | 失败方式、观察点与最小集合 |
| 实际执行、处理失败或核对结果 | [验证执行](references/verification-execution.md) | 候选固定与证据保存 |
| 复用或审计旧证据 | [证据规则](references/evidence-rules.md) | 前提影响与有限结论 |
| 涉及文件、网络或外部资源 | [共同操作边界](references/common-rules.md) | 授权与安全副作用 |

## 输出与完成条件

说明对象、候选、结论范围、检查方式、逐项结果、覆盖和未覆盖内容。已经足以支持当前要求时完成，不无限追加检查。检查完成与检查通过不是同一件事，blocked 不得变成 pass。

## 停止与例外

候选改变后只让受影响证据失效。没有现成检查入口时可提出最小方法；实际创建或执行必须符合本轮权限，不凭空编造正式命令。验证不自动授权修复、独立审查、验收、合并、发布或关闭。

## 示例

公开协议改动：先指出调用者可能误读的字段/错误语义，选择真实边界检查；不以 JSON 能解析替代协议兼容。只改帮助文案且运行语义未变时，局部格式/链接检查可以足够，不要求全量重验。
