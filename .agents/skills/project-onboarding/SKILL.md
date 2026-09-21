---
name: project-onboarding
description: Use when a new, existing, or partially adopting project needs its Vision Harness adoption gaps identified and the smallest authorized integration applied. Reuses equivalent project facts and does not rebuild the repository or require global planning first.
license: MIT
---

# Project Onboarding

交付项目的真实接入结果：现有入口、缺口分类、实际改动或零改动、可确认命令和剩余限制。

## 何时使用／何时不使用

用于新项目接入、既有项目补齐最少导航/规则，或局部采用一种能力。不用于重建已有项目、强制生成文档套餐或在明确实施请求前重跑愿景和全局规划。

## 输入与环境条件

需要目标目录和期望采用范围。愿景、规格、规则、工作入口和命令从项目读取；采用深度与新增权威载体由用户决定。缺 GitHub 工具时仍可完成本地分析，但不能另建任务数据库或宣称 GitHub 接入完成。

## 开始前的最少读取

读取目标项目已有愿景/产品说明、长期规格与架构入口、根和相关局部规则、工作跟踪入口，以及 manifest、脚本、Makefile、CI 中的真实命令。只读与本次采用范围相关内容。

## 执行步骤与关键分支

1. 明确是新项目、已有项目还是局部采用，并固定允许写入范围。
2. 将现状分类为：已满足、只缺导航、缺规则、缺关键输入、工具不可用；同一项目可有多类。
3. 复用等价材料和现有布局。文件名不同不是缺口，不移动整个目录，也不生成 VISION/ARCHITECTURE/ADR/Spec 套餐。
4. 为每个真实缺口提出最小改动及其作用；复杂 reviewer 配置只在本次明确需要时处理。
5. 只执行已授权的必要变化，完整读取目标、保护无关内容、写后回读。
6. 从实际配置确认可用命令；没有入口时报告缺口，不猜测命令或引入整套工具。
7. 再次运行且无新事实时返回零写入。

## 按条件加载的本地资源

| 触发条件 | 文件 | 使用目的 |
| --- | --- | --- |
| 判断新项目、已有项目或局部采用 | [采用缺口](references/adoption-gap.md) | 选择最小接入分支 |
| 查构建命令或规则加载方式 | [工具与指引](references/tooling-and-instructions.md) | 核对真实入口和加载事实 |
| 涉及写入或授权边界 | [共同操作边界](references/common-rules.md) | 安全修改并限定完成层级 |

## 输出与完成条件

正常完成需列出现有入口、真实缺口、实际改动、可确认命令和限制。只读请求给出最小建议；已有条件充分时以零改动完成；外部工具不可用时只将对应接入标为受阻。本地文件完成不等于宿主已自动加载。

## 异常与停止边界

不修改全局 Codex 配置、凭据、信任或其他项目。需要用户决定项目长期目标时暂停该项，不用模板替用户决定。未授权 GitHub 写入时停止在本地结果。

## 简短输入输出示例

正常：已有 README、Spec 和测试脚本，只缺根 AGENTS 导航；获准后增加一处最小导航并回读，报告真实测试命令。

边界：项目已有等价规则但文件名不同，输出“无需修改”，不复制成新套餐。
