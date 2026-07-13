---
name: action-closeout-cards
description: Create separate Markdown status and process cards when the user requests closeout documentation or a completed deployment, migration, repair, or configuration change is worth long-term audit. Do not use for simple network-state edits; update the matching network card directly.
---

# Action Closeout Cards

Create two documents:

- Status card: current result, entry point, usability, verification, and boundaries.
- Process card: implementation route, audit points, dependencies, and troubleshooting entry.

## Lightweight workflow

1. Confirm the action is complete.
2. Read project instructions and existing document naming; load only necessary context.
3. Read `references/card-templates.md` and write the two cards separately.
4. Exclude command transcripts, chat history, temporary failures, full logs, and discarded designs.
5. If the action confirmed durable network facts, use `$network-state` to update the matching private network cards directly.
6. Update an existing project status index only with the final state and card links.
7. Scan both cards for credentials and unnecessary private details.

Simple changes to an address, port, availability, or verification time do not need closeout cards.

## Output paths

Follow project conventions. When none exist, use:

```text
docs/<action-or-service>-status-card.md
docs/<action-or-service>-process-card.md
```

## Security

Never write passwords, tokens, API keys, private keys, cookies, recovery codes, one-time codes, subscription secrets, UUIDs, or credential-bearing URLs. Use configuration paths, variable names, keychain aliases, or password-manager references.

Use `rg` for a quick heuristic scan, then inspect matches:

```bash
rg -n "token=|password|passwd|api[_ -]?key|secret|cookie|BEGIN .*PRIVATE KEY|[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}" <status-card> <process-card>
```

Report card paths, project-index changes, network-card updates, and the sensitive-information check.
