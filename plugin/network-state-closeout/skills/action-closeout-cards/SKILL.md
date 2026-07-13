---
name: action-closeout-cards
description: >-
  Generate two separate Markdown closeout documents for a completed action, service setup, deployment, migration, troubleshooting session, or configuration change: a status card that states the final usable condition and a process card that preserves the implementation route, audit points, and troubleshooting entry. For network-related work, also produce a validated machine-readable handoff pair that network-state can reconcile into canonical private records and acknowledge with an ingestion receipt. Use when the user asks for status and process cards, closeout records, service-state documentation, an implementation-route card, post-action audit notes, or card-driven network-state maintenance.
---

# Action Closeout Cards

Create two documents with different responsibilities:

- Make the **status card** answer what the final state is now.
- Make the **process card** answer which technical route produced that state and where future diagnosis should begin.
- For network-related work, make the pair a structured evidence package for `$network-state`, not merely a human-readable summary.

Do not mix the two responsibilities.

## Close out the action

1. Confirm that the action has reached a final state and identify its service, requirement, version, host, entry point, configuration, and deliverable.
2. Read project-local instructions such as `AGENTS.md`. If an Obsidian project context index exists, read `01 项目入口与版本历史.md` and `04 当前范围与执行状态.md` before writing.
3. For network-related work, use `$network-state` when saved network facts are relevant or the cards contain durable network-state candidates. Let it autonomously maintain confirmed durable facts unless the user asked not to record them.
4. Inspect existing `docs/` naming and numbering. Reuse the project convention without renaming existing documents.
5. Read `references/card-templates.md` and create one status card plus one process card. For network-related work that is allowed to maintain network records, give both cards the same stable `Handoff ID`, set their roles to `status` and `process`, and start their ingestion state at `pending`. If the user explicitly asked not to record network facts for this task, omit the complete handoff sections and leave the private profile unchanged.
6. Validate every pair that contains a network-state handoff with `scripts/validate_card_pair.py`, then ask `$network-state` to reconcile it into canonical private records.
7. After reconciliation, update both writable cards with the same `applied`, `blocked`, or `skipped` receipt returned by `$network-state`, then validate the pair again. If the cards are read-only, leave the authoritative receipt in the private handoff ledger and report that the card copies were not updated.
8. Register links in an existing project status index when that convention already exists. For an Obsidian project context index, update `04 当前范围与执行状态.md`. Keep only the final service state and the two card links in the index.
9. Check separation, completeness, and sensitive information before reporting completion.

## Keep network state and cards separate

- Treat the private network profile as the only source of truth for current operational facts.
- Treat project cards as concise human-facing documentation and machine-readable evidence of one completed action.
- Copy only the minimum facts needed to understand the result, entry point, boundary, verification, architecture route, and troubleshooting entry.
- Do not duplicate a complete device inventory, address list, topology, raw logs, or configuration export into cards.
- Do not copy card prose into the private network profile. `$network-state` may reconcile only the reusable confirmed candidates declared in the handoff sections.
- When the project documentation is not confirmed private, redact exact endpoints and use device, service, path, or secret-manager references.
- When private GitHub synchronization is part of the action, record only its purpose, remote alias, branch, validation result, and final commit identifier. Never record a credential-bearing URL.

## Choose output paths

Follow the current project's convention. When no convention exists, use:

```text
docs/<action-or-service>-status-card.md
docs/<action-or-service>-process-card.md
```

If numbered documents already exist, use the next available number. Do not renumber older files.

## Exclude non-durable material

Do not include:

- command-by-command transcripts, installation logs, chat history, or raw debug output;
- temporary failures, speculative state, or discarded designs;
- passwords, tokens, API keys, private keys, cookies, recovery codes, one-time codes, subscription URLs, login artifacts, or secret values;
- full private network inventories or unnecessary exact endpoints.

Write only private configuration paths, environment-variable names, keychain aliases, or secret-manager references.

## Validate the cards

Confirm all of the following:

- A reader can understand the current usability and entry point from the status card within 30 seconds.
- A future agent can find the architecture, critical implementation decisions, audit points, and first troubleshooting checks from the process card.
- The status card contains no deployment narrative.
- The process card is not a command transcript.
- Both cards contain only final, confirmed, still-relevant information.
- No sensitive value, UUID, credential-bearing URL, or raw configuration is present.
- Any project status index, including `04 当前范围与执行状态.md`, contains only the final state and links to both cards.
- A network-related pair has matching handoff ID, ingestion state, and detail level; complementary card roles; and a complete receipt block.

Validate every pair that contains a network-state handoff before and after ingestion:

```bash
python3 <action-closeout-cards-skill-directory>/scripts/validate_card_pair.py \
  --status-card <status-card> \
  --process-card <process-card>
```

Use `rg` for a heuristic scan when available, then inspect every match manually:

```bash
rg -n "token=|password|passwd|api[_ -]?key|secret|cookie|BEGIN .*PRIVATE KEY|[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}" <status-card> <process-card>
```

## Report completion

Tell the user only:

- where the two cards were written;
- whether an existing project status index was updated;
- whether sensitive-information checks passed;
- for network-related work, the handoff ID and whether ingestion was applied, blocked, or skipped.
