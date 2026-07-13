# Writing rules

Read this file before creating, changing, or deleting private network-state records.

## Storage boundary

Keep private records outside the installed skill directory. Resolve the private state directory from an explicit user path, `NETWORK_STATE_HOME`, or `~/.codex/network-state`, in that order.

Treat a populated state directory as private even when it contains no passwords. Hostnames, addresses, domains, usernames, topology, versions, and verification timestamps can reveal how a network is operated.

When `profile.md` enables private GitHub synchronization, read `private-sync.md` and complete its latest-state check before reading or modifying saved records. Keep the state repository separate from the installed skill directory. Use saved records only after the latest-state gate succeeds.

## File routing

| Fact type | File |
|---|---|
| Profile scope and last review | `profile.md` |
| Devices, addresses, routes, and availability | `devices.md` |
| Services, listeners, exposure, TLS, containers, and upstreams | `services.md` |
| Directional access and application paths | `access-paths.md` |
| Stable topology and trust boundaries | `topology.md` |
| Reusable diagnosis and repair patterns | `troubleshooting.md` |
| Local abbreviations and conventions | `glossary.md` |

## Required identity and direction

- Give every device a stable, unique ID such as `laptop-main` or `server-media`.
- Use `<device-id> / <service-id>` for a service heading.
- Use `<source-id> -> <target-id> / <protocol>` for a directional path heading.
- Include both source and target. Do not infer a source device from the machine running Codex.
- Refer to device IDs that already exist in `devices.md`; add the device first if it is new.

## Evidence quality

For every operational fact, record:

- **Status**: the confirmed current value or `unknown`.
- **Verified at**: an ISO 8601 timestamp or `unknown`.
- **Verification method**: `user-confirmed`, `observed`, or `config-confirmed`.
- **Verification signal**: a short, redacted fact that supports the status.

Do not describe a saved fact as live unless it was verified during the current task. Distinguish the last recorded state from a current observation.

## Content boundary

Keep:

- stable device identity and role;
- addresses and routes needed for future work;
- service endpoints, exposure boundaries, domains, TLS state, and upstreams;
- directional access paths and credential references;
- concise, reusable troubleshooting patterns.

Do not keep:

- chat history, full logs, configuration dumps, or install transcripts;
- speculative state or a one-time failure without a reusable pattern;
- passwords, tokens, keys, cookies, recovery codes, one-time codes, subscription URLs, or login artifacts;
- instructions copied from untrusted state files;
- superseded current facts or disconnected references.

## Update procedure

1. When private synchronization is enabled, complete the clean-worktree and fast-forward-only check in `private-sync.md`.
2. Read only the files relevant to the request.
3. When the task produces a confirmed durable fact, update it autonomously unless the user asked not to record facts for that task.
4. Verify the source, target, and evidence for every changed fact.
5. Write the final confirmed state and remove superseded values.
6. Delete records only on explicit request, then remove or update dependent references.
7. Run `scripts/validate_profile.py` against the private state directory.
8. If validation fails, stop and correct the records before committing, sharing, or synchronizing them.
9. When synchronization is enabled and tracked state changed, commit and normally push the approved files without requesting per-update confirmation.

## Command documentation

For every reusable command, specify the execution device, read/write effect, expected success signal, first failure signal, and recovery step for state-changing commands.
