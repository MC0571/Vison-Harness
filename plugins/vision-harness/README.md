# Vision Harness Plugin

0.4.0-alpha.2 组合分发十二个职责明确、资源自包含的普通 Skill。每个 `skills/<name>/` 都有自己的方法 references、可选 assets 和 LICENSE；Plugin 没有根级方法 references，也不负责补齐不完整 Skill。

## 工作入口

| 工作 | Skill |
| --- | --- |
| 恢复任务上下文并定位下一步 | `using-vision-harness` |
| 查明并完成最小项目接入 | `project-onboarding` |
| 形成、检查或修订愿景 | `vision-management` |
| 全景/滚动规划、单项整理、交付协调 | `breakdown` |
| 建立、更新或复用长期行为约定 | `spec-development` |
| 技术方案、架构影响与必要 ADR | `technical-design` |
| TDD 实施、缺陷修复与诊断 | `tdd-development` |
| Spec / Code / PR 审查 | `review` |
| 执行、复用或审计证据 | `change-verification` |
| 打包、PR、合并、发布或关闭 | `release-delivery` |
| 系统级偏离与限定纠偏 | `project-convergence` |
| Agent 指引与 reviewer 配置 | `agent-instructions` |

这些入口不是固定流程。明确的实施、审查或单项整理可以直接调用；`using-vision-harness` 不是必经路由器。维护者 Skill `method-evaluation` 不在本包中。

## 安装整个 Plugin

先检出准备使用的分支或提交，再从仓库根 marketplace 安装：

```bash
codex plugin marketplace add /path/to/Vison-Harness
codex plugin add vision-harness@personal
```

当前分发使用 Codex 兼容清单 `.codex-plugin/plugin.json`，其 `skills` 指向 `./skills/`。这个 Plugin 格式与“每个 Skill 目录方法自包含”是两个边界：前者负责组合发现，后者保证单目录不依赖 Plugin 根或提供者仓库。

## 单 Skill 导出与复制

在研发仓库运行：

```bash
python3 scripts/assemble_plugin.py --export-skill breakdown --output /tmp/vision-harness-export
```

命令生成 `/tmp/vision-harness-export/breakdown/`。确认消费项目目标目录不存在或无冲突后，将整个目录复制到：

```text
<consumer-project>/.agents/skills/breakdown/
```

不要只复制 `SKILL.md`，也不要覆盖消费项目已有同名目录。本命令不安装到用户全局环境，不携带其他 Skill、研发 METHOD/Spec/Eval 或 Plugin 清单。

## 研发装配与检查

编辑 `.agents/skills/<name>/` 中的人工方法文件；共同方法只编辑 `skill-resources/` 的四份源。不要手改 `plugins/vision-harness/skills/` 或各 Skill 中由装配同步的共同副本与 LICENSE。

首次准备开发环境时，在仓库本地创建并启用虚拟环境，然后安装固定开发依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
```

```bash
python3 scripts/assemble_plugin.py
python3 scripts/validate_skills.py --source
python3 scripts/validate_skills.py --package
python3 scripts/test_assemble_plugin.py
python3 scripts/test_validate_skills.py
python3 scripts/assemble_plugin.py --check
```

[CI](../../.github/workflows/ci.yml) 在面向 `main` 的 PR 和 `main` 推送中执行上述校验、回归测试与只读装配检查；检查提交中的生成物，不先重新装配来消除漂移。

装配递归保留完整目录、二进制内容和执行位；`--check` 是只读漂移检查。结构与迁移检查只证明当前文件集合、封装和确定性规则，不证明宿主安装、自动触发、权限隔离或 Agent 效果。

## 当前候选边界

当前源码与 Plugin 构件都包含完整本地方法资源，旧插件根 `references/` 已移除。候选未执行真实消费项目安装或 Agent 效果评估，未发布正式版本。构件生成、宿主安装、任务结果、独立审查、合并与发布仍分别判断。
