---
name: project-onboarding
description: 按真实缺口帮助新项目或既有项目采用 Vision Harness，复用已有事实与布局，只做获准的最少接入修改。
---

# Project Onboarding

交付项目采用差距判断，以及明确授权下最少必要的接入修改。它不是模板生成器，也不要求项目重建目录或重新写一套愿景。

## 核心过程

1. 确认目标项目、宿主、允许修改范围和停止位置。
2. 读取现有愿景/等价入口、规划来源、适用 AGENTS.md、Spec/架构入口和真实构建测试配置。
3. 区分“文件存在”“Agent 可手动读取”“宿主会自动加载”。新会话恢复、组织级事实或加载规则不清时，读取[项目上下文行为约定](../../references/project-context-behavior.md)。
4. 逐项判断哪些已经足够、哪些缺口实际影响本次使用。缺少愿景交给 vision-management；缺少规划交给 breakdown；缺少 Agent/审查配置交给 agent-instructions。
5. 只要求评估时零写入；获准修改时完整读取目标、保留无关内容、写后回读。

涉及授权、安全写入或“是否已经足够”的判断时读取[共享规则](../../references/shared-rules.md#1-先确认本轮任务和授权)。涉及 AGENTS/审查入口具体维护时再读取[Agent 配置方法](../../references/agent-config-methods.md#6-维护-agent-工作约定和审查规则)。

## 不应发生

不要创建平行 VISION、ROADMAP、状态库或固定审查文件套餐；不要猜测不存在的命令；安装/更新方法包不得覆盖消费项目愿景、规则、规划、自定义配置或代码。

结束时说明复用内容、真实缺口、实际写入/零写入结果、仍未验证的宿主加载事实及下一直接入口。
