# Card templates

Use these templates as a structural baseline. Adapt labels to the project's language and conventions without merging the two cards.

## Status card

```markdown
# <Action or service> status card

## Current conclusion

- <One-sentence final conclusion>

## Service identity

| Item | Value |
|---|---|
| Service or action |  |
| Purpose |  |
| Entry point |  |
| Runtime location |  |
| Key configuration |  |
| Private configuration | <Path, variable name, keychain alias, or secret-manager reference only> |

## Current usability

- <Available, unavailable, partially available, or under observation>

## Verified results

- <Final valid verification result and verification time>

## Boundaries

- <What this does not affect>
- <Where this must not be treated as a default or replacement>

## Follow-up observation

- <Remaining user-experience or scheduled verification item, or none>
```

Exclude deployment steps, command lists, failed attempts, detailed tutorials, and sensitive values.

For network-related work, append this section before finalizing the card:

```markdown
## Network-state handoff

| Field | Value |
|---|---|
| Handoff ID | `<yyyymmdd-action-sequence>` |
| Card role | `status` |
| Ingestion state | `pending` |
| Detail level | `<private-or-alias-only>` |
| Verified at | `<ISO-8601 timestamp>` |
| Verification method | `<user-confirmed, observed, or config-confirmed>` |
| Target records | `<semicolon-separated target files and stable headings>` |
| Applied at | `unknown` |
| Applied targets | `none` |
| Network-state validation | `pending` |
| Network-state commit | `none` |
| Block reason | `none` |

### Durable state candidates

| Target | Field | Final value | Verification signal |
|---|---|---|---|
| `<target file and stable heading>` | `<field>` | `<confirmed current value>` | `<concise redacted signal>` |

### Ingestion receipt

Pending reconciliation by `$network-state`.
```

## Process card

````markdown
# <Action or service> process card

## Purpose

Preserve the implementation route, audit points, and troubleshooting entry. Do not reproduce a command log.

## Architecture flow

```text
client -> entry point -> service component -> data or configuration -> external dependency
```

## Critical implementation route

1. <Core approach and the decision that affected implementation>
2. <Deployment or runtime model>
3. <Domain, DNS, certificate, port, route, or network boundary>
4. <Configuration, secret reference, database, storage, or external dependency>
5. <Client integration>
6. <Verification method and final signal>

## Audit points

| Audit item | Current value or location | Diagnostic meaning |
|---|---|---|
| Entry point |  |  |
| Configuration |  |  |
| Secret storage | <Path, variable name, keychain alias, or secret-manager reference only> |  |
| External dependency |  |  |

## Troubleshooting entry

- <Symptom>: check <critical location or signal> first.

## Boundaries

- <Explicitly unaffected scope>
````

Exclude full commands, install logs, temporary debug output, click-by-click UI records, discarded designs, and sensitive values.

For network-related work, append this section before finalizing the card. Reuse the status card's handoff ID, state, detail level, timestamp, and verification method:

```markdown
## Network-state handoff

| Field | Value |
|---|---|
| Handoff ID | `<yyyymmdd-action-sequence>` |
| Card role | `process` |
| Ingestion state | `pending` |
| Detail level | `<private-or-alias-only>` |
| Verified at | `<ISO-8601 timestamp>` |
| Verification method | `<user-confirmed, observed, or config-confirmed>` |
| Target records | `<semicolon-separated target files and stable headings>` |
| Applied at | `unknown` |
| Applied targets | `none` |
| Network-state validation | `pending` |
| Network-state commit | `none` |
| Block reason | `none` |

### Durable route and troubleshooting candidates

| Target | Candidate type | Durable content | Verification signal |
|---|---|---|---|
| `<target file and stable heading>` | `<access-path, topology, dependency, or troubleshooting>` | `<confirmed reusable mechanism>` | `<concise redacted signal>` |

### Ingestion receipt

Pending reconciliation by `$network-state`.
```

After ingestion, set the same final state in both cards. For `applied`, fill `Applied at`, `Applied targets`, `Network-state validation`, and `Network-state commit`; for `blocked`, fill `Block reason`; for `skipped`, explain the no-change result in the receipt. Keep the private handoff ledger authoritative if the cards cannot be edited.

## Mapping confirmed network facts into cards

| Confirmed network fact | Status card | Process card |
|---|---|---|
| Device and service IDs | Service identity and runtime location | Architecture components |
| Current service status | Current usability | Only when it explains an audit point |
| User-facing entry | Entry point | First architecture hop and audit point |
| Verification time and redacted signal | Verified results | Verification method |
| Directional access path | Concise boundary when needed | Architecture flow |
| Exposure, TLS, route, proxy, or upstream | Boundary | Critical implementation route |
| Reusable troubleshooting pattern | Follow-up observation only when still active | Troubleshooting entry |
| Credential reference | Private configuration reference only | Secret-storage reference only |
| Private GitHub synchronization | Mention only when it affects current availability | Remote alias, branch, validation result, and final commit identifier |

Do not copy a full device list, address table, topology, or troubleshooting catalog. Use `Detail level: private` only when the destination is confirmed private and exact endpoints are operationally necessary. Otherwise use `alias-only`, which permits stable device, service, path, and secret-manager references but no exact IP address, MAC address, or concrete URL.
