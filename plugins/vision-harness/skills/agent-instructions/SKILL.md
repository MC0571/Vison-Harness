---
name: agent-instructions
description: Create, maintain, or correct root and local AGENTS.md guidance while preserving existing rules and verifying real command and host-loading facts.
---

# Agent Instructions

Use this entry when a project needs Agent guidance created or corrected. Read the [project-context behavior rules](../../references/project-context-behavior.md) and [shared operating rules](../../references/shared-rules.md), then inspect the target project before writing.

## Find the real instruction surface

1. Identify the target root and all applicable `AGENTS.md` files from the host's documented lookup behavior. A file in a directory is not automatically loaded by every host.
2. Read the complete current root and relevant local files. Preserve existing safety, review, authorization, and project-specific rules. Rules already owned by a Spec or architecture document should be referenced rather than copied.
3. Determine whether the requested behavior is a repository-wide rule or a true local difference. Put the former in the root file and the latter in the narrowest applicable directory. If there is no local difference, do not create a local file.
4. Discover build, test, lint, and run commands from real project configuration and scripts. If no command is available, report that fact; do not invent one or turn a guessed command into a requirement.

## Make a minimum authorized change

- For read-only review, report gaps and suggested text without changing files.
- For an authorized edit, name the exact target files first, then preserve unrelated content and add only the missing rule or correction. Do not weaken a rule to make the current task pass.
- Keep the distinction explicit between (a) a file being present, (b) an Agent reading it manually, and (c) the host automatically loading it. Verify (c) with the actual host when that claim matters; never infer it from the filename.
- Do not edit global trust, permissions, credentials, hooks, or unrelated project configuration as a shortcut.
- After writing, reread every target and report the actual content/command evidence. If the target changed concurrently or the update result is unclear, preserve the newer content and stop the affected write rather than overwriting it.

Finish with:

```text
Scope: root or local instruction surface
Existing rules retained: what was preserved
Change: exact files and local differences addressed
Commands: only commands found in project configuration
Loading: manual-read and host-load facts kept separate
Verification: write-back/read-back or read-only evidence
Stop: the remaining boundary or unknown
```
