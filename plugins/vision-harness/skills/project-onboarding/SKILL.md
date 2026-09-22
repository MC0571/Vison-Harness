---
name: project-onboarding
description: Use when a new, existing, or partially adopting project needs its real adoption gaps identified and the smallest authorized integration applied. Reuses equivalent project facts and returns a usable entry or a justified no-change result, not a new document suite.
license: MIT
---

# Vision-Harhess: Project Onboarding

交付可使用的最小接入：已有权威入口、真实缺口、实际改动或零改动、命令来源与加载限制。

## 何时使用／何时不使用

用于新项目、既有项目或局部采用。明确实施任务且现有上下文充分时直接工作，不先接入全套方法。

## 输入与开始前的最少读取

固定目标目录、采用哪种工作能力和允许写入范围。按本次能力定位目标、工作项、语义约定、Agent 指引和命令；不因这些类别存在就全部要求补齐。命令从实际 manifest、脚本、Makefile、CI 与维护说明核对。

## 工作方法

1. 按事实职责而非文件名检查现状：谁维护什么、从哪里读、何时生效。
2. 区分已满足、只缺导航、缺可执行规则、缺关键输入、来源冲突和工具不可用。等价材料直接复用，不能仅因名称或标题不同判定缺失。
3. 来源冲突先比较对象、范围、版本和有效决定；不要机械宣布 CI、最新文档或最长文件永远获胜。
4. 为每个真实缺口选择最小修正。只缺入口就补入口，不复制已存在的规则；关键产品取舍缺失则只暂停依赖它的接入。
5. 在授权内完整读取、最小修改、保留无关内容、写后回读。宿主专用配置必须核对实际支持，不修改全局信任、凭据或权限。
6. 从实际工作目录走读本次能力所需入口，区分文件存在、可手读和宿主实际加载。再次运行无新事实时零写入。

## 按条件加载的本地资源

| 条件 | 文件 | 用途 |
| --- | --- | --- |
| 判断现有材料是否等价、冲突或缺失 | [采用缺口](references/adoption-gap.md) | 按职责接入而非按文件套餐接入 |
| 发现命令、规则与加载入口 | [工具与指引](references/tooling-and-instructions.md) | 核对项目实际配置 |
| 修改文件或共享事实 | [共同操作边界](references/common-rules.md) | 授权、并发保护与回读 |

## 输出与完成条件

说明已满足入口、缺口及影响、实际修改、命令来源和剩余限制。当前采用能力已有可定位的输入和必要规则即可完成；无必要修改是正常结果。未访问 GitHub 不等于没有工作项，本地文件完成也不等于宿主接入完成。

## 停止与例外

缺一个外部工具只限制对应部分，不创建平行 tasks 或状态数据库。既有布局可用就保留；不要求用户为已授权的局部可逆修改逐项重新确认。

## 示例

项目以 `docs/product.md` 维护目标、CI 提供测试命令，只缺 Agent 找到它们的入口：补一处导航，不另建 VISION/ARCHITECTURE/Spec 套餐。若 README 与 CI 使用不同测试配置，先辨认本地开发与发布检查的不同职责，不直接删除其中一个。
