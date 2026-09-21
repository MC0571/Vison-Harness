---
name: change-verification
description: Use when a precise candidate needs checks executed, existing evidence reused, or evidence audited against a concrete promise. Returns scoped pass, fail, blocked, not-run, and uncovered results; it does not repair the candidate or declare the whole product complete.
license: MIT
---

# Change Verification

交付与当前承诺相匹配、绑定准确候选的验证证据和未覆盖范围。

## 何时使用／何时不使用

三种模式：直接执行、证据复用、证据审计。用于需要独立取证或判断现有证据适用性时；实现过程中必要的基本测试仍由实现工作完成。本技能默认不修代码。

## 输入与环境条件

需要待证明承诺、候选、环境和允许副作用。命令从项目实际配置发现；外部网络、数据库、生产资源和真实账号需要相应授权。缺一项只限制对应检查。

## 开始前的最少读取

固定候选和承诺，读取现有原始证据、变更范围及真实检查入口。先判断旧证据对象、版本、环境、入口和覆盖是否仍适用。

## 执行步骤与关键分支

1. 将承诺拆成可由格式/结构、单元、集成、正式入口、安装或行为证据支持的部分。
2. 列出现有证据及范围，比较当前变化是否影响结论；适用则复用并说明理由，失效部分才补验。
3. 选择与风险相称的最小检查集合，不用总分或大量低层检查抵消核心缺口。
4. 直接执行前说明命令、环境和可能副作用；记录退出码、关键输出和生成对象。
5. 失败先区分产品、测试设置、环境与权限；只有识别出瞬时原因或设置修复才重试。
6. 候选在运行后变化时判断哪些证据失效；本技能不默认修改候选。
7. 对照承诺分别报告 `pass`、`fail`、`blocked`、`not-run`、`not-applicable` 及未覆盖内容。

## 按条件加载的本地资源

| 触发条件 | 文件 | 使用目的 |
| --- | --- | --- |
| 选择证据类型与强度 | [验证选择](references/verification-selection.md) | 将承诺映射到判别检查 |
| 执行、重试或回读证据 | [验证执行](references/verification-execution.md) | 固定候选并处理失败 |
| 复用或审计已有证据 | [证据规则](references/evidence-rules.md) | 判断变化影响与结论层级 |
| 涉及外部副作用 | [共同操作边界](references/common-rules.md) | 核对授权与停止位置 |

## 输出与完成条件

输出检查对象、候选、来源/环境、执行或复用内容、逐项结果、覆盖和未覆盖部分。证据足以支持本次承诺时完成；只读审计不执行命令；环境阻塞按项报告。结构正确不等于宿主行为或 Agent 效果正确。

## 异常与停止边界

失败保留原始结果，不降低断言或修代码制造通过。没有运行的命令不得写成通过。验证不自动产生独立审查、验收、合并、发布或关闭授权。

## 简短输入输出示例

正常：候选只改 Markdown 资源，复用未受影响的单元证据，执行资源链接与装配检查，明确宿主安装未覆盖。

边界：安装检查因无宿主权限未启动，报告 `blocked`，不把结构检查称为安装通过。
