# Vision Harness

Vision Harness gives a coding Agent five direct work entries:

- `using-vision-harness` identifies the request, relevant project facts, authorization, and stopping point.
- `project-onboarding` finds real adoption gaps without creating a second project structure.
- `vision-management` (shown as **Vision**) conducts a real multi-turn discussion and records only authorized decisions.
- `agent-instructions` maintains root or local `AGENTS.md` guidance while preserving existing rules.
- `breakdown` turns an accepted vision into concrete product delivery planning and keeps its existing planning behavior.

The package is self-contained. Runtime rules are in `references/`; consumer-project facts remain in the consumer project. Installing or updating the plugin does not write `VISION.md`, `AGENTS.md`, plans, or custom project rules.

## Local installation

From a checkout containing this package, install the repository marketplace and then the plugin:

```bash
codex plugin marketplace add /path/to/Vison-Harness
codex plugin add vision-harness@personal
```

Start a new session after an update so the host loads the new Skill set. The package does not make a host claim merely because a Skill file exists; verify automatic loading with the target host when that distinction matters.

## Development assembly

The committed package is produced by the repository's deterministic `scripts/assemble_plugin.py`. It copies the four new source Skills and the existing Breakdown Skill, converts their project-relative references to package-local references, and derives the small runtime reference set from the repository's authoritative method/spec sources. Run it from the repository root before validation.
