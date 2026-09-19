---
name: vision-management
description: Conduct real multi-turn vision discussions, reuse or locally revise an existing vision, and persist only decisions the user has authorized.
---

# Vision (Vision Management)

Use this entry to form, inspect, or revise a project's long-term vision. Read the project's authoritative facts and the [vision behavior rules](../../../specs/vision/spec.md) plus [shared operating rules](../../../METHOD.md) before acting. The package's own vision is method material, never a consumer-project decision.

## Establish the current decision

1. Identify the consumer project, the user's requested mode, the exact allowed side effects, and the stopping point. “Discuss”, “review”, and “organize” do not automatically authorize a file write.
2. Locate an existing `VISION.md` or organization-level vision. Reuse it when it is sufficient; do not create a second authority because its filename or headings differ.
3. Read only the facts that can change the current decision. Separate confirmed decisions, proposals, assumptions, unknowns, deferred work, non-goals, and evidence. Do not import the package's goals or examples into the project.

## Run the conversation

Keep a small working record in the conversation, not a private state file:

```text
Confirmed: user decisions and facts that were actually checked
Open: questions whose answers change the current user/problem/result/boundary
Suggested: options with reasons, still awaiting the user's decision
Deferred: useful but irrelevant to the current decision
```

For each round:

1. Pick the smallest unanswered decision that can change the current direction. Explain its consequence in plain language and ask one question or a small related group.
2. If the answer is required, stop the turn and wait for the user's answer. Never answer your own question, treat silence as consent, or write a recommendation as confirmed.
3. After an answer or new evidence, update only the affected questions. Keep unaffected agreement; do not restart the whole interview for a local change.
4. Check facts that can be found in the project or permitted tools yourself. If a fact cannot be checked, say exactly what is missing instead of making the user choose whether an unverified claim is true.
5. Offer a recommendation only with its reason and label it as a recommendation. The user must make the product trade-off.

Do not use a fixed questionnaire, number of rounds, decision-tree display, or “ask everything before stopping”. Stop clarifying when the current decision has enough of: primary users and problem, desired result, known major capabilities, product boundary and non-goals, success observation, and the unknowns that still matter for the requested next step. Irrelevant future detail must not block a usable current decision.

## Reuse and local revision

- With an adequate existing vision and no new evidence, summarize the applicable agreement and proceed to the requested next method without rewriting it.
- When new evidence changes a premise, state the fact, the inference, and the affected scope. Retain valid goals and historical decisions; stopping one implementation route does not silently cancel the goal it carried.
- Only revise the authorized section or authority. Preserve unrelated content and the project's existing organization. Do not shrink the product goal to make an implementation easier.
- A high-level comparison may end with options and open decisions. It is not an accepted implementation plan.

## Persist only when authorized

When the user explicitly authorizes recording and the relevant decisions are clear:

1. Read the complete current target and confirm it is still the intended authority.
2. Make the smallest edit that records the confirmed understanding; preserve unrelated rules and unknowns.
3. Write only the named target, then read it back and report what actually changed.

If the user asked only to discuss or review, do not write a vision, create planning objects, modify code, or request a ceremonial second confirmation. Writing permission does not give permission to decide product direction. After a successful authorized write, stop at the requested boundary; do not automatically invoke `breakdown`.

The final response must distinguish the conversation's shared understanding, recommendations, unresolved unknowns, actual file writes, and what remains unverified. A file's presence or a polished summary is not evidence that an unconfirmed direction was accepted.
