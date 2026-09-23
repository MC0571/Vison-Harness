---
name: agent-instructions
description: Use when project Agent guidance, review rules, or host execution configuration needs a scoped improvement. Turns durable project differences into trigger-action-boundary instructions, reuses canonical sources, and distinguishes file existence, loading, and actual review outcomes.
---

# Vision-Harness: Agent Instructions

交付必要、可执行的项目 Agent 指引或审查/宿主配置，并说明真实加载与权限边界。

## 何时使用／何时不使用

项目指引与审查/宿主配置是两类工作。只有真实缺口才修改，不为每级目录铺设 AGENTS，也不默认配置三名 reviewer。普通代码或 Spec 审查不是本技能职责。

## 输入与开始前的最少读取

固定项目、宿主、工作目录、规则适用范围和授权。读取根/相关局部规则、既有审查依据、实际配置与命令。宿主格式和优先级从现行官方资料或可信本地配置核对，不靠文件名猜自动加载。

## 工作方法

1. 区分缺规则、缺准确引用、缺宿主执行入口、规则冲突或其实无需修改。
2. 判断内容是否值得长期写入：稳定项目差异与安全/协作边界可保留，一次任务进度、临时选择和可由工具自动发现的重复信息不升成全局规则。
3. 将空泛建议写成触发条件、动作、适用范围/例外和完成边界。每项新增规则都应说明防什么具体错误，不能只增加“必须更完整”。
4. 根规则放全仓约定，局部规则只放差异；已有 Spec、架构和审查标准引用而不复制，没有局部差异就不新建。
5. 审查配置先明确判断对象、依据、finding 与只读边界，再选择宿主入口；按真实格式创建，不把 Markdown 当 TOML，也不假定角色名等于权限隔离。
6. 在授权内最小修改，保留有效安全与审查约束。回读并尽可能从实际工作目录核对加载、覆盖与引用，区分存在、可手读、实际加载和真正执行结果。

## 按条件加载的本地资源

| 条件 | 文件 | 用途 |
| --- | --- | --- |
| 判断规则是否值得写、如何写与分层 | [项目指引](references/project-instructions.md) | 可执行规则与权威引用 |
| 审查规则或宿主入口配置 | [Reviewer 配置](references/reviewer-configuration.md) | 规则、角色、权限与加载 |
| 写入或全局权限边界 | [共同操作边界](references/common-rules.md) | 安全修改与授权 |

## 输出与完成条件

说明真实缺口、修改、保留内容、命令/格式来源、加载事实和未验证部分。只读建议与零修改是正常结果。宿主格式无法核对时可交付通用规则，但配置受阻；不能将文件生成称为已完成独立审查。

## 停止与例外

不改全局配置、信任、凭据或 Hook 绕过问题。不能为当前 PR 通过而降低标准；局部差异不自动授权削弱上级安全边界。规则足够时结束，不将一次故障固化成所有未来任务的新审批。

## 示例

“认真测试”改为“修改该解析器时运行项目已有边界测试；新增编码输入时补对应回归，环境失败如实说明，不跳过断言”。命令已有权威来源就引用，不再次复制。临时热修复步骤留在工作项，不写入全仓永久规则。
