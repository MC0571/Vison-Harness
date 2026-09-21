# Agent Config Methods

This runtime reference is generated from the repository's accepted method and behavior sources. It is intentionally self-contained; edit the source documents and rerun the assembly instead of hand-editing this file.

## 6. 维护 Agent 工作约定和审查规则

仓库中的长期事实不仅包括产品行为和架构，也可以包括长期有效的 Agent 工作约定。

Vision Harness 应按需要帮助项目创建和维护 `AGENTS.md`：

- 根目录文件保存全仓适用的工作规则、事实入口、构建测试入口和关键边界；
- 子目录文件只保存该范围特有的差异；
- 没有局部差异，就不创建局部文件；
- 已经由 Spec、架构或其他权威文档维护的规则，应引用而不是复制。

维护不仅包括新增，也包括发现失效、重复、冲突和已经不适用的规则。

项目使用的宿主可能有不同的 `AGENTS.md` 查找、覆盖和加载方式。Vision Harness 应依据实际宿主验证适用规则是否真的能被 Agent 读取，而不能仅凭文件存在就宣布配置完成。

修改 `AGENTS.md`、Skill、审查规范或 Agent 配置，可能改变后续 Agent 行为，不能仅因为文件是 Markdown 或配置文件就自动视为无风险修改。

实施者不能为了让当前工作通过，未经授权先放宽约束自己的规则或审查标准。

### 审查规则

Vision Harness 应帮助项目在确有需要时建立长期审查规则，例如：

- Spec 审查：行为、边界、异常、约束和可验证性是否清楚；
- 代码审查：实现是否正确、是否满足相关约定、是否破坏架构、是否引入无必要复杂度；
- PR 审查：当前候选变更的范围、证据、审查和授权是否足以支持本次合并或交付判断。

这些是不同审查对象，不代表每次必须有三个文件、三名 reviewer 或三轮审批。

审查规范应说明：

- 何时触发；
- 需要读取哪些输入；
- 检查什么；
- 什么构成阻断；
- 什么只是建议；
- 审查者允许做什么。

没有发现问题可以是正常结果。风格偏好和可由 CI 自动处理的问题，不应为了体现审查工作量而被包装成阻断。

规则可以由项目文档、Vision Harness 的 Skill 或宿主支持的 Agent 配置承载。子 Agent 是一种执行方式，不是审查规范本身；一次审查结果仍应留在对应的 Issue、PR 或项目既有载体中。

---
