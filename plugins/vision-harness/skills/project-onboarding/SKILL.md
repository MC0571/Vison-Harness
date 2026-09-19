---
name: project-onboarding
description: Help a new or existing project adopt Vision Harness by identifying real gaps and making only the authorized, minimum integration changes.
---

# Project Onboarding

Use this entry when a project is new to the method or when the user asks whether an existing project needs to be connected. Read the [project-context behavior rules](../../references/project-context-behavior.md) and [shared operating rules](../../references/shared-rules.md) before assessing gaps. The result is a gap assessment and, when explicitly authorized, the smallest useful changes. It is not a template generator.

## Inspect before changing

1. Confirm the target project and read its applicable `AGENTS.md` files, existing `VISION.md` or organization-level equivalent, architecture/Spec entry points, current planning source, and relevant work item. The package's own examples are not project facts.
2. Discover real commands and host conditions from files that exist in the target project (`package.json`, `pyproject.toml`, `Cargo.toml`, `Makefile`, CI configuration, and documented scripts as applicable). Never invent a test or build command.
3. Record which of these are already sufficient: a readable long-term goal, a current planning entry, project instructions, and an actual host loading/install path. Distinguish “file exists”, “an Agent can read it”, and “the host loads it automatically”.
4. Report each remaining gap with its effect on the requested work. A missing remote integration or unrelated future Skill is not a reason to rebuild a usable project.

## Choose the smallest next action

- Reuse an existing vision, directory layout, issue/plan, and rule file when they already carry the needed fact. Do not create a second `VISION.md`, parallel roadmap, or private state file.
- If a goal is unclear, hand the relevant gap to `vision-management`; do not fill the user's product decision from the package's vision.
- If a plan is missing but the goal is sufficient and planning is requested, hand off to `breakdown`; do not turn onboarding into implementation.
- If a rule is missing or a true local difference exists, hand off to `agent-instructions`. No local difference means no local `AGENTS.md`.
- If the request only asks for assessment, stop without writing. If writing is authorized, name the exact files and preserve unrelated rules before writing and reread each file afterward.
- Installing or updating this package must not overwrite the consumer project's vision, instructions, plans, custom rules, or source tree. If a proposed action would do so, stop and report the boundary.

## Finish with an adoption result

Return:

```text
Target: project and working directory
Reused: existing authoritative facts and paths
Gaps: only gaps that affect this request
Allowed change: exact files/objects, or “read-only”
Next method: the direct Skill or action that owns the gap
Stop: the boundary for this onboarding turn
```

Do not claim the project is “adopted” merely because a package installed, a file exists, or a host entry was suggested. The project is ready only to the extent supported by the facts and checks actually performed.
