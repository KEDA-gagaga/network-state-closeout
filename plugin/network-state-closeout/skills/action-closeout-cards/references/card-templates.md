# Card templates

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

````markdown
# <Action or service> process card

## Purpose

Preserve the implementation route, audit points, and troubleshooting entry without reproducing a command log.

## Architecture flow

```text
client -> entry point -> service component -> data or configuration -> external dependency
```

## Critical route

1. <Core approach>
2. <Deployment or runtime model>
3. <Domain, certificate, port, route, or network boundary>
4. <Configuration, credential reference, storage, or dependency>
5. <Client integration and final verification>

## Audit points

| Item | Current value or location | Diagnostic meaning |
|---|---|---|
| Entry point |  |  |
| Configuration |  |  |
| Credential storage | <Path, variable, or alias only> |  |
| External dependency |  |  |

## Troubleshooting entry

- <Symptom>: check <critical location or signal> first.

## Boundaries

- <Explicitly unaffected scope>
````
