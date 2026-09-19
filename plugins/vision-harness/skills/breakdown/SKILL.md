---
name: breakdown
description: Turn an accepted project vision into concrete product delivery planning, refine the next delivery batch after facts change, or review and revise an existing abstract plan. Use for product breakdown, milestone/FR planning, dependency and parallel-work planning, or planning migration; do not use to implement the planned product.
---

# Breakdown

Build a plan that keeps the complete confirmed goal visible while making only the next useful delivery batch implementation-ready.

Before acting, read the applicable project rules and the current sources of truth. For Vision Harness behavior, use [the Breakdown specification](../../references/breakdown-behavior.md); use [METHOD.md](../../references/shared-rules.md) for shared authorization, evidence, dependency, and completion rules. Do not copy those rules into the output.

## Establish the task

1. Identify whether the request is an initial breakdown, next-batch refinement, or review/revision of an existing plan.
2. State the requested result, allowed side effects, and stopping boundary. Read access never implies write authorization.
3. Read only the current facts needed for this decision: the project vision, applicable rules, accepted decisions, relevant issues/milestones, dependencies, and evidence. Prefer live project systems over handoff summaries.
4. Separate confirmed goals, candidate choices, assumptions, unknowns, deferred work, and non-goals. Ask only about a gap that changes the current product boundary or next decision.

## Produce concrete delivery planning

- Map every confirmed goal to a concrete product object, an explicit unresolved decision, or an existing work item that already carries it.
- Use objects native to the product. For a Plugin, consider actual Skills, necessary packaged material, tools, distribution entry points, and only evidence-backed Hooks. Do not force these objects onto a CLI, library, or application.
- Connect stage outcomes to user- or upstream-visible results, the deliverables that provide them, and evidence that could support the result. Planned validation is not evidence already obtained.
- Keep future stages coarse. Make the next batch specific enough to enter exploration, Spec, design, implementation, or validation without redefining the product.
- Reuse valid issues, milestones, identities, decisions, and evidence. Do not create a new layer or duplicate item merely to make the plan look complete.
- Do not require a fixed tree, fixed number of components, or one-to-one mapping among goals, FRs, components, milestones, and work items.

For each important dependency, name the missing result, the stage it blocks, and the condition that removes the block. Treat priority, parentage, and shared goals as distinct from dependency. When work can proceed in parallel, include the shared contract, modification boundaries, integration owner or unresolved ownership, integration order, and the checks to repeat on the combined candidate.

## Refine or review existing planning

When facts change, preserve unaffected goals, work identities, decisions, and evidence. Change only the affected next batch; do not rebuild the whole plan or expand distant work.

When reviewing a plan, check separately:

1. Do all confirmed goals still have an owner or explicit unresolved decision?
2. Are the real product entry points and deliverables visible, rather than only capability labels or renamed titles?
3. If every lower-level item finished, could the upper-level user result still be missing because integration, packaging, invocation, behavior, or evidence is absent?
4. Does each stage's evidence plan support the result it intends to claim?
5. Do recorded relationships and statuses match the current facts and actual operations?

Recommend retaining, revising, splitting, merging, replacing, or stopping existing items only where needed. Preserve valid commitments and history, and state where a still-valid goal moves when its old route stops. If the current plan is already usable and no fact changed, say so and point to the existing next step.

## Apply only authorized writes

In advice-only or review-only work, make no repository or project-system writes.

When planning writes are authorized:

1. Re-read each target and search for an equivalent existing object.
2. Preserve unrelated current content and handle concurrent changes instead of overwriting from an old snapshot.
3. Perform only the authorized planning changes.
4. Re-read bodies, native relationships, and states after writing.
5. If a result is unknown, query before retrying. If a tool cannot express the required operation, report the gap; do not imitate a native relation with prose or create a parallel state store.

Never infer authorization for code implementation, merge, release, global migration, deletion, or bulk rewriting from approval to plan.

## Finish

Keep these conclusions distinct:

- goal coverage;
- planning usability and the next actionable batch;
- actual project-system operations, including not requested, succeeded and re-read, failed, or unverified;
- unknowns, deferred work, evidence gaps, and the stopping boundary.

Before calling the plan usable, verify that its requested level of goals, deliverables, dependencies, and validation is sufficient. A usable plan is not an implemented product and does not grant permission to execute the next batch.
