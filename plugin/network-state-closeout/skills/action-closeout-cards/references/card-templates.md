# Card templates

Use only the template justified by the decision in `SKILL.md`. Never instantiate the process template until the process-card evidence gate passes. Delete unused sections; do not leave placeholders.

## Status card

```markdown
# <Action or service> status card

## Current conclusion

- <One-sentence result>

## Identity

| Item | Value |
|---|---|
| Service or action |  |
| Purpose |  |
| Entry point |  |
| Runtime location |  |
| Key configuration |  |
| Private configuration | <Path, variable, or credential alias only> |

## Current usability

- <Available, unavailable, partially available, or under observation>

## Verified result

- <Final valid result and time>

## Boundaries

- <What this does not affect or replace>

## Follow-up

- <Remaining observation or none>
```

## Process card

Use this only for a process supported by direct observation or reliable records.

```markdown
# <Action or service> process card

## Evidence basis

- <Task actions, configuration diff, change record, runbook, or user-provided process notes>

## Goal and result

- <What the action set out to change and what it actually achieved>

## Actual technical route

1. <Evidence-backed change or decision>
2. <Evidence-backed implementation step or dependency>
3. <Evidence-backed integration and verification>

## Key decisions and constraints

- <Why this route was used, only when recorded>

## Changed locations and dependencies

| Item | Actual location or dependency | Diagnostic meaning |
|---|---|---|
| Entry point |  |  |
| Configuration |  |  |
| Credential reference | <Path, variable, or alias only> |  |
| External dependency |  |  |

## Verification and troubleshooting

- Verification: <Observed result>
- If <symptom>, check <recorded critical location or signal> first.

## Boundaries

- <Explicitly unaffected scope>
```
