# Vision Harness

[English](README.en.md) | [中文版](README.md)

**Helps users clarify what their software project is trying to achieve, so coding Agents can deliver reliably and efficiently without losing sight of the overall goal.**

Vision Harness is a software engineering method for AI coding Agents. It integrates into existing coding Agent environments through Plugins and Skills.

It is not a new project management platform, nor a process that requires you to maintain large amounts of documentation by hand. It mainly helps users and Agents do five things:

1. Turn vague ideas into project visions sufficient to support planning;
2. Keep the full goal visible while detailing only the part that actually needs to move forward now;
3. See dependencies clearly and arrange sensible serial, parallel, and integration work;
4. Choose Specs, architecture, TDD, review, and quality verification based on actual changes, while suppressing unjustified complexity;
5. Use authorization and evidence to decide when to continue, finish, adjust, or stop.

The complete project vision is in [VISION.md](VISION.md), and the detailed method rules are in [METHOD.md](METHOD.md).

## Installation and quick start

Vision Harness can be installed as a complete Codex Plugin package, or individual Skills can be installed in a consuming project. Choose one to avoid having two sources for the same Skill.

### Install the entire Plugin

Run this in the Codex CLI:

```bash
codex plugin marketplace add MC0571/Vison-Harness --ref main
codex plugin add vision-harness@MC
```

Add the marketplace above first; after adding `MC`, you can also use the Codex UI to select `vision-harness` in that marketplace. After installation, start a new session so the host loads the new Plugin. See [Plugin usage instructions](PLUGIN.md) for package installation and maintenance commands.

### Install selected Skills

The default scope of third-party `npx skills` is the current project; the following command installs all Vision Harness Skills for Codex:

```bash
npx skills add https://github.com/MC0571/Vison-Harness/tree/main/skills --skill '*' -a codex
```

To install only selected Skills, use the short names in their frontmatter, for example:

```bash
npx skills add https://github.com/MC0571/Vison-Harness/tree/main/skills --skill review breakdown -a codex
```

Add `-g` for user-level installation. Do not use `--all`: it installs every discovered Skill to every Agent. `--skill` uses the short name from `SKILL.md` frontmatter (for example, `review`), not the `Vision-Harness: Review` label shown in the installation UI. Every Skill directory contains complete method resources; `npx` does not require publishing or installing this repository's npm package or preparing a Python environment. Start a new session after installation.

If the host does not support Plugin or `npx skills`, manually copy the complete directory following [Copy a single Skill](PLUGIN.md#单-skill-复制). This is a fallback installation path and does not require Python.

### Work entry points

| Independent result | Skill |
| --- | --- |
| Bounded context recovery and identifying the next step | using-vision-harness |
| Adoption gaps and minimal integration | project-onboarding |
| Vision formation, inspection, and revision | vision-management |
| Whole-product / rolling planning, single-item shaping, and delivery coordination | breakdown |
| Long-term behavioral agreements or a conclusion that no change is needed | spec-development |
| Architecture impact, technical approach, and necessary ADR | technical-design |
| TDD implementation, defect repair, or diagnosis | tdd-development |
| Independent Spec / Code / PR review | review |
| Direct execution, reuse, or audit of evidence | change-verification |
| Artifact, PR, merge, release, or closure | release-delivery |
| System drift diagnosis and bounded correction | project-convergence |
| Agent guidance and reviewer configuration | agent-instructions |

See [Product architecture](ARCHITECTURE.md) and [development assembly and checks in the Plugin usage instructions](PLUGIN.md#研发装配与检查) for architecture and maintainer assembly and check instructions.

## Starting from a vague idea

Users can enter with only an incomplete idea; they do not need to prepare `VISION.md` in advance.

For example, the experience below requires actually waiting for the user's answer; the Agent does not fill in the conversation itself:

```text
User:
I want to build a project that helps teams run and evaluate AI Agents, reusing the tools our team already has.
Let's discuss the goal first; do not create implementation tasks.

Agent:
Does “run” mean providing a runtime environment, or inspecting and guiding an existing environment?
This changes the product's primary responsibility. Given your wish to reuse existing tools,
I suggest considering the latter first, but you need to confirm the tradeoff.

User:
Guide the existing environment without taking over runtime operations. It is mainly for people who maintain projects over the long term.

Agent:
Clear: the users are long-term maintainers; we are not building a runtime.
What needs to be decided next is the task they find hardest, not the deployment approach.
Which real failures are most worth solving first?
```

The Agent should independently verify checkable facts and ask only about decisions that affect current tradeoffs; recommendations are not user answers. It should not repeat known questions, and should reopen only the relevant discussion when premises change. Once understanding is sufficient, it should summarize decisions and unknowns; when authorized to record them, it should save them in the project's existing authoritative vision entry, and when the interaction is only a discussion, it should end at the summary. Questionnaires, fixed round counts, and extra confirmation procedures are not required.

Vision Harness should help users form a valid `VISION.md`, but “valid” does not mean long or complete with every heading.

It only needs enough to support subsequent tradeoffs: the users and problem, expected outcomes, main capabilities, product boundaries, explicit non-goals, signs of success, and key unknowns still to validate.

Once these are sufficient, move to the next step instead of interviewing indefinitely for the sake of completeness.

## From vision to work planning

Vision Harness does not convert a single vision straight into a large number of engineering tasks. It should first connect goals, outcome evidence, and concrete product deliveries, then progressively detail near-term work.

Using Vision Harness itself as an example, the planning method can be expressed as follows (this is a method example, not an acceptance record for the current version):

```text
VISION
  ↓
Stage goal:
Breakdown can turn a vision into concrete product planning that someone else can take over
  ↓
Outcome evidence:
- Users do not need to translate abstract capabilities into product components again
- A new Agent can continue directly to the next layer of breakdown
  ↓
Concrete product components:
- Breakdown Skill
- Necessary reference materials
- Host integration and Hook (only the parts confirmed necessary after validation)
- Behavioral evaluation
  ↓
Milestone
  ↓
FR / Issue
  ↓
Current batch detailed enough to enter Spec / implementation
```

Concrete product components should be visible in planning; implementation details can be decided incrementally. Do not omit the primary deliverables merely to avoid designing ahead.

Breakdown keeps its existing name and handles overall planning and rolling refinement; the candidate name roadmap-planning should not generate another synonymous entry. Repository-level acceptance and actual distribution, single-item shaping, and execution-time coordination are accepted separately. Hooks are selected based on specific automatic-triggering needs; they are not components every Skill must configure.

Confirmed but deferred capabilities should remain traceable, but every detail does not need its own Issue. If an existing suitable capability Issue covers it, do not create a duplicate.

## Choose capabilities by work

The regular package's twelve entry points are not a fixed pipeline. A direct request for a piece of work can enter its corresponding Skill directly; cross-cutting methods load conditionally inside the entry point.

| User request | Entry point and stopping point |
| --- | --- |
| “Continue this Issue” | With an explicit implementation scope, enter tdd-development directly; do not force a repeat of vision or project onboarding |
| “Integrate an existing repository with this method” | project-onboarding checks the real gaps and reuses facts that are already sufficient |
| “How far should this Issue go?” | breakdown's single-item mode organizes scope and completion conditions; it does not replan the whole product |
| “How should these items be parallelized and integrated?” | breakdown's coordination mode handles real dependencies, modification boundaries, and a unified candidate |
| “Review only the Spec / code / PR” | The unified review forms a judgment for the object; review-only does not automatically fix, merge, or publish |
| “Validate this candidate” | change-verification runs or reuses evidence proportionate to risk |
| “These implementations are too complex” | tdd-development loads the complexity method for code changes; technical-design handles long-term design issues; project-convergence handles system governance burden |
| “Establish/maintain AGENTS or reviewer configuration” | agent-instructions maintains project differences without requiring a fixed file bundle |

For example, when technical design encounters an unknown that could overturn the approach, it no longer switches to a standalone Assumption Skill; it loads the key-assumption method into the current design. When Review finds that old evidence no longer covers the current head, it verifies only the affected portion again.

If the existing facts are sufficient, move forward; do not expand upfront work because long-term planning is incomplete, an unrelated reference was not loaded, or there are not enough documents.

## Help arrange dependencies and parallel work

Parent and child Issues indicate work ownership only; they do not automatically indicate execution order. Priority is not the same as dependency.

Vision Harness should help users and Agents explain:

- which piece of work truly needs another result before it can continue;
- whether the dependency blocks starting, integration, acceptance, or release;
- which preparation can happen first;
- which work can run in parallel;
- what conventions parallel work shares and what each piece is allowed to modify;
- who will integrate the work, in what order, and revalidate it on the same candidate result.

For example:

```text
Current goal: add “pause task”.

Align first:
- Pause state and transition rules
- External call contract

Can run in parallel:
- Executor handles the pause request
- Caller adds a pause entry point
- Prepare tests for the interactions among pause, resume, and cancel

Before integration:
- Merge into the same candidate version
- Verify the real call path
- Check conflicts between pause and cancel
```

Parallelism is not the goal. If coordination cost, shared modification conflicts, or final integration risk exceed the benefit, reduce parallel work.

## Taking over an existing project

For an existing project, Vision Harness should not rebuild a separate directory structure and process.

A typical interaction can be simple:

```text
Continue with #37.

Agent:
I will first read the current Issue, related Specs, applicable AGENTS.md, architecture conventions, and existing verification.

#37 is already clear:
✓ Goal and current scope
✓ Related Spec
✓ Authorization allows code and test changes
✓ No unresolved prerequisites

This does not change the long-term architecture, so no new ADR is needed.
The information is sufficient; I will enter implementation directly instead of replanning the whole project.
```

If the same method is run again while project facts have not changed, Vision Harness should not generate duplicate Issues, duplicate Specs, duplicate review material, or meaningless documentation updates.

## Authorization scope determines what an Agent can do

Knowing what the next step should be and being authorized to execute it are two different things.

For example:

```text
You:
Evaluate whether we should replace the current cache approach; give advice only, and do not change the code.

Agent:
I will investigate the existing constraints, risks, and alternatives.
This round can read and analyze, but it will not create an implementation Issue, modify product code, or submit a PR.
```

If the user has explicitly authorized “complete this Issue, submit it to a separate branch, but do not merge”, the Agent should proceed continuously within that scope without reconfirming each step; it should stop at the merge boundary.

## Where facts live in a project

Vision Harness does not build its own state database. Each fact is maintained in one authoritative location, and other places reference it.

| Content | Common location |
| --- | --- |
| Project long-term goal | `VISION.md` or the project's existing authoritative vision entry |
| Roadmap, Milestone, priority, owner, and work status | GitHub |
| Capabilities, features, deferred work, parent-child relationships, and dependencies | GitHub Issue |
| Long-term behavioral rules | Spec |
| Current long-term architecture | `ARCHITECTURE.md` or an architecture document |
| Rationale for major long-term technical decisions | ADR |
| Technical approach for one change | GitHub |
| Execution work needing independent arrangement, collaboration, or acceptance | GitHub child Issue |
| Project-level Agent work conventions | `AGENTS.md`, layered as the project requires |
| Review method | The project's existing review conventions, Skill, or host-supported configuration |
| Current implementation | Code |
| Executable guarantees | Tests / Schema / Contract |
| Record of one review, acceptance, or authorization | The corresponding Issue, PR, review record, or existing project artifact |

By default, Vision Harness does not require maintaining a `ROADMAP.md`, `tasks.md`, or its own `state.yaml` in parallel with GitHub. Pure navigation, automatically generated views, or explicitly non-authoritative summaries in existing projects can remain as long as they do not become another source of facts that must be synchronized by hand.

A project might look like this:

```text
/
├── VISION.md
├── AGENTS.md                    # When repo-wide Agent conventions exist
├── ARCHITECTURE.md              # When long-term architecture needs to be documented
├── specs/
│   ├── execution-engine/
│   │   ├── spec.md
│   │   └── state-model.md
│   └── authorization/
│       └── spec.md
├── docs/
│   ├── adr/
│   └── review/                  # When the project genuinely needs long-term review rules
│       ├── spec-review.md
│       ├── code-review.md
│       └── pr-review.md
├── .codex/
│   └── agents/                  # When using Codex sub-Agents and actually needed
├── src/
└── tests/
```

This is one possible organization, not a fixed template.

## Handling a concrete Issue

Vision Harness selects the methods needed from the current state, rather than mechanically applying the full process.

```text
Issue
  ↓
Confirm this round's commitments and authorization
  ↓
Read goals, rules, and related facts sufficient for the current decision
  ↓
Check actual dependencies and key unknowns
  ↓
Update only the Spec / architecture / project conventions affected by the current changes
  ↓
Choose serial, parallel, and integration modes
  ↓
Execute TDD in behavioral slices
  ↓
Perform review and verification proportionate to risk
  ↓
Check this round's commitments, evidence, and authorization boundaries
  ↓
Continue / deliver / adjust / stop
```

If this is only an internal refactor, it may not require a Spec change at all.

If a technical choice will constrain multiple follow-on features over the long term, consider recording an ADR. Ordinary implementation choices do not need one.

If the existing facts are sufficient, move forward; do not expand upfront work because long-term planning is incomplete or unrelated documents are missing.

## Vision Harness also helps reduce complexity

“More complete” and “safer” are not automatically reasons to add engineering complexity.

When an Agent adds an abstraction, compatibility path, defensive logic, or process requirement, it should be able to answer:

> What confirmed need, credible risk, or explicit maintenance need does this complexity serve? Why is a simpler solution insufficient?

Vision Harness should point out:

- When behavior has not changed, no new Spec is needed;
- When an existing Issue already covers a deferred capability, no duplicate Issue is needed;
- When the existing architecture can directly support the current feature, no new ADR is needed;
- Style preferences or speculative future needs should not automatically become blockers;
- When valid evidence has not been affected by the current changes, do not rerun everything without a reason.

But “simplification” is not an excuse to remove necessary permission checks, data protection, error handling, or real quality verification.

## Why all-green tests do not always mean done

Tests can only prove that the behavior already written down passes.

If the Spec requires:

```text
- It can time out
- After timing out, it cannot become “completed” again
- The timeout state must persist
```

If the Agent writes tests for only the first two items, all tests can be green while one item is still missing.

Conversely, if the current scope and necessary verification are satisfied, the delivery should not be rejected merely because the long-term capability still has future content.

Therefore, Vision Harness requires conclusions to match the level of the commitment:

- An exploratory task being complete does not mean the feature has been delivered;
- An accepted Spec does not mean the code has been implemented;
- A completed current slice does not mean the long-term capability is complete;
- An incomplete long-term capability does not mean the current version cannot be delivered;
- A passed review does not automatically mean merge or release authorization has been obtained.

## What Vision Harness does not do

Vision Harness does not provide a dashboard, visualization, roadmap database, its own Issue tracker, or its own workflow state engine.

It does not force every project to generate the same Spec, `AGENTS.md`, or review files; it does not turn every technical choice into an ADR; and it does not require all work to pass through a fixed number of reviewers or sub-Agents.

It is a methodology tool that helps Agents judge and advance work more accurately, rather than another project management tool.
