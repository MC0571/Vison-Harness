---
name: release-delivery
description: Use for an explicitly authorized package, PR, merge, release, deployment, or work closure. Applies action-specific checks, observes actual outcomes, and handles partial success with bounded recovery; building, merging, publishing, and closing never automatically authorize each other.
license: MIT
---

# Vision-Harness: Release Delivery

完成本轮明确授权的交付动作，分别说明真实结果、失败或部分成功。动作不是默认流水线。

## 何时使用／何时不使用

打包、PR、合并、发布/部署和关闭可独立请求。只报告状态就只读。创建 PR 不授权合并，构建不授权发布，合并不自动关闭长期能力。

## 输入与开始前的最少读取

固定交付对象、准确候选、目标环境、允许动作与停止位置。核对工作区、分支/head/base、远端、等价 PR/构件及真实命令来源。验证已有包先记录其身份，不能先重建覆盖原对象。

## 工作方法

1. 将本轮动作与完成层级说清，检查凭据用途与权限；已有明确授权范围内连续推进。
2. 打包使用正式本地入口，核对内容、依赖、许可证、执行位和敏感信息，记录构件标识；不把打包命令中的远端发布副作用当默认许可。
3. PR 先核对分支、base/head、范围和等价对象，再在授权内创建或更新；正文区分实际检查与计划。
4. 合并前重读 head/base、冲突、必要检查与审查，使用可用的期望候选条件；合并后读取实际目标分支，不能假设固定叫 main。
5. 发布/部署按对象选择方法：构件发布核对版本与内容；有生产运行影响时，按真实风险明确推进、健康判断、停止与恢复条件，不套固定比例或观察时长。
6. 遇到超时或部分成功，先分清已发生、未发生与未知的效果，查询并保留成功产物，再决定获准的补做、暂停、回退或向前修复。不盲目重复整个流程。
7. 关闭前核对相应切片/阶段/长期能力承诺与后置条件。需合并后验证时避免自动关闭关键词，验证后在关闭授权内单独关闭。
8. 分项回读与报告，到本轮未授权边界停止；不依赖其他 Skill 安装才能承担自己的候选与结果核对。

## 按条件加载的本地资源

| 条件 | 文件 | 用途 |
| --- | --- | --- |
| 构建或检查包 | [构件交付](references/package-delivery.md) | 原对象身份与包内容 |
| 创建/更新 PR、合并 | [PR 与合并](references/pr-and-merge.md) | 候选、平台条件与回读 |
| 发布、部署、部分失败或关闭 | [发布与关闭](references/release-and-close.md) | 推进信号、恢复与完成层级 |
| 核对旧证据和当前结论 | [证据规则](references/evidence-rules.md) | 影响判断与继承 |
| 副作用、未知结果和权限 | [共同操作边界](references/common-rules.md) | 安全操作 |

## 输出与完成条件

报告构件/PR/版本/目标提交、已执行动作、各项结果、未执行部分与限制。只在用户要求的动作真实发生并必要回读后称完成；“上传成功但部署未完成”必须分开。长期观察未执行时不虚构已监控。

## 停止与例外

不修改保护、全局配置、信任或凭据绕过限制。未授权不部署、打 tag、创建 Release 或关闭事项。恢复可能产生新高影响副作用时核对授权；保留已完成结果，不把失败描述成全盘失败或全面成功。

## 示例

获准提交、推送、开 PR：完成并返回 SHA/PR，未授权合并则停。构件已上传、Release 创建失败：先验证构件身份和 Release 是否实际存在，仅在原权限内补缺动作，不重建并覆盖已发布版本。
