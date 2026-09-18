# Vision Harness Method

这份文档记录 Vision Harness 的完整方法规则。它主要服务于实现 Vision Harness 的 Agent、维护者，以及需要理解其判断逻辑的使用者。

如果只是想知道 Vision Harness 是什么、怎么使用，请先阅读 [README.md](README.md)。项目为什么存在见 [VISION.md](VISION.md)。

---

## 1. 先看清整体，再做眼前工作

Coding Agent 很容易把当前上下文中可见的目标，当成整个系统的目标。Vision Harness 要求在深入实现之前，先建立足够完整的目标状态和主要结构。

“完整”不是要求提前确定所有细节，也不是消灭未知。它意味着：

- 已经明确属于最终目标的主要能力不能因为暂时不做而消失；
- 已确认的目标、待验证的假设和尚未解决的问题要分开；
- 远期工作可以只保留粗粒度，近期工作才逐步细化；
- 实现细节只在接近执行时确定。

因此，当前 Scope 可以小，但完整目标必须保持可见。

任何已经确认属于目标状态、但当前不实施的工作，都必须有可追踪的位置。不能只留下“以后支持”“后续优化”“future improvement”这类自然语言备注。

---

## 2. 每一种事实只维护一个地方

Vision Harness 不靠同步多份文档保持一致，而是给不同事实指定唯一来源。

| 事实 | 维护位置 |
| --- | --- |
| 项目长期目标 | `VISION.md` |
| Roadmap、Milestone、优先级、Owner、工作状态 | GitHub |
| Initiative / Capability / Feature / Deferred Work | GitHub Issues |
| 父子工作、依赖关系 | GitHub Issue relationships |
| 系统长期行为和约束 | Specs |
| 当前长期架构 | `ARCHITECTURE.md` 或 architecture docs |
| 重要长期设计决策的原因 | ADR |
| 一次变更的实施方案 | GitHub Technical Plan |
| 执行任务 | GitHub Sub-issues |
| 当前实现 | Code |
| 可执行保证 | Tests / Schemas / Contracts |

Repository 保存长期系统事实；GitHub 保存动态工作事实。

不要维护 `ROADMAP.md`、`tasks.md` 或其他与 GitHub 平行的镜像。需要关联时使用引用，不复制一份再同步。

---

## 3. GitHub Work Graph 如何工作

这里的 Work Graph 指 GitHub 中由 Milestones、父子 Issues、依赖和 Deferred Work 组成的工作结构。

它不只是“待办列表”，还要让 Agent 看见系统主要能力及其关系。

高层规划优先保证 breadth：主要 Milestones 和 Capabilities 应尽早可见。越接近执行，才增加 detail。远期 Capability 没有必要提前拆成数据库迁移、API 修改或测试文件等具体任务。

Issue 可以代表一个尚未马上实施、但已经确认属于目标状态的能力。是否现在执行，由 Milestone、Priority、Status 等动态信息决定。

当新的事实出现时，Work Graph 可以重排、拆分、合并或删除。规划是当前最佳认知，不是不可修改的承诺。

---

## 4. Issue 写什么，Spec 写什么

Issue 是工作的生命周期容器，主要回答：

- 为什么这项工作存在；
- 它在整体目标中的位置；
- 完整目标状态包含哪些能力；
- 本次准备推进哪些内容；
- 哪些内容明确不属于这里；
- 依赖谁、影响谁；
- 哪些已知能力暂不做；
- 对应的长期规格在哪里；
- 满足什么条件后这项工作可以关闭。

Spec 不负责项目状态和工作排序。Spec 精确定义系统必须满足的行为和约束。

因此，范围决策属于 GitHub Work Graph；Spec 定义该范围触碰到的长期系统语义。Tests 用来证明实现是否满足这些要求，但不能反过来决定本次应该交付什么。

Issue 的关闭条件回答“这项工作能不能结束”；Spec 的验收条件回答“系统行为是否正确”。两者不要复制。

---

## 5. Spec 不是固定的一份文件

Spec 是长期系统语义的集合，不等于每个 Issue 都创建一份 `spec.md`，也不要求每套 Spec 拥有相同文件。

一次变化可能触碰的规格对象包括：

| 变化 | 常见规格对象 |
| --- | --- |
| 用户或系统行为 | behavioral spec |
| 状态和生命周期 | state model |
| 长期领域数据语义 | domain data semantics |
| API / event / protocol | machine-readable contract |
| 权限规则 | authorization semantics |
| 安全保证 | security guarantees |
| 兼容要求 | compatibility guarantees |
| 必须满足的性能、可用性等性质 | non-functional requirements |

执行时先问：Current Scope 改变了哪些长期保证？

对每个被改变的保证，再判断已有规格是否足够；如果没有，决定是放进现有 spec，还是创建一个值得独立维护的规格对象。

只有具备独立验证、独立复用或独立演进价值的语义，才值得拆成独立 Spec Object。不要为了凑模板生成 `data-model.md`、`security.md` 等文件。

Spec 是否完整，不看文件是否齐全，而看 Current Scope 中所有需要长期保证的语义是否都有明确、唯一、可验证的表达。

Spec 目录使用稳定的语义名称，例如：

```text
specs/
├── execution-engine/
│   ├── spec.md
│   ├── state-model.md
│   └── contracts/
│       └── run-api.yaml
├── authorization/
│   └── spec.md
└── evaluation/
    └── spec.md
```

不要使用 Issue 编号、创建顺序或临时阶段作为目录身份。

Spec 文件不保存 Owner、Milestone、Status、Accepted At 等工作流状态。只有系统语义改变时，Spec 才应该产生 diff。

---

## 6. Spec、Code 和 Tests 的关系

验收前，Spec 是实现必须满足的规范；Code 是待验证的实现。

验收后：

- Code 表达系统当前实际上怎么运行；
- Tests、Schemas、Contracts 表达能够自动验证的保证；
- Spec 保留稳定的行为语义和长期约束。

代码中已经存在的行为不一定是正确行为。Bug 不能因为“代码就是这样跑的”就自动变成新的规范。

另一方面，Spec 也不应该长期复制实现细节。内部类结构、缓存方式、数据库索引、具体调用顺序等，应该由 Code 表达。

当一次代码变化改变了对外行为、状态语义、错误规则、权限、安全保证、兼容性等长期承诺时，需要重新进入 Spec 判断。纯内部重构或不改变语义的实现优化通常不需要。

---

## 7. Architecture、ADR 和 Technical Plan

三者分别解决不同问题。

**Architecture** 记录系统长期如何组织，例如 subsystem 边界、依赖方向、数据 ownership、跨组件协议、trust boundary、extension point 和部署关系。它描述稳定结构，不复制当前类和文件结构。

**ADR** 记录一个重要长期决定为什么这样做。只有当存在真实备选方案、明显 trade-off、未来修改成本较高，而且决定会约束后续工作时，才值得写 ADR。讨论阶段留在 GitHub；真正决定后再记录。旧决定被替代时，新 ADR 说明替代关系，旧 ADR 保留历史。

**Technical Plan** 只服务一次具体变化，说明如何安全实施，例如受影响组件、变更顺序、迁移、兼容、测试、回滚和风险。它默认留在 GitHub，实施结束后不要求继续与代码同步。

进入实现前，Agent 要判断当前变化是否改变长期架构。如果只是沿用现有架构实现一个功能，可以直接继续；如果改变 subsystem 边界、依赖方向、数据 ownership、protocol、consistency、trust boundary、deployment topology 或长期扩展模型，则先处理架构问题，必要时形成 ADR。

---

## 8. TDD 如何融入

TDD 是实现方法，不负责发现完整 Scope。

外层由 Issue 的 Current Scope 和相关 Spec 决定本次必须满足哪些行为；内层再按 behavioral slice 执行 Red → Green → Refactor。

例如“给 Run 增加 timeout”可以按用户或系统可观察行为拆：

```text
Slice 1: running Run 到期后进入 timed_out
Slice 2: timed_out Run 拒绝 late success result
Slice 3: timeout 状态能够被正确持久化和重新读取
```

不要按“先建数据库、再写 service、再写 API、最后补测试”来拆。

每个 slice 中，允许只写使当前测试通过的最小代码。这里的“最小”只针对实现，不代表可以缩小已经明确的完整目标。

Refactor 阶段除了代码质量，还要检查：当前结构是否符合 Architecture，是否产生重复概念或意外接口，是否为了当前 slice 阻碍了已知目标，以及是否借“未来需求”之名提前实现了 Deferred Work。

Tests 全绿不等于工作完成。结束前还要回到 Current Scope 和 Spec，确认没有遗漏行为，并执行必要的质量验证。

---

## 9. 质量检查按变化触发

不是每个 Feature 都机械执行所有检查。

Agent 应根据变化判断是否需要 Security、Reliability、Performance、Compatibility、Observability、Migration 等专项验证。

同样，不要求每条 Spec 都必须对应一个普通自动化测试。一个长期保证可以通过 Test、Schema、Type、Static Analysis、Benchmark、Runtime Assertion 或必要的人工验证来证明。

关键问题不是“有没有生成测试文件”，而是：

> 当前承诺的每一项长期保证，是否都有合适的验证证据？

---

## 10. 什么时候允许继续

Vision Harness 的关键作用之一，是在证据不足时阻止 Agent过早进入下一阶段。

典型判断包括：

- Issue 是否已经说明 Target State、Current Scope、边界和 Deferred；
- Current Scope 涉及的长期语义是否已经被规格覆盖；
- 架构影响是否已经判断，必要设计是否完成；
- 是否已经具备安全实施所需的计划和依赖；
- 实现和必要质量验证是否完成；
- 结束工作前，Current Scope 是否重新逐项核对；
- Milestone 或长期开发过程中，系统是否仍然朝 Vision 收敛。

这些判断不需要生成新的状态文档。

判断必须基于当前变化对应的可核验证据。证据缺失、互相冲突或无法验证时，不能默认通过，也不能为了通过而静默缩小 Scope、降低质量要求或修改验收条件。

目标、范围和质量承诺的变化必须有明确依据，执行 Agent 不能为了完成当前任务自行改写。

---

## 11. 三个持续循环

Vision Harness 不是一条只从 Vision 走到 Code 的流水线，而是三个相互连接的循环。

### Strategic Loop

持续检查 GitHub 中的 Milestones 和 Issues 是否仍然覆盖 Vision。生产、使用、研究或新的项目事实出现后，可以重新规划，而不是机械执行旧计划。

### Delivery Loop

对当前工作执行 Issue shaping、Spec 判断、Architecture 判断、Technical Plan、behavioral slicing、TDD 和质量验证，直到本次承诺被完整实现。

### Convergence Loop

周期性从系统整体检查：Code 是否仍符合 Architecture，不同 Specs 是否冲突或重复，Deferred 是否已经失效或积累成系统缺口，Work Graph 是否仍反映真实认知，以及当前系统和 Vision 之间最大的差距是否发生变化。

完成一个 Feature 只是局部闭环，不代表上层假设已经被证明正确。行为验收、交付结果和目标效果要分开看，后续 Evidence 应能够反向修改 Work Graph、Spec、Architecture，必要时也可以修正对 Vision 的解释。

---

## 12. 执行必须基于当前状态

Vision Harness 不要求 Agent 每次从第一步重新走完整流程。

Agent 应读取 canonical sources，判断项目和当前 Issue 已经具备什么、缺什么，然后只执行下一步真正需要的方法。

在相同事实和相同意图下，重复执行同一方法不应产生重复 Issue、重复文档或无意义 diff。当事实或决策变化时，则允许有依据地更新、拆分、合并或删除旧工作。

Vision Harness 自身不能创建权威的 `state.yaml`、`progress.json`、Roadmap store 或其他平行状态系统。状态从 GitHub、Repository、Code、Tests 和 CI 中读取。

---

## 13. Vision Harness 自身也必须被验证

Vision Harness 不是靠“方法看起来合理”证明有效。

Agent 行为评估应覆盖真实和失败场景，例如：

- Target State 尚未建立时，Agent 是否会拒绝直接滑向“先做一个简单版本”；
- Agent 声明某项能力 Deferred 时，是否会给它留下可追踪位置；
- Tests 全绿但 Spec 仍有遗漏时，Agent 是否会识别为未完成；
- 变化触及长期架构边界时，Agent 是否会进入架构判断；
- 新 Session 是否能从项目事实恢复完整上下文；
- 重复执行方法时，是否避免制造重复事实；
- 证据不足时，是否会明确缺口而不是自行宣布通过。

评估关注实际决策、操作和结果，而不只检查 Skill 是否加载、文档是否生成或 Agent 是否口头声称遵守流程。
