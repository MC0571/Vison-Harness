# Vision Harness Plugin

0.4.0 组合分发十二个职责明确、资源自包含的普通 Skill。每个 `skills/<name>/` 都有自己的方法 references、可选 assets 和 LICENSE；Plugin 没有根级方法 references，也不负责补齐不完整 Skill。

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

Plugin 整包安装和下方的散装 Skill 安装二选一，避免同一 Skill 出现重复来源。

在 Codex CLI 中执行：

```bash
codex plugin marketplace add MC0571/Vison-Harness --ref main
codex plugin add vision-harness@MC
```

先添加上面的 marketplace；添加 `MC` 后，也可以改用 Codex UI，在该 marketplace 中选择 `vision-harness` 安装。安装完成后开启新会话，让宿主加载新的 Plugin。

如果以前从旧的 `vision-harness@personal` 安装，先确认 `vision-harness@MC` 已成功安装，再按需要移除旧的 Vision Harness 副本。只处理这个旧副本，不要删除整个 `personal` marketplace，因为其他 Plugin 可能仍在使用它。

Plugin 根目录的 `plugin.json` 使用 Agent Plugins 1.0 清单（`$schema` 为 `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`），插件名是 `vision-harness`；OpenAI 安装界面元数据位于 `extensions.com.openai.interface`，Skill 目录为 `./skills/`。每个 Skill 目录仍然自包含完整方法资源。

## 安装指定 Skill

第三方 `npx skills` 默认安装到当前项目。把全部 Vision Harness Skill 安装给 Codex：

```bash
npx skills add https://github.com/MC0571/Vison-Harness/tree/main/plugins/vision-harness/skills --skill '*' -a codex
```

只安装指定 Skill 时使用 `SKILL.md` frontmatter 中的短名，并可在同一个 `--skill` 参数后列出多个名称：

```bash
npx skills add https://github.com/MC0571/Vison-Harness/tree/main/plugins/vision-harness/skills --skill review breakdown -a codex
```

需要用户级安装时加 `-g`。不要使用 `--all`，它会把发现的全部 Skill 安装到全部 Agent。`--skill` 使用 `review` 这类短名，不使用安装界面显示的 `Vision-Harhess: Review`。源目录包含完整方法资源；`npx` 不需要安装本仓库的 npm 包，也不需要 Python。安装后开启新会话。

## 单 Skill 复制

如果宿主不支持 Plugin 或 `npx skills`，可将当前 Plugin 目录下的 `skills/<name>/` 作为备选路径整体复制。确认消费项目目标目录不存在或无冲突后，将整个目录复制到：

```text
<consumer-project>/.agents/skills/<name>/
```

例如，将 `skills/breakdown/` 整体复制到消费项目的 `.agents/skills/breakdown/`。不要只复制 `SKILL.md`，也不要覆盖消费项目已有同名目录。消费项目不需要 Python 环境，也不需要运行本仓库的全仓校验。

## 研发装配与检查

编辑 `.agents/skills/<name>/` 中的人工方法文件；共同方法只编辑 `skill-resources/` 的四份源。不要手改 `plugins/vision-harness/skills/` 或各 Skill 中由装配同步的共同副本与 LICENSE。

维护者若需从本地分支或提交安装，先检出目标版本，再在仓库根执行：

```bash
codex plugin marketplace add /path/to/Vison-Harness
codex plugin add vision-harness@MC
```

首次准备开发环境时，在仓库本地创建并启用虚拟环境，然后安装固定开发依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
```

先运行只读漂移检查，识别已有构件状态；发现需要同步时再运行装配：

```bash
python3 scripts/assemble_plugin.py --check
```

若检查发现需要同步源副本或构件，再运行装配：

```bash
python3 scripts/assemble_plugin.py
```

```bash
python3 scripts/validate_skills.py --source
python3 scripts/validate_skills.py --package
python3 scripts/test_assemble_plugin.py
python3 scripts/test_validate_skills.py
python3 scripts/assemble_plugin.py --check
```

维护者需要验证单 Skill 导出时，可在上述开发环境准备完成后运行：

```bash
python3 scripts/assemble_plugin.py --export-skill breakdown --output /tmp/vision-harness-export
```

命令生成 `/tmp/vision-harness-export/breakdown/`，用于维护者核对导出结果；它不属于消费项目的安装前置步骤，不安装到用户全局环境，也不携带其他 Skill、研发 METHOD/Spec/Eval 或 Plugin 清单。

[CI](https://github.com/MC0571/Vison-Harness/blob/main/.github/workflows/ci.yml) 在面向 `main` 的 PR 和 `main` 推送中执行上述校验、回归测试与只读装配检查；检查提交中的生成物，不先重新装配来消除漂移。

装配递归保留完整目录、二进制内容和执行位；`--check` 是只读漂移检查。结构与迁移检查只证明当前文件集合、封装和确定性规则，不证明宿主安装、自动触发、权限隔离或 Agent 效果。

## 参考来源

- [OpenAI Plugin 清单与打包说明](https://developers.openai.com/plugins/build/plugins)
- [`npx skills` CLI](https://github.com/vercel-labs/skills)
