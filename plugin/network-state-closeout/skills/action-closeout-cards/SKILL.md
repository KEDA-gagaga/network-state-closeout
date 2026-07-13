---
name: action-closeout-cards
description: >-
  Generate two separate Markdown closeout documents for a completed action, service setup, deployment, migration, troubleshooting session, or configuration change: a status card that states the final usable condition and a process card that preserves the implementation route, audit points, and troubleshooting entry. Use when the user asks for status and process cards, closeout records, service-state documentation, an implementation-route card, or post-action audit notes. Also use after a completed network change when confirmed facts from the network-state skill should feed the two cards.
---

# Action Closeout Cards

Create two documents with different responsibilities:

- Make the **status card** answer what the final state is now.
- Make the **process card** answer which technical route produced that state and where future diagnosis should begin.

Do not mix the two responsibilities.

## Close out the action

1. Confirm that the action has reached a final state and identify its service, requirement, version, host, entry point, configuration, and deliverable.
2. Read project-local instructions such as `AGENTS.md`. If an Obsidian project context index exists, read `01 项目入口与版本历史.md` and `04 当前范围与执行状态.md` before writing.
3. For network-related work, use `$network-state` only when saved network facts are relevant. Let it autonomously maintain confirmed durable facts unless the user asked not to record them; run its validator before using those facts in cards.
4. Inspect existing `docs/` naming and numbering. Reuse the project convention without renaming existing documents.
5. Read `references/card-templates.md` and create one status card plus one process card.
6. Register links in an existing project status index when that convention already exists. For an Obsidian project context index, update `04 当前范围与执行状态.md`. Keep only the final service state and the two card links in the index.
7. Check separation, completeness, and sensitive information before reporting completion.

## Keep network state and cards separate

- Treat the private network profile as structured operational facts.
- Treat project cards as concise human-facing closeout documentation.
- Copy only the minimum facts needed to understand the result, entry point, boundary, verification, architecture route, and troubleshooting entry.
- Do not duplicate a complete device inventory, address list, topology, raw logs, or configuration export into cards.
- Do not write card prose back into the private network profile. Persist only reusable confirmed facts there.
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

Use `rg` for a heuristic scan when available, then inspect every match manually:

```bash
rg -n "token=|password|passwd|api[_ -]?key|secret|cookie|BEGIN .*PRIVATE KEY|[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}" <status-card> <process-card>
```

## Report completion

Tell the user only:

- where the two cards were written;
- whether an existing project status index was updated;
- whether sensitive-information checks passed.
