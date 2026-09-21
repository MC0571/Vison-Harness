# Evidence Methods

This runtime reference is generated from the repository's accepted method and behavior sources. It is intentionally self-contained; edit the source documents and rerun the assembly instead of hand-editing this file.

## 10. 用适用证据判断完成和交付

“有证据”不等于“这个证据能支持任何结论”。

验收结论必须受证据的以下范围约束：

- 对应对象或构件；
- 代码或文档版本；
- 运行环境；
- 实际使用路径；
- 行为覆盖范围；
- 证据是本轮直接执行、合理继承，还是对已有结果的审计。

例如：

- 单元测试通过，证明对应内部行为；
- Contract 验证通过，证明相应接口契约；
- 正式安装成功，证明安装路径；
- 真实 Agent 从正式入口完成任务，才能支持相应真实使用路径结论。

这些结论不能互相替代。

旧证据可以复用，但必须能够说明当前变化没有影响它支持的结论。受影响的部分重新验证；无关部分不为了“更完整”全部重跑。

一次工作结束时，还要判断完成的是哪一层承诺，不能只说“Done”。

同样，条件已经满足时应该允许继续和交付：

- 远期能力未完成，不自动阻塞本版；
- 无关文档缺失，不阻塞当前工作；
- 非相关未知尚未解决，不阻塞已有明确约束下的实现；
- 没有新事实时，不应继续生成治理改动。

---
