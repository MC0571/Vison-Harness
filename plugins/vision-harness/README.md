# Vision Harness

0.3.0-alpha.1 将普通分发从十九个平级入口收敛为 12 个工作入口 + 按条件加载的 references。职责没有按文件数量删减：单项 Issue 整理、交付协调、关键假设、复杂度控制和审查配置等方法仍在包内，只是不再作为独立用户入口。

## 工作入口

| 工作 | Skill |
| --- | --- |
| 识别请求、恢复最少事实与授权 | [using-vision-harness](skills/using-vision-harness/SKILL.md) |
| 按真实缺口接入项目 | [project-onboarding](skills/project-onboarding/SKILL.md) |
| 愿景形成、检查与维护 | [vision-management](skills/vision-management/SKILL.md) |
| 全景/滚动规划、单项整理、依赖并行与集成协调 | [breakdown](skills/breakdown/SKILL.md) |
| 行为 Spec surface、制定与演进 | [spec-development](skills/spec-development/SKILL.md) |
| 技术方案、Architecture Impact、ADR | [technical-design](skills/technical-design/SKILL.md) |
| TDD 实施、调试与复杂度控制 | [tdd-development](skills/tdd-development/SKILL.md) |
| Spec / Code / PR 审查 | [review](skills/review/SKILL.md) |
| 获取、复用或审计变更证据 | [change-verification](skills/change-verification/SKILL.md) |
| 构件、PR/合并、发布与收尾 | [release-delivery](skills/release-delivery/SKILL.md) |
| 系统级长期 convergence | [project-convergence](skills/project-convergence/SKILL.md) |
| AGENTS、审查规则和宿主 Agent 配置 | [agent-instructions](skills/agent-instructions/SKILL.md) |

维护者的 method-evaluation 只存在于研发仓库，不装入普通用户包。

## 旧入口迁移

- issue-shaping、delivery-coordination → 直接调用 breakdown 的单项/协调模式。
- spec-review、code-review、pr-review → review，按对象选择 Spec/Code/PR。
- assumption-validation → 当前负责决定的工作入口按条件加载规划方法。
- simplification → Design/TDD/Review/Convergence 按条件加载实现与复杂度方法。
- review-setup → agent-instructions 的审查配置模式。

这些是入口收敛，不是能力删除。

## Progressive disclosure

SKILL.md 只保留结果、使用边界、执行骨架、关键授权规则和 reference 加载条件。详细方法位于 references/：

- shared-rules.md：授权、安全共享事实修改、治理充分性；
- planning-methods.md：完整目标、单项整理、关键假设、依赖/并行/集成；
- spec-design-methods.md：Spec surface、Architecture Impact、ADR、技术方案；
- implementation-methods.md：行为切片、TDD、调试、复杂度控制；
- review-methods.md：Spec/Code/PR 详细审查；
- evidence-methods.md：证据范围、复用、执行和审计；
- convergence-methods.md：系统级收敛；
- agent-config-methods.md：AGENTS、审查规范和宿主配置；
- 另有 Vision、Project Context、Breakdown、Review 的行为 references。

不要在开始任务时预读全部 references。Skill 中写明了何时加载哪一份。

## 本地安装

先检出准备使用的分支或提交，再使用仓库根 marketplace：

~~~bash
codex plugin marketplace add /path/to/Vison-Harness
codex plugin add vision-harness@personal
~~~

安装后启动新会话，让宿主读取当前候选。在支持显式 Skill 选择的宿主中可以直接调用，例如：

~~~text
使用 breakdown 整理这个 Issue 的范围与完成条件；只给建议，不改 GitHub。
~~~

~~~text
使用 review 审查当前 PR，只给判断，不修复、不合并。
~~~

~~~text
使用 tdd-development 完成这个明确 Issue，允许修改代码和测试，提交独立分支，不要合并。
~~~

自然语言请求可以由 using-vision-harness 帮助选择入口；它不是必经路由器，是否自动触发取决于宿主。

## 包和工具边界

共享 references 由研发仓库的 METHOD 与行为 Spec 确定性生成；消费项目事实仍从消费项目和 GitHub 获取。文件、GitHub、测试、子 Agent 等操作使用宿主已有工具及本轮授权，本包不捆绑自有状态库、调度器或权限系统。

安装和更新不得覆盖消费项目愿景、AGENTS、规划、自定义规则或代码。讨论、实施、审查、合并、发布分别判断权限。

## 开发装配与检查

源 Skill 位于研发仓库 .agents/skills/；包内 skills/ 和 references/ 是生成物：

~~~bash
python3 scripts/assemble_plugin.py
~~~

只读漂移检查与装配测试：

~~~bash
python3 scripts/assemble_plugin.py --check
python3 scripts/test_assemble_plugin.py
~~~

测试检查目标 Skill 集、包内引用、reference 分割、旧入口移除以及确定性装配。结构检查不等于真实 Agent 行为通过；行为回归设计位于研发仓库 evals/，不会打进普通包。

## 当前候选边界

0.3.0-alpha.1 是架构收敛候选：源入口、分发构件、独立 Review 行为约定和路由/reference Eval 已同步更新。当前提交环境没有执行真实宿主安装或 Agent 行为验收；旧候选的运行证据不能自动扩到本候选。构建通过、安装通过、用户任务完成、独立审查和发布授权仍是不同结论。
