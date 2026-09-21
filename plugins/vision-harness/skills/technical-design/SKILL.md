---
name: technical-design
description: Use when a confirmed behavior change needs an implementation path, architecture-impact decision, bounded investigation, or durable ADR. Returns an existing-architecture reuse decision or targeted design; it does not invent product requirements or create ADRs for simple changes.
license: MIT
---

# Technical Design

交付“沿用或调整架构”的结论、选择依据、当前实施路径、必要长期记录和未决项。

## 何时使用／何时不使用

用于跨模块边界、依赖方向、数据所有权、协议、一致性、信任或部署变化，或实施前确有重要技术取舍。现有结构能直接承载的简单变化给出沿用结论，不制造方案竞赛或 ADR。

## 输入与环境条件

需要已确认行为、现有架构和相关代码/配置。产品取舍不能由技术偏好代替；可查技术事实自行查。一次方案默认记录在授权的现有工作载体，不自动新建 `plan.md`。

## 开始前的最少读取

读取受影响行为约定、当前架构边界、真实入口和依赖方向；查看足够的调用/数据流以判断影响，不做无关全仓设计审查。

## 执行步骤与关键分支

1. 检查模块边界、依赖方向、数据所有权、协议、一致性、信任和部署是否变化。
2. 若不变化，指出复用的现有结构和局部实施路径后停止架构扩展。
3. 若变化，明确约束和受影响组件；只比较真实可行且会改变选择的方案，不为形式制造三个选项。
4. 会推翻路线的未知使用有界调查：先固定观察量、预算、停止条件与判据；环境失败不等于路线失败。
5. 选定方案后写变更顺序、兼容/迁移、验证与回滚条件，并检查推测性抽象或多余兼容。
6. 只有真实权衡已决定且长期影响多个后续工作时记录 ADR；未决定内容留在讨论。替代旧决定时保留历史并更新当前架构。

## 按条件加载的本地资源

| 触发条件 | 文件 | 使用目的 |
| --- | --- | --- |
| 判断结构边界是否变化 | [架构影响](references/architecture-impact.md) | 确定沿用或调整 |
| 形成当前实施方案 | [变更设计](references/change-design.md) | 说明组件、顺序、迁移与验证 |
| 判断是否需要 ADR | [决策记录](references/decision-records.md) | 区分结构、讨论与重大决定 |
| 关键未知会推翻路线 | [关键假设](references/critical-assumptions.md) | 有界调查而非无限研究 |
| 检查推测性负担 | [复杂度控制](references/complexity-control.md) | 保留保护并删除无依据复杂度 |
| 涉及写入与授权 | [共同操作边界](references/common-rules.md) | 安全修改长期事实 |

## 输出与完成条件

输出沿用/调整架构结论、选择与依据、当前技术方案、必要长期记录和未决项。无需 ADR、无需架构修改或只读方案都是正常结果；调查受阻时只限制依赖它的选择。

## 异常与停止边界

技术选择不擅自变成产品需求。未授权不改架构/ADR/工作项，不启动实现、合并或发布。无法确定关键产品行为时暂停相应设计并明确需要的决定。

## 简短输入输出示例

正常：新状态跨服务持久化，设计明确所有权、协议版本、迁移顺序、回滚和集成验证，并记录真正长期权衡。

边界：只给现有模块增加一个局部分支，输出沿用架构和文件级实施路径，不创建 ADR。
