# Vision Harness 产品架构

## 设计目标

Vision Harness 通过少量明确的用户工作入口提供软件工程方法；横切判断通过按条件加载的 references 复用，确定性操作才使用 scripts/assets。它不是固定流水线，也不建设自己的项目状态、调度、审批或权限系统。

划分 Skill 时主要看：用户是否会自然直接请求、是否有独立可验证结果、是否有不同副作用/授权边界、交互方式、可独立失败/完成，以及合并后是否会模糊职责。方法重要、内容长、有 checklist 或经常共同触发，本身都不足以成为独立 Skill。

## 当前普通工作入口

普通分发包含 12 个 Skill；method-evaluation 是维护者入口，不进入用户包。

| 入口 | 用户直接请求的结果 | 关键边界 |
| --- | --- | --- |
| using-vision-harness | 识别当前任务、最少必要事实与授权，选择直接入口 | 不实施、不自动授权；明确入口可绕过 |
| project-onboarding | 判断项目采用缺口，并按授权做最少接入修改 | 不重建已有愿景/规划/规则 |
| vision-management | 形成、检查或维护愿景 | 推荐不自动升级为用户决定 |
| breakdown | 全景/滚动规划、单项工作整理、多项交付协调 | 共享工作图事实；不实现产品 |
| spec-development | 建立、修改或复用长期行为 Spec | 纯内部重构不制造 Spec |
| technical-design | 架构影响、技术方案、必要 ADR、一次实施计划 | 简单变化直接沿用架构 |
| tdd-development | 实施明确变更，或诊断/修复缺陷 | 只调查时不修；按行为切片 |
| review | 审查 Spec、Code 或 PR | review-only 不改候选、不合并 |
| change-verification | 取得、复用或审计变更证据 | 证据结论不超范围，不替代审查 |
| release-delivery | 打包、PR/合并、发布或收尾 | 每种副作用分别授权 |
| project-convergence | 系统级偏离、重复、冲突与长期收敛 | 无新事实时零治理改动 |
| agent-instructions | AGENTS、审查规则与宿主 Agent 配置 | 文件存在不等于宿主加载或独立审查 |

这些入口都可以被直接调用。using-vision-harness 只是识别/接续入口，不是强制路由器。

## 从平级 Skill 收敛为共享方法

本次收敛不删除职责，而是把没有独立用户结果或高度横切的方法下沉。

| 旧平级 Skill / 责任 | 重构后归属 |
| --- | --- |
| assumption-validation | planning-methods 中的关键假设验证；Vision/Breakdown/Design 等遇到失败会推翻路线的未知时加载 |
| issue-shaping | breakdown 的单项整理模式 + planning-methods |
| delivery-coordination | breakdown 的协调模式 + planning-methods |
| simplification | implementation-methods 的复杂度控制；Design/TDD/Review/Convergence 按需使用 |
| spec-review / code-review / pr-review | 统一 review 入口，按对象读取 review-behavior 与 review-methods |
| review-setup | agent-instructions 的审查配置模式 + agent-config-methods |

Review 合并的依据是三类任务共享形成审查判断的用户意图、同一只读授权边界和相同问题输出模型；对象差异保留在方法 reference。Breakdown 合并单项整理与交付协调，是因为它们都直接维护同一工作图和交付承诺，允许用户以三种模式直接请求，不要求先做全景规划。

change-verification、release-delivery、project-onboarding 等仍保留独立入口，因为它们具有不同的可验证结果或明显不同的副作用边界。

## 条件 references

装配后的普通包使用以下 references。每个 Skill 只在对应条件出现时读取，不要求开始前读取 references 全部文件。

| Reference | 来源 | 什么时候读取 |
| --- | --- | --- |
| shared-rules.md | METHOD 1/5/12 | 授权、安全修改共享事实、条件充分/不足和治理比例 |
| planning-methods.md | METHOD 3/4 | Target/Current/Deferred、单项整理、关键假设、依赖、并行与集成 |
| agent-config-methods.md | METHOD 6 | AGENTS 分层、审查规则和宿主配置 |
| spec-design-methods.md | METHOD 7 | Spec surface、Architecture Impact、ADR 与技术方案 |
| implementation-methods.md | METHOD 8 | behavioral slicing、TDD、调试与复杂度控制 |
| review-methods.md | METHOD 9 | Spec/Code/PR 的详细审查方法 |
| evidence-methods.md | METHOD 10 | evidence scope、reuse、直接执行与审计 |
| convergence-methods.md | METHOD 11 | Spec/架构/工作图/Vision 的系统级 convergence |
| vision-behavior.md | Vision Spec | 愿景工作的独立可观察行为 |
| project-context-behavior.md | Project Context Spec | 接续、接入、授权有效性与宿主加载 |
| breakdown-behavior.md | Breakdown Spec | Breakdown 的长期行为约定 |
| review-behavior.md | Review Spec | 统一 Review 的行为与只读边界 |

SKILL.md 保留不能隐藏的规则：只审查不自动修改、当前切片不等于长期完成、测试通过不等于全部承诺、信息足够时继续、Deferred 与 Non-goal 分开、建议不自动升级为决定等。reference 只承载更长的判断过程和对象差异。

## 职责覆盖矩阵

| 已确认责任 | 工作入口 | 条件方法 / 独立依据 | 主要 Eval |
| --- | --- | --- | --- |
| Vision 形成、审查、维护 | vision-management | vision-behavior + shared-rules | project-startup |
| 全景规划、rolling refinement | breakdown | breakdown-behavior + planning-methods | breakdown |
| Issue shaping | breakdown 单项模式 | planning-methods | breakdown + work-entry-routing |
| delivery coordination | breakdown 协调模式 | planning-methods | work-entry-routing |
| Spec surface assessment / authoring / updating | spec-development | spec-design-methods | work-entry-routing |
| Spec review | review Spec 模式 | review-behavior + review-methods | work-entry-routing |
| architecture impact / design / durable decision / technical planning | technical-design | spec-design-methods；关键未知时 planning-methods | work-entry-routing |
| behavioral slicing / TDD / debugging | tdd-development | implementation-methods | work-entry-routing |
| adaptive verification / evidence reuse | change-verification | evidence-methods | work-entry-routing |
| code review / PR review | review Code/PR 模式 | review-behavior + review-methods + 按需 evidence-methods | work-entry-routing |
| semantic coverage | spec-development + tdd-development + review + change-verification | spec-design / implementation / review / evidence | breakdown + work-entry-routing |
| deferred work review / issue graph reconciliation | breakdown + project-convergence | planning + convergence | breakdown + work-entry-routing |
| architecture convergence / Spec consistency / Vision gap | project-convergence | convergence；按问题追加 spec-design/planning | work-entry-routing |
| authorization | 所有入口 | shared-rules；关键边界直接保留在 SKILL | project-startup + work-entry-routing |
| evidence scope | verification / review / delivery / implementation | evidence-methods | work-entry-routing |
| critical assumptions | 当前负责决定的入口 | planning-methods | work-entry-routing |
| complexity control | design / implementation / review / convergence | implementation-methods | work-entry-routing |
| AGENTS / project Agent configuration | agent-instructions | agent-config-methods + project-context-behavior | project-startup + work-entry-routing |

任何责任若没有入口、方法资源和验证位置，就不能因 Skill 合并而删除。

## 条件协作，不建立强制流水线

- 技术设计发现会推翻方案的未知：在当前 Design 中加载关键假设方法；只阻塞受影响决定。
- Spec 发现未确认产品取舍：返回 Vision/当前 Issue 讨论，不把技术偏好写成需求。
- TDD 发现真实语义歧义：暂停受影响行为；其他明确切片继续。
- Review 发现旧证据不再覆盖当前候选：只请求补验受影响部分。
- Convergence 发现重复或失效规则：交给对应规划、设计或 Agent 配置入口，不重跑完整生命周期。
- Breakdown 协调模式发现没有并行收益：直接选择串行，不为了协调制造子 Agent 或额外 Issue。

交接只传递范围、来源/版本、允许副作用、缺口和期望返回结果。前一个入口完成不自动证明后一个入口条件成立，也不扩大权限。

## 分发与可分发性

.agents/skills/ 是研发源；plugins/vision-harness/skills/ 与 references/ 是 scripts/assemble_plugin.py 生成的普通用户包。清单显式选择普通入口；method-evaluation 只留研发仓库。

运行 reference 从 METHOD/行为 Spec 的指定章节确定性生成。包内 Skill 的所有相对引用必须指向包内资源；普通 Plugin 安装不依赖研发源码、旧安装或其他同名 Skill。当前正式分发边界是整个 Plugin；.agents/skills/ 与包内 skills/<name>/ 都不是声明为可单独复制安装的自包含分发单元。若未来提供单 Skill 安装，构建必须把该 Skill 所需 references/scripts/assets 一并物化，并增加相应完整性测试。装配测试负责检查 Skill 集合、断链、生成漂移、reference 归属和已移除入口不再泄漏。

当前没有独立 Claude/Cursor/Copilot 适配层；仓库提供通用 Skill 源和 Codex Plugin/marketplace 清单。其他宿主只有在实际适配和验证存在时才声明支持。

## Spec / Skill / Eval 分离

行为约定回答什么行为才算正确；Skill/reference 回答 Agent 如何完成；Eval 检查实际行为是否满足约定。三者可以表达同一要求的不同投影，但当前 Skill 不能同时修改方法和唯一成功标准。

本轮统一 Review 新增独立 specs/review/spec.md。路由与 reference 条件由 evals/work-entry-routing/ 验证，并与既有 Vision/Project Context/Breakdown 场景共同覆盖该停时停和条件充分时继续。
