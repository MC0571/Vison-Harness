# Vision Harness

`0.2.0-alpha.1` 提供一个入口与十八个用户工作 Skill，覆盖从愿景到交付、协调和长期纠偏的完整职责。它们是按需调用的工作方法，不是十九个强制步骤。

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

检出本候选所在分支后，在仓库目录中添加 marketplace 并安装：

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

共享规则位于 `references/`，从研发仓库的权威方法与必要行为约定确定性生成。实施、规格、审查和协调使用按需读取的 `engineering-rules.md`，不把全部规则复制到每个 Skill。消费项目的事实仍从项目本身和 GitHub 获取。

文件、GitHub、测试和委派操作依赖宿主已有工具与本轮授权。本包不捆绑 MCP、Hook、调度服务或自有状态数据库，也不会因安装而获得额外操作权限。缺少工具时说明受影响动作，其他可以完成的工作继续。

安装和更新不得改写消费项目的愿景、指引、规划、自定义规则或代码；显式获准的工作才修改相应对象。讨论、实施、审查、合并和发布的权限分别判断。

## 开发装配

源 Skill 位于仓库 `.agents/skills/`，包内 Skill 与运行参考由已有脚本生成。在仓库根目录运行：

```bash
python3 scripts/assemble_plugin.py
python3 scripts/assemble_plugin.py --check
python3 scripts/test_assemble_plugin.py
```

`--check` 只读比较，不修复漂移；装配测试使用隔离临时目录，不改写待检查包。不要手工维护生成副本，也不要把 Spec、Eval、oracle 或完整研发仓库复制进分发包。

## 本候选的边界

这是完整工作职责的实现与分发候选，不是已经证明所有场景可靠的正式稳定版。本次不扩展 Eval 项目，不进行新的 Codex 多轮行为验收、跨宿主验证、真实 GitHub 写入补验或公开发布。历史五 Skill 的接受记录不能自动覆盖新增能力。

获得构件、打开 PR、合并、发布和关闭长期能力是不同动作；交付候选不会自动执行后四项。实际质量结论以对应提交的工作记录为准。
