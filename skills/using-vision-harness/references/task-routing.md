# 用户意图与直接工作

| 用户意图 | 直接工作 | 选择依据与停止位置 |
| --- | --- | --- |
| 恢复上下文、找下一步 | using-vision-harness | 返回可接手上下文，不实施 |
| 接入新/既有项目 | project-onboarding | 查真实采用缺口并做获准最小接入 |
| 形成、检查或修订愿景 | vision-management | 交付共同理解或获准愿景修改 |
| 全景/滚动规划、单项整理、协调 | breakdown | 按请求模式交付计划或统一候选 |
| 建立或修改长期行为约定 | spec-development | 交付 Spec 变化或无需修改结论 |
| 技术方案、架构影响、ADR | technical-design | 交付实施路径与必要长期决定 |
| 实施或诊断缺陷 | tdd-development | 交付代码与基本验证，或诊断结论 |
| 审查 Spec、Code 或 PR | review | 交付绑定候选的只读判断 |
| 执行、复用或审计证据 | change-verification | 交付有范围的验证结论 |
| 打包、PR、合并、发布、关闭 | release-delivery | 只执行明确授权的动作 |
| 系统级偏离与限定纠偏 | project-convergence | 交付诊断或获准有界调整 |
| Agent 指引或 reviewer 配置 | agent-instructions | 交付最小配置与加载边界 |

入口名称是可选建议，不是依赖。若对应 Skill 不存在，仍返回这项工作的目标、必要输入、允许副作用、完成条件与下一步；不得只说“请安装某 Skill”。

一个请求可包含多项工作，但不自动变成固定生命周期。先做真正阻塞的动作；例如“实现并开 PR”可连续实施、验证和创建 PR，而“只评估”止于建议。
