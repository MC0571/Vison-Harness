---
name: release-delivery
description: Use when a package, pull request, merge, release, or work closure must be completed under explicit authorization. Executes only the requested delivery action with candidate and evidence checks; one action never grants permission for the next.
license: MIT
---

# Release Delivery

交付用户明确指定的打包、PR、合并、发布或关闭动作，并分别报告其真实结果。

## 何时使用／何时不使用

五类动作彼此独立，不组成默认顺序。创建 PR 不授权合并，构建成功不授权发布，合并不自动授权关闭长期事项。只要求状态报告时保持只读。

## 输入与环境条件

需要交付对象、准确候选、目标环境及该动作的明确授权。命令来自真实项目配置；凭据可用不等于获准使用。缺少推送/发布能力时保留本地结果并准确报告。

## 开始前的最少读取

确认分支、head、base、工作区、远端和已有等价 PR/构件；读取正式构建/发布入口、适用证据和当前授权。检查原构件时先保存其身份，不能先重建再声称原对象通过。

## 执行步骤与关键分支

1. 固定本轮只执行哪些动作及停止位置。
2. 打包：从配置识别正式构件；运行正式入口；检查生成文件、依赖、权限、敏感信息并记录构件标识。
3. PR：核对分支/base/head/范围和已有等价 PR，保留工作区；获准后创建或更新，结果不明先查询。
4. 合并：只有明确授权才执行；重读最新 head/base、冲突、要求和证据，使用宿主条件能力；合并后回读实际目标分支，不假设固定叫 `main`。
5. 发布：确认对象、版本、许可和目标；按真实命令执行并回读，不用“应该上线”代替结果。
6. 关闭：区分切片、PR、阶段和长期能力。需要合并后验证的事项使用普通关联并在验证后单独关闭。
7. 每一步都核对候选与证据，不硬依赖其他 Skill 存在；超出授权即停止。

## 按条件加载的本地资源

| 触发条件 | 文件 | 使用目的 |
| --- | --- | --- |
| 构建或检查交付包 | [构件交付](references/package-delivery.md) | 保留原对象身份并检查包内容 |
| 创建/更新 PR 或合并 | [PR 与合并](references/pr-and-merge.md) | 核对分支、条件与远端结果 |
| 发布或关闭工作 | [发布与关闭](references/release-and-close.md) | 分开版本、副作用和完成层级 |
| 核验证据适用范围 | [证据规则](references/evidence-rules.md) | 防止旧证据外推 |
| 核对授权和结果不明 | [共同操作边界](references/common-rules.md) | 安全执行外部写入 |

## 输出与完成条件

输出实际构件/入口、候选或版本、已执行动作、每项结果、限制和未执行动作。只读请求给状态；无新增动作时零写入；环境受阻时给本地提交/构件标识。只有用户指定动作真实发生并回读才称其完成。

## 异常与停止边界

响应未知先查询，不重复 PR/发布。未经明确授权不合并、发布、部署、打 tag、创建 Release 或关闭事项。不修改保护、凭据和全局配置绕过限制。

## 简短输入输出示例

正常：用户授权“提交、推送、开 PR，不合并”。完成三项并返回 SHA/URL，到合并边界停止。

边界：构建通过但未授权发布，报告构件及检查，发布为未执行。
