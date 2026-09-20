# Vision Harness

Vision Harness 为编程 Agent 提供五个可直接调用的工作入口：

- `using-vision-harness`：识别请求、相关项目事实、授权和停止位置。
- `project-onboarding`：查找真实接入缺口，不创建第二套项目结构。
- `vision-management`（显示为 **Vision**）：进行真实多轮讨论，只记录已获授权的决定。
- `agent-instructions`：维护根或局部 `AGENTS.md`，保留已有规则。
- `breakdown`：把已接受的愿景转成具体产品交付规划，并保留既有规划行为。

包内运行规则位于 `references/`；消费项目事实仍保留在消费项目中。安装或更新 Plugin 不会写入 `VISION.md`、`AGENTS.md`、计划或自定义项目规则。

## 本地安装

在仓库检出目录中，先添加仓库 marketplace，再安装 Plugin：

```bash
codex plugin marketplace add /path/to/Vison-Harness
codex plugin add vision-harness@personal
```

更新后启动新会话，使宿主加载新的 Skill 集合。当前仓库只提供本地候选，没有公开发布；仅有 Skill 文件也不能证明宿主会自动加载，必要时应在目标宿主中验证。

## 开发装配

提交的包由仓库中的确定性脚本 `scripts/assemble_plugin.py` 生成。脚本复制四个新源 Skill 和既有 Breakdown Skill，把项目相对引用改为包内引用，并从权威方法和 Spec 源生成精简运行参考。验证前从仓库根目录运行。
