# Vision Harness 产品架构

## 设计目标

Vision Harness 由十二个可独立使用的普通 Skill 与一个组合分发 Plugin 构成。每个普通 Skill 目录是自己的运行方法资源边界：`SKILL.md`、直接加载的 `references/`、可选 `assets/` 和 `LICENSE` 一起构成完整单元。Plugin 只组合这些完整单元，不为不完整 Skill 补方法。

这些入口不是固定生命周期。用户可以直接请求任何一项工作；条件协作按任务发生，不要求兄弟 Skill 已安装。方法重要、内容长或常被共同使用，本身都不足以成为新入口。

## 源码、共享源与分发

```text
.agents/skills/<name>/        # 完整 Skill 源目录，可单独复制
skill-resources/              # 四份研发期共同方法单一来源
plugins/vision-harness/       # 组合分发；skills/ 是完整目录生成物
scripts/                      # 装配、完整性检查和 unittest
```

`skill-resources/` 只在研发时复用。装配将明确映射的内容逐字节物化到各源 Skill 的 `references/`，这些副本与源码一起提交，使 `.agents/skills/<name>/` 自身可迁移；副本不是第二个人工权威源。运行时不读取 `skill-resources/`、仓库根 METHOD/Spec/Eval、兄弟 Skill 或插件根 references。

`plugins/vision-harness/plugin.json` 与 Plugin README 手工维护；这是 portable Agent Plugins 根清单，Skills 由固定的 `skills/` 目录发现，OpenAI 专用 interface 位于 `extensions["com.openai"].interface`。`plugins/vision-harness/skills/` 和 Plugin LICENSE 由装配生成。包内不再存在 `.codex-plugin` 清单或根级 `references/`。历史材料和 Eval 留在研发仓库，不进入普通分发。

共享源映射固定为：

| 共享源 | 接收 Skill |
| --- | --- |
| `common-rules.md` | 全部十二项 |
| `critical-assumptions.md` | vision-management、breakdown、technical-design |
| `complexity-control.md` | technical-design、tdd-development、review、project-convergence |
| `evidence-rules.md` | tdd-development、review、change-verification、release-delivery |

## 十二个组件与条件交接

| Skill | 独立结果 | 必要本地资源 | 外部环境要求 | 可选协作 | 无其他 Skill 时的完成边界 |
| --- | --- | --- | --- | --- | --- |
| using-vision-harness | 可接手上下文与下一步 | context-recovery、task-routing、common-rules | 消费项目事实入口 | 任一后续工作 | 完整返回项目、承诺、授权、缺口和下一步 |
| project-onboarding | 缺口分类与最小接入 | adoption-gap、tooling-and-instructions、common-rules | 目标项目与实际命令/宿主 | agent-instructions、vision-management | 完成本地接入或准确报告外部受阻 |
| vision-management | 形成/检查/修订愿景 | vision-dialogue、vision-review-and-update、vision-outline、critical-assumptions、common-rules | 用户真实产品取舍 | breakdown | 交付确认/未知/非目标；按授权持久化 |
| breakdown | 产品规划、单项整理或统一候选 | whole-product-planning、rolling-refinement、work-slicing、issue-shaping、delivery-coordination、critical-assumptions、common-rules | GitHub/宿主工具按模式可用 | technical-design、tdd-development、change-verification、release-delivery | 方案模式止于方案；执行模式负责集成与必要证据 |
| spec-development | Spec 变化或无需修改结论 | spec-surface、spec-authoring、behavior-spec-outline、common-rules | 已确认行为；已有语义入口存在时复用 | review、technical-design | 完成长期行为约定，不实施代码 |
| technical-design | 架构沿用/调整与实施路径 | architecture-impact、module-and-interface-design、change-design、decision-records、critical-assumptions、complexity-control、common-rules | 现有架构与代码事实 | spec-development、tdd-development | 给出方案和必要长期记录，不替用户定产品 |
| tdd-development | 实现/修复与基本验证，或诊断 | test-discovery、tdd-cycle、test-quality、debugging、complexity-control、evidence-rules、common-rules | 代码、测试或现有运行入口、修改授权 | review、change-verification、release-delivery | 自行完成当前修改所需测试，停在未授权交付边界 |
| review | Spec/Code/PR 独立判断 | 三类 review、finding-validation、review-report、complexity-control、evidence-rules、common-rules | 准确候选和基线 | change-verification、tdd-development | 只读形成 finding 或有限无阻断结论 |
| change-verification | 执行/复用/审计证据 | verification-selection、verification-execution、evidence-rules、common-rules | 候选、命令与环境 | tdd-development、review | 给出范围化结果，不修候选 |
| release-delivery | 指定交付副作用 | package-delivery、pr-and-merge、release-and-close、evidence-rules、common-rules | 远端/发布工具与逐项授权 | review、change-verification | 自行核对候选证据，只执行获准动作；部分成功分项处理 |
| project-convergence | 事件纠偏、阶段检查或限定调整 | convergence-analysis、bounded-correction、complexity-control、common-rules | 明确回顾范围或新事实，以及相关权威入口 | 任一受影响工作 | 主动检查限定阶段，或完成获准限定纠偏；越界工作明确交接 |
| agent-instructions | 项目规则或宿主配置 | project-instructions、reviewer-configuration、common-rules | 真实宿主资料与项目规则 | review | 区分文件存在、加载与审查结果 |

交接是条件性的：愿景充分时可进入规划，但愿景结果自身也可结束；明确 Issue 可直接实施；Review 可独立请求；交付协调在已授权执行时不能因其他 Skill 缺失退化成静态方案。

## 工作方法与资源边界

`SKILL.md` 保持任务选择、主决策、输入输出与停止位置；本地 reference 提供该任务所需的选择方法、反例、操作分支与例外。资源只在条件适用时加载，不要求每次通读全部文件，也不把方法菜单变成新审批流程。

复杂工程工作的具体判断包括：Breakdown 区分决策、行为切片与迁移批次；技术设计检查接口知识负担、复杂度承担与变化局部性；TDD 选择有判别力的观察点、独立期望与适当测试替身；Review 在报告前反证疑点；Verification 从承诺和失败方式选择检查；Release 分清部分成功与恢复；Convergence 支持事件驱动和阶段主动检查。

这些是现有职责的实现方法，不新增公开 Skill、强制文件套餐、固定比例/阈值、固定 reviewer 数量或兄弟 Skill 运行依赖。架构未变也可需要复杂迁移方案；阶段回顾不要求用户先指出已知缺陷。

## 职责覆盖与既有验证投影

| 有效职责 | 当前承担 | 独立行为依据 | 既有 Eval 投影 |
| --- | --- | --- | --- |
| 愿景多轮形成、检查与修订 | vision-management | `specs/vision/spec.md` | project-startup |
| 上下文恢复、接入与授权有效性 | using-vision-harness、project-onboarding、agent-instructions | `specs/project-context/spec.md` | project-startup、work-entry-routing |
| 全景/滚动规划 | breakdown | `specs/breakdown/spec.md` | breakdown |
| 单项整理与交付协调 | breakdown 的单项/协调模式 | Breakdown Spec 与对应本地方法 | breakdown、work-entry-routing |
| Spec/Code/PR 独立审查 | review 的三对象模式 | `specs/review/spec.md` | work-entry-routing |
| 关键假设、复杂度与证据复用 | 当前负责决定/实现/审查的入口按条件加载共享方法 | METHOD 的共同判断原则 | work-entry-routing |

这些 Eval 是既有验证设计和历史证据入口，不表示当前方法修订候选已执行新的 Agent 效果验收。静态设计修订不删除既有独立行为依据，也不将结构检查称为真实行为通过。

## 事实与责任边界

GitHub 承载动态工作事实；Spec 承载长期行为；Architecture 承载当前长期结构；ADR 承载重大已作决定的理由；一次实施方案默认留在 GitHub。Skill 是操作方法，Eval 检查实际行为，不能相互替代。

完整目标保持可见，近期逐步细化。Deferred 与 Non-goal 分开；已有合适工作项即可承载暂缓内容。不维护与 GitHub 平行的权威路线图或进度数据库。

## 装配与完整性不变量

`scripts/assemble_plugin.py` 先同步明确生成的共享副本与 LICENSE，验证源 Skill，再将完整目录递归复制到 staging，验证通过后替换生成区域。复制保留字节、相对层级和执行位，并排除缓存、虚拟环境与临时产物；失败的源/staging 校验不破坏现有包。

`--check` 只读构造预期树，比较源副本、缺失/多余文件、内容和执行位。`--export-skill` 只导出一个普通 Skill，结果必须与 Plugin 中对应目录一致。`validate_skills.py --skill` 仅依赖给定目录；它验证结构封装，不证明宿主加载或 Agent 效果。

普通 Skill 不包含运行脚本、Hook、MCP 或自定义子 Agent；装配仍保留未来 Skill 自身 `scripts/`、二进制 assets 和执行位的能力。复杂度、安全、授权和证据边界由方法执行，不建设自有调度器、状态库或审批平台。
