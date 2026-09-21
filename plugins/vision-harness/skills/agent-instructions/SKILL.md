---
name: agent-instructions
description: Use when project Agent instructions, review rules, or host reviewer/sub-agent configuration need to be created, corrected, or minimized. Returns scoped files and verified loading facts; it does not assume a filename is auto-loaded or weaken constraints to pass current work.
license: MIT
---

# Agent Instructions

交付必要的项目 Agent 指引或审查/宿主配置，以及文件存在、可读取、实际加载和独立审查之间的准确边界。

## 何时使用／何时不使用

两种模式：项目 Agent 指引；审查规则与宿主执行配置。只有真实缺口才修改，不为每层目录铺设 AGENTS，也不默认配置三名 reviewer。普通代码或 Spec 审查不属于本技能。

## 输入与环境条件

需要目标项目、真实宿主、目标工作目录和允许修改范围。宿主格式从其现行官方资料/本地配置核对；无法核对时只完成通用规则，不制造未知配置。全局权限、信任、凭据和 Hook 不在默认范围。

## 开始前的最少读取

读取根与目标目录适用的局部规则、现有审查规范、CI/宿主配置和真实命令来源。确认宿主的加载位置与优先级，不能从文件名推断自动加载。

## 执行步骤与关键分支

1. 固定项目、宿主、配置范围和授权。
2. 区分缺审查/工作规则、缺权威引用、缺宿主执行入口或其实无需修改。
3. 项目指引：根文件放全仓约定，局部文件只放差异；已有 Spec/架构/安全规则引用而不复制；无局部差异不建文件。
4. 审查配置：先写清需要的审查结果和规则，再核对宿主真实配置格式；只有本次需要才创建具体入口，不把 Markdown 假扮 TOML/YAML。
5. 在授权内最小修改，保留原有安全、权限与审查约束；不为当前 PR 通过而降低标准。
6. 回读文件并尽可能用宿主只读能力确认加载；分别报告存在、可手读、实际加载和是否产生独立审查结果。

## 按条件加载的本地资源

| 触发条件 | 文件 | 使用目的 |
| --- | --- | --- |
| 创建或调整项目/局部指引 | [项目指引](references/project-instructions.md) | 选择层级并复用权威规则 |
| 配置审查规则或宿主入口 | [Reviewer 配置](references/reviewer-configuration.md) | 区分规则、引用和执行入口 |
| 涉及写入或全局边界 | [共同操作边界](references/common-rules.md) | 防止权限与范围扩张 |

## 输出与完成条件

输出修改范围、保留的原规则、真实命令来源、加载事实和未验证项。只读请求给最小建议；已有配置足够时零修改；无官方格式资料时通用规则可完成而宿主入口标为受阻。配置成功不等于候选已独立审查通过。

## 异常与停止边界

不改全局配置、权限、信任、凭据或 Hook 绕过问题。局部文件不能削弱上级安全约束。未经授权不修改其他项目或启动审查/实施。

## 简短输入输出示例

正常：根规则已有安全边界，某子目录只需补特有测试命令；新增一份局部差异并验证宿主加载层级。

边界：用户要 reviewer 配置但宿主格式无法核对；交付通用审查规则，明确执行配置未创建。
