# Vision Harness

## 愿景

**让软件项目的 Vision 能够被 AI Coding Agent 有序、高质量、持续收敛地实现。**

Vision Harness 是一套面向 Agent 的软件工程方法论工具。它不替 Agent 决定产品要做什么，也不替项目保存另一套事实；它的职责是让 Agent 在从愿景到代码的整个生命周期中，始终理解完整目标、选择正确的方法、遵守必要的工程边界，并持续验证局部实现是否仍在推动整体 Vision。

Vision Harness 以 Plugin / Skills 的形式融入现有 Coding Agent 工作环境，将方法原则转化为可发现、可执行、可验证的指导与检查，而不建立独立的项目管理平台。

最终，我们希望一个 Agent 在任何时刻进入项目，都能够回答：

- 我们最终想构建什么？
- 当前工作在完整目标中的位置是什么？
- 哪些能力已经实现，哪些明确延期，哪些仍然未知？
- 当前变化需要哪些规格、架构判断和工程验证？
- 什么条件满足后才可以继续进入下一阶段？
- 当前局部实现是否仍与整体系统和 Vision 收敛？

---

## 我们要解决的问题

AI Coding Agent 已经能够快速完成局部软件任务，但它们天然更擅长解决“当前可见的问题”，而不是长期维持完整的软件世界模型。

这种倾向会反复表现为：

- 过早进入“先做一个最简单版本”的实现；
- 把当前切片误认为完整目标；
- 在后续会话中遗忘尚未实现的全景能力；
- 在已有最小实现上持续打补丁，形成局部正确、整体失衡的系统；
- 把测试通过误认为需求已经完整实现；
- 在 Feature 演进中逐渐侵蚀架构边界；
- 让 Issue、文档、计划和代码分别保存同一事实，最终彼此漂移；
- 将“暂不实现”“以后支持”留在自然语言中，最终成为不可追踪的遗忘项。

Vision Harness 的目标不是用更多文档解决这些问题，而是通过一套可执行的方法，让 Agent 的规划、规格化、设计、实现、验证和回顾行为受到一致约束。

---

## 核心理念

### Plan the whole. Detail the next.

在深入实现局部之前，先建立尽可能完整的目标状态和问题空间。

远期工作可以保持较低分辨率，近期工作逐步细化；但当前没有实现的能力不能因此从 Agent 的世界模型中消失。

这里的“完整”以当前 Vision、已知目标和明确边界为依据，并不意味着消灭所有未知。已确认的目标、待验证的假设和尚未解决的问题必须被区分；未知应被显式保留，而不是被 Agent 擅自补成确定需求。探索性工作可以用于降低不确定性，但其结果不能未经正式的规格与验收判断，就被默认视为正式实现。

**完整的是目标和结构，渐进的是实现细节。**

---

### Never lose the deferred.

Deferred 不等于 Missing。

任何已经确认属于目标状态、但当前不实施的工作，都必须存在可追踪的 canonical location。不得以“以后再做”“future improvement”“暂不考虑”等自然语言代替正式的工作节点。

当前 Scope 可以很小，但 Target State 必须保持可见。

---

### One fact, one canonical home.

同一种事实只维护一个权威来源。

Vision Harness 不通过同步多份文档维持一致性，而通过明确事实归属并建立引用关系避免重复：

- Repository 保存长期系统事实；
- GitHub 保存动态工作事实；
- Code 表达当前实际实现；
- Tests、Schemas、Contracts 表达可执行保证。

**Link, don't mirror.**

---

### Scope complete, implementation minimal.

Vision Harness 反对的是 Scope Minimalism，而不是 TDD 中的 Minimal Implementation。

Agent 应先完整理解本次需要满足的系统语义，再针对一个明确的 behavioral slice，以最小实现使其成立。

因此：

- GitHub Work Graph 承载目标展开与本次工作的范围决策；
- Spec 精确定义该范围涉及的系统行为与约束；
- TDD 控制实现增量；
- Tests 证明已实现行为的正确性，但不能反向定义交付范围。

---

### Green is not Done.

测试全部通过只是必要条件。

工作完成前，Agent 必须重新回到 Spec 和 Current Scope，确认没有遗漏任何应当成立的语义，并确认所有必要质量验证已经完成。

**测试不能证明 Agent 没有忘记实现某件事。**

---

### Code is reality, not automatically authority.

验收前，Spec 是规范真理，Code 是待验证实现。

验收后：

- Code 是当前运行现实；
- Tests / Schemas / Contracts 是可执行保证；
- Spec 是稳定的行为语义基线；
- Architecture 是当前长期结构模型；
- ADR 保存重要设计决策的历史原因。

代码中的偶然行为和 Bug 不会因为已经存在，就自动成为新的系统规范。

---

## 完整目标状态

Vision Harness 应覆盖从项目启动到长期演进的完整方法闭环，而不是只解决某一个开发阶段。

### Strategic Loop

确保 Agent 始终在实现正确的整体目标。

它应能够指导 Agent：

- 从 VISION 建立完整的系统 / capability 世界模型；
- 形成并持续维护 GitHub Work Graph；
- 在较高层级优先建立完整 breadth，再滚动提高近期工作的 detail；
- 识别目标状态、Current Scope、Boundaries 与 Deferred Work；
- 检查当前 Milestones / Issues 是否仍然覆盖 Vision；
- 根据新的事实和生产反馈重新规划，而不是机械执行旧计划。

---

### Delivery Loop

确保每一个局部变化都以足够完整和可靠的方式实施。

它应能够指导 Agent：

1. 理解和 shaping 当前 Issue；
2. 判断 Current Scope 触碰了哪些长期系统语义；
3. 按语义覆盖需求选择或创建必要的 Spec Objects；
4. 检查 Spec semantic coverage，而不是机械检查文档套餐；
5. 判断变化是否具有 Architecture Impact；
6. 在需要时进行架构设计，并将真正长期的设计决策记录为 ADR；
7. 对复杂变化形成 Technical Plan；
8. 将实现拆成 behavioral slices，而不是机械的技术层任务；
9. 在每个 slice 内执行 TDD：Red → Green → Refactor；
10. 根据变化触发必要的 Security、Reliability、Performance、Compatibility、Observability、Migration 等质量验证；
11. 在关闭工作前重新检查完整语义覆盖和所有已知 gap；
12. 区分行为验收、交付验证与目标效果验证，并将交付、使用和运行中产生的 Evidence 反馈到相关工作节点与整体规划。

---

### Convergence Loop

确保大量局部正确不会逐渐形成整体错误。

Vision Harness 应能够周期性指导 Agent 检查：

- Code 是否仍符合 Architecture；
- 不同 Specs 是否产生冲突或重复定义；
- Architecture 是否出现 erosion 或 accidental structure；
- Deferred Work 是否仍然有效、是否正在累积成系统性缺口；
- GitHub Work Graph 是否仍然反映真实的系统认知；
- 当前系统与 VISION 之间最大的 gap 是否发生变化。

局部 Feature 的完成不是终点。系统必须持续重新收敛到 Vision。

---

## 事实模型

Vision Harness 自身不建立第二套项目状态数据库，而是读取和操作项目已有的 canonical facts。

### Repository：长期系统事实

典型包括：

- `VISION.md`：项目长期目标；
- Specs：系统必须成立的行为语义；
- `ARCHITECTURE.md` / architecture docs：当前稳定结构；
- ADRs：重要长期设计决策及其原因；
- Code：当前实际实现；
- Tests / Schemas / Contracts：可执行保证。

这些文件只应因为它们代表的系统事实发生变化而改变，而不因为项目管理状态变化而改变。

### GitHub：动态 Work Graph

GitHub 承载：

- Roadmap；
- Milestones；
- Initiatives / Capabilities / Features；
- Parent / Sub-issues；
- Priority / Owner / Status；
- Dependencies；
- Deferred Work；
- Technical Plans；
- PRs 和工作讨论。

Vision Harness 不维护 `ROADMAP.md` 或 `tasks.md` 作为 GitHub 的镜像。

---

## Spec 的角色

Spec 不是固定的一份 `spec.md`，也不是固定的一套文档套餐。

一个 Spec Suite 可以由不同的语义对象构成，例如：

- behavioral specification；
- state model；
- domain data semantics；
- API / event / protocol contracts；
- authorization semantics；
- security guarantees；
- compatibility guarantees；
- 必要的 non-functional requirements。

Agent 应根据本次变化触碰的语义面决定需要哪些 Spec Objects。

**Spec completeness 不等于 artifact completeness。**

Spec 是否完整的判断标准是：

> Current Scope 中所有需要长期保证的系统语义，是否都有唯一、明确、可验证的 canonical representation。

Spec 目录应按稳定的 domain / capability / contract boundary 使用语义名称组织，不使用 Issue 编号、创建顺序或临时实施阶段作为目录身份。

---

## Architecture、ADR 与 Technical Plan

三者承担不同寿命的事实：

- **Architecture**：系统长期如何组织；
- **ADR**：为什么做出一个会长期约束未来工作的设计决策；
- **Technical Plan**：这一次变化具体如何安全实施。

Architecture 只描述长期结构、边界、ownership、dependency direction、data flow、trust boundary 等稳定事实，不成为代码结构的文字镜像。

ADR 是 Decision Record，而不是 Decision Proposal。只有存在真实 alternatives、明显 trade-off、较高变更成本并会约束未来工作的决策，才值得长期记录。

Technical Plan 属于一次工作生命周期，默认由 GitHub 承载；实施结束后无需持续与代码同步。

---

## TDD 的角色

TDD 是实施方法，不是 Scope 发现方法。

Vision Harness 使用两层反馈：

- 外层依据 Issue 的 Current Scope 和相关 Spec，确定本次必须满足的 behavioral guarantees 与 acceptance；
- 内层针对 behavioral slice 执行 Red → Green → Refactor。

Refactor 不只检查代码整洁度，还应检查：

- 是否符合既有 Architecture；
- 是否制造重复概念或 accidental API；
- 是否为了当前 slice 阻断已知 Target State；
- 是否借未来需求之名提前实现 Deferred Work。

**Known future should influence boundaries, not silently expand current scope.**

---

## 方法执行原则

Vision Harness 应当是 **state-aware** 和 **idempotent** 的。

Agent 不应该机械地从流程第一步重新执行，而应该从 canonical sources 判断：

- 当前项目已经具备什么；
- 当前 Issue 已经成熟到什么程度；
- 哪些 Gate 已具备事实依据；
- 当前真正缺少什么；
- 下一步应该使用哪一种方法。

在相同事实和相同意图下，重复执行同一方法不应产生重复节点、重复工件或无意义变更；当事实或决策发生变化时，应有依据地更新、合并、拆分或移除既有工作，而不是机械保留旧结论。

Vision Harness 自身不得创建权威的 `state.yaml`、`progress.json`、Roadmap store 或其他平行状态系统。

---

## Stage Gates

Vision Harness 的价值不仅是给出建议，还在于阻止 Agent 在关键条件未满足时过早进入下一阶段。

典型 Gate 包括：

- Shaping Gate；
- Spec Coverage Gate；
- Architecture Impact Gate；
- Implementation Readiness Gate；
- Quality / Verification Gate；
- Semantic Coverage Gate；
- Vision Coverage / System Convergence Review。

Gate 是判断规则和可验证条件，不是新的状态文档。

Gate 必须依据与当前变更相匹配的可核验证据作出判断。证据缺失、相互冲突或无法验证时，不得默认通过；应明确缺口，并转入调查、补充验证或请求决策。不得通过静默缩小 Current Scope、降低质量要求或修改验收条件来使 Gate 通过。

目标、范围和质量承诺的变更必须依据明确的授权或决策规则，不能由执行 Agent 为完成当前任务自行改写。

---

## Non-goals

Vision Harness **不是**：

- 项目管理平台；
- Issue Tracker；
- Roadmap 数据库；
- Dashboard 或可视化系统；
- 自有 workflow state engine；
- GitHub 的替代品；
- Spec、Issue、Code 之间的同步数据库；
- 强制所有项目生成同一套文档的模板系统；
- 某一种编程语言、框架或软件架构的最佳实践集合；
- 以“MVP”“先做最简单版本”为默认策略的开发方法；
- 一次性把 Vision 自动转换成代码的代码生成器。

它也不追求消灭工程判断。

它的目标是让 Agent 在做判断时拥有完整上下文、正确边界、明确的事实来源和可靠的质量控制回路。

---

## 成功意味着什么

当 Vision Harness 发挥作用时：

- Agent 不会在 Target State 尚未建立时默认滑向“首切”实现；
- 当前实现再小，也能明确看到它属于哪个更大的目标，以及哪些能力仍被 Deferred；
- Deferred Work 不会因为离开当前上下文而消失；
- Issue、Spec、Architecture、ADR、Technical Plan、Tests 与 Code 各自承担明确且唯一的职责；
- Agent 能根据变化实际触碰的语义和风险选择需要的规格与质量机制，而不是机械执行模板；
- Tests 全绿不会掩盖 Spec 覆盖缺失；
- 一系列局部正确的变更不会在缺少整体检查的情况下持续侵蚀系统；
- 新 Agent、新 Session 或新的 Coding Environment 能重新从项目事实中恢复完整的方法上下文；
- 随着实现推进，系统能够通过 Evidence 和 Convergence 不断修正 Work Graph，并持续接近 VISION。

Vision Harness 自身必须接受 Agent 行为评估。评估关注 Agent 在代表性场景和失败场景中的实际决策、操作与结果，而不只检查文档是否生成、Skill 是否加载或 Agent 是否声明遵守流程。方法有效性的判断应建立在可复查的行为证据上。

行为验收、交付结果和目标效果应被区分。完成一次实现，不等于已经证明其上层假设成立；后续 Evidence 应能够反向修正 Work Graph、Spec、Architecture 或 Vision 解释中的错误认知。

Vision Harness 最终要实现的不是“让 Agent 遵守更多流程”，而是：

> **让 Agent 在长期软件开发中始终看得见完整目标，在正确的层级做正确的决策，并让每一次局部实现都成为向 Vision 收敛的一步。**
