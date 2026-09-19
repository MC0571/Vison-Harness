---
name: using-vision-harness
description: Identify the current project task, recover only the facts and authorization it needs, and choose a suitable Vision Harness method without acting as a router or scheduler.
---

# Using Vision Harness

Use this entry when a new request or a fresh session needs to determine what work is actually being requested. Read the [project-context behavior rules](../../../specs/project-context/spec.md) and [shared operating rules](../../../METHOD.md) before choosing a method. It returns a bounded handoff to the relevant work; it does not perform that work.

Before choosing a method, do the following in order:

1. Identify the consumer project, working directory, current request, and the requested stopping point. Treat the installed package as method material, not as the consumer project's product facts.
2. Classify the request: high-level discussion, vision work, project onboarding, planning, implementation, review, verification, or delivery. Choose only the smallest applicable method.
3. Read the consumer project's authoritative sources needed for that choice: its `AGENTS.md`, `VISION.md` or equivalent, relevant Spec, current work item, and real tool/configuration entry points. Do not scan unrelated history merely because it exists.
4. Separate confirmed decisions, proposals, assumptions, unknowns, deferred work, evidence, and authorization. A review result, CI status, tool access, or issue state is not write permission.
5. State the next method, the allowed action, the facts still missing, and the stop boundary. If a required method is not installed, say so instead of pretending that it ran.

The output should make this handoff explicit:

```text
Task: what this request asks for
Sources: authoritative files/objects and versions actually read
Authorization: read, discuss, write, or another exact scope
Method: the next direct Skill or bounded action
Missing: only facts that change the next decision
Stop: where this entry returns control
```

Rules:

- This is a recognition and handoff entry, not a dispatcher, workflow engine, state store, or automatic permission grant.
- A clear existing issue can go directly to its work Skill; do not repeat onboarding or vision discovery when the facts are already sufficient.
- This package currently installs only `using-vision-harness`, `project-onboarding`, `vision-management`, `agent-instructions`, and `breakdown`. Other architecture responsibilities may be referenced as future work, but an absent Skill must be reported as unavailable rather than treated as a successful handoff.
- Directly called work Skills must repeat their own authorization and shared-rule checks. Never use this entry as the sole safety gate.
- Recommendations remain recommendations. Do not turn silence, readiness, a parent issue, or a passing review into a product decision or implementation authorization.
- If the request is advice-only, stop after the bounded advice. Do not create files, issues, plans, or commits.
- If the request is authorized implementation, the authorization still ends at its stated boundary; merge, release, and unrelated project changes require their own authorization.
- A fresh session must recover from persistent consumer-project facts. Do not rely on an old transcript, hidden handoff, source checkout, or an uninstalled copy of a Skill.
- When a user changes a premise, reopen only the affected decision and retain unaffected facts. When facts are sufficient, stop rather than inventing more ceremony.
