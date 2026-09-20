# Vision Harness

`0.2.0-alpha.1` 为一个入口与十八类用户工作提供 Skill 实现，覆盖愿景、规划、实施、审查、交付、协调和长期纠偏。它们按任务选择，不是十九个强制步骤。实现文件已经提交不等于工作路径已经通过运行验收，具体边界见本文末尾。

## 工作入口

| 工作 | Skill |
| --- | --- |
| 识别请求、恢复事实与授权 | [using-vision-harness](skills/using-vision-harness/SKILL.md) |
| 按缺口接入项目 | [project-onboarding](skills/project-onboarding/SKILL.md) |
| 多轮愿景讨论与维护 | [vision-management](skills/vision-management/SKILL.md) |
| 关键假设调查 | [assumption-validation](skills/assumption-validation/SKILL.md) |
| 整体规划与滚动细化 | [breakdown](skills/breakdown/SKILL.md) |
| 单项范围与完成条件 | [issue-shaping](skills/issue-shaping/SKILL.md) |
| 依赖、并行与统一候选集成 | [delivery-coordination](skills/delivery-coordination/SKILL.md) |
| 行为规格制定与演进 | [spec-development](skills/spec-development/SKILL.md) |
| 技术方案、架构与必要 ADR | [technical-design](skills/technical-design/SKILL.md) |
| TDD 实施与缺陷处理 | [tdd-development](skills/tdd-development/SKILL.md) |
| 设计、代码和流程简化 | [simplification](skills/simplification/SKILL.md) |
| 规格审查 | [spec-review](skills/spec-review/SKILL.md) |
| 代码审查 | [code-review](skills/code-review/SKILL.md) |
| PR 推进条件审查 | [pr-review](skills/pr-review/SKILL.md) |
| 获取或审计变更证据 | [change-verification](skills/change-verification/SKILL.md) |
| 交付构件、发布与收尾 | [release-delivery](skills/release-delivery/SKILL.md) |
| 整体回顾与纠偏 | [project-convergence](skills/project-convergence/SKILL.md) |
| 根或局部 Agent 指引维护 | [agent-instructions](skills/agent-instructions/SKILL.md) |
| 审查规范与宿主入口维护 | [review-setup](skills/review-setup/SKILL.md) |

维护者的 `method-evaluation` 保留在研发仓库，不包含在此普通用户包内，也不是用户项目的必经步骤。

## 本地安装

下面使用仓库根目录的 marketplace 配置，不是将包目录当成 marketplace。先检出准备使用的分支或提交，再把示例路径替换为本地仓库路径：

```bash
codex plugin marketplace add /path/to/Vison-Harness
codex plugin add vision-harness@personal
```

安装后启动新会话，让宿主读取当前候选。已有安装的更新命令以本机 `codex plugin --help` 和实际宿主支持为准，不通过手动覆盖用户缓存、信任或全局配置处理。

在支持显式 Skill 选择的宿主中选择相应名称，再给出任务与边界。例如：

```text
使用 tdd-development 完成现有 Issue，允许修改相关代码和测试，提交到独立分支，不要合并。
```

```text
使用 pr-review 检查当前 PR，只给判断，不修复、不合并。
```

```text
使用 delivery-coordination 安排这批工作的依赖与集成，保留已有规划。
```

自然语言请求可由入口帮助选择工作；是否自动触发取决于宿主，不能仅因存在入口 Skill 就假定会自动调用。安装本候选不等于已经完成某项用户任务。

## 包和工具边界

共享规则位于 `references/`，从研发仓库的权威方法与必要行为约定确定性生成。实施、规格、审查和协调按需读取 `engineering-rules.md`，不把全部规则复制到每个 Skill。消费项目的事实仍从项目本身和 GitHub 获取。

文件、GitHub、测试和委派操作依赖宿主已有工具与本轮授权。本包不捆绑 MCP、Hook、调度服务或自有状态数据库，也不会因安装而获得额外操作权限。缺少工具时说明受影响动作，其他可以完成的工作继续。

安装和更新不得改写消费项目的愿景、指引、规划、自定义规则或代码；显式获准的工作才修改相应对象。讨论、实施、审查、合并和发布的权限分别判断。

## 开发装配：生成分发内容

源 Skill 位于研发仓库 `.agents/skills/`。包内 `skills/` 和 `references/` 由 `scripts/assemble_plugin.py` 中的明确清单与引用映射生成，许可证随构件复制。该脚本不生成 Plugin 清单、marketplace 配置或本使用说明。

修改源材料后，只有需要重新生成分发内容时，才在研发仓库根目录运行：

```bash
python3 scripts/assemble_plugin.py
```

这是构建命令，会重建包内生成目录，不是对原包的只读检查。不要对生成副本单独修补后再与源文件各自维护，也不要将完整研发仓库、评估判据或未见案例复制进包。

## 维护检查：与构建分开执行

下面是已有检查入口，不是安装步骤，也不会仅因本文列出而自动运行：

```bash
python3 scripts/assemble_plugin.py --check
python3 scripts/test_assemble_plugin.py
```

`--check` 比较当前包和临时装配结果，不修复漂移；装配测试在临时副本中运行，不应改写原始待检查包。

要判断一个已经存在的包是否漂移，先对该包执行只读检查，不要先运行构建命令将它重建。需要修订源文件并重新构建时，分别记录原包状态和新构件结果；后者通过不能证明原包没有问题。结构或装配检查也不能替代实际宿主中的任务结果。

## 本候选的边界

本次迭代交付完整入口范围的实现与分发文件，没有执行装配检查、测试、安装演练或新的 Agent 行为验收。它不是已经证明所有工作路径可靠的正式稳定版，也没有公开发布。此前五个入口的历史接受只适用于相应旧候选，不能自动覆盖新增能力或本轮对交付指令的修改。

实现、检查和审查的实际记录见 [PR #38](https://github.com/MC0571/Vison-Harness/pull/38)。本说明中的命令与交互只提供使用方式，不构成执行记录。

获得构件、打开 PR、合并、发布和关闭长期能力是不同动作；交付候选不会自动执行后四项。实际质量结论以对应提交的工作记录为准。
