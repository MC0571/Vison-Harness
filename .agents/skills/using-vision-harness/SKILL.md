---
name: using-vision-harness
description: 识别当前用户工作、恢复最少必要事实与授权，并选择一个直接工作入口；不充当强制路由器、调度器或权限授予者。
---

# Using Vision Harness

负责把“这次到底要做什么”识别清楚，并把范围、来源、授权和停止位置交给一个合适的工作入口。用户已经直接调用明确入口且条件足够时，不必先经过这里。

## 使用与边界

用于新请求、新会话或任务类型不清楚时。它只做识别与有界接续，不替代愿景、规划、实施、审查、验证或交付，也不因工具可写、Issue 状态或 CI 结果扩大授权。

新会话、来源冲突、持续授权或消费项目/方法包容易混淆时，读取[项目上下文行为约定](../../../specs/project-context/spec.md)。涉及写入、完成层级或治理充分性时，读取[共享规则](../../../METHOD.md#1-先确认本轮任务和授权)。

## 执行骨架

1. 确认目标项目、当前请求、用户要求的结果和停止边界。
2. 读取只足以支持这次选择的权威事实；区分确认决定、建议、假设、未知、证据、暂缓内容和授权。
3. 从下表选择最小工作入口。缺少已安装入口时报告限制，不假称已经执行。
4. 交出本轮范围、实际来源/版本、允许副作用、仍缺的关键事实和返回条件，然后结束本入口职责。

| 用户直接请求的工作 | 入口 |
| --- | --- |
| 新项目或既有项目接入 | [project-onboarding](../project-onboarding/SKILL.md) |
| 形成、检查或维护愿景 | [vision-management](../vision-management/SKILL.md) |
| 全景拆解、单项整理、依赖/并行与滚动细化 | [breakdown](../breakdown/SKILL.md) |
| 建立或修改长期行为 Spec | [spec-development](../spec-development/SKILL.md) |
| 技术设计、架构影响、ADR 与实施方案 | [technical-design](../technical-design/SKILL.md) |
| 实施明确变更、定位或修复缺陷 | [tdd-development](../tdd-development/SKILL.md) |
| 审查 Spec、代码或 PR | [review](../review/SKILL.md) |
| 获取、复用或审计变更证据 | [change-verification](../change-verification/SKILL.md) |
| 打包、PR/合并、发布或工作收尾 | [release-delivery](../release-delivery/SKILL.md) |
| 系统级偏离、重复或长期收敛 | [project-convergence](../project-convergence/SKILL.md) |
| AGENTS、审查规则或宿主 Agent 配置 | [agent-instructions](../agent-instructions/SKILL.md) |

直接调用任何工作入口都有效；各入口仍核对自己的依据与授权。条件已经足够时继续，不为了“完整流程”补跑其他入口。
