# Review Methods

This runtime reference is generated from the repository's accepted method and behavior sources. It is intentionally self-contained; edit the source documents and rerun the assembly instead of hand-editing this file.

## 9. 按对象组织审查，而不是机械增加审查轮次

实施者自检、自动测试、独立审查和最终验收是不同判断。

必要时，审查应由能够独立形成判断的 reviewer 完成：直接读取当前候选变更、相关规则和证据，而不是只复述实施者的完成摘要。

但并不是所有工作都需要多人、多模型或多 Agent。审查强度应与风险、影响和项目规则相称。

三类常见审查对象是：

### Spec 审查

关注：

- 当前承诺是否被准确表达；
- 行为、边界、异常和约束是否清楚；
- 是否存在冲突、遗漏或不可验证要求；
- 是否擅自扩大或缩小范围。

Spec 合理不能证明代码已经实现。

### 代码审查

关注：

- 实现是否正确；
- 是否满足相关 Spec 和项目约定；
- 是否破坏架构；
- 是否引入没有依据的复杂度；
- 测试是否真正覆盖风险。

代码看起来正确不能证明正式交付路径已经验证。

### PR 审查

关注当前候选变更是否具备本次合并或交付所需的：

- 范围；
- 证据；
- 必要审查；
- 授权；
- 受影响检查结果。

PR 审查不机械重做前面全部工作，而是确认这些结论是否仍适用于当前候选版本。

审查通过不能自动产生合并、发布或关闭上层长期能力的授权。

修复后的重验只扩大到受影响范围；没有依据时不要求重新执行所有昂贵验证。

---
