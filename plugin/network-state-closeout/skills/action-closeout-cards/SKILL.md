---
name: action-closeout-cards
description: Create only evidence-backed Markdown status and/or process cards for a completed action when closeout documentation has lasting value. Decide each card independently. Do not create process cards for simple network-state edits, discovery or import of pre-existing network structure, current configuration without recorded history, or any process that would need to be reconstructed or invented.
---

# Action Closeout Cards

Create no card by default. Judge the status card and process card independently; they are not a required pair.

## Decide what is justified

- **Neither card**: use for simple facts, routine verification, discovery or import of pre-existing structure, incomplete work, or results with no lasting closeout value.
- **Status card only**: use when a completed result, entry point, usability, verification, or boundary is worth a durable summary.
- **Process card only**: use rarely, when the user asks for a technical route record and reliable process evidence exists, but a separate operational status summary adds no value.
- **Both cards**: use only when the final state and the recorded implementation route each have independent future value.

Current configuration proves current state, not how it was reached. Never infer chronology, commands, decisions, failures, or implementation steps from an existing Nginx, Docker, SSH, VPN, VPS, or topology configuration. An explicit request for a process card does not authorize fabrication; if evidence is missing, omit the process card and say why.

## Process-card evidence gate

Create a process card only when the action was performed or observed in the current work, or reliable source material records the actual process. The available evidence must support the real change, technical route, important decision or constraint, changed locations or dependencies, and verification or troubleshooting entry.

Generic best practices, a template, the current end state, and guessed intermediate steps are not process evidence. Do not create a placeholder process card or fill one mostly with `unknown`.

## Lightweight workflow

1. Confirm the action is complete and identify the available evidence.
2. Decide independently whether a status card, process card, both, or neither is justified.
3. If neither is justified, update any confirmed durable network facts through `$network-state` and stop the card workflow.
4. Read `references/card-templates.md` and use only the selected template sections.
5. Keep final facts and actual evidence-backed route details; exclude command transcripts, chat history, temporary failures, full logs, and discarded designs.
6. Update `$network-state` with confirmed reusable network facts. Do not turn pre-existing network discovery into a process card.
7. Update a project status index only with the final state and links to cards that actually exist.
8. Scan only the created cards for credentials and unnecessary private details.

## Output paths

Follow project conventions. When none exist, use only the applicable path:

```text
docs/<action-or-service>-status-card.md
docs/<action-or-service>-process-card.md
```

## Security

Never write passwords, passphrases, tokens, API keys, private-key contents, VPN private or preshared keys, cookies, sessions, recovery codes, one-time codes, subscription URLs, UUIDs, or credential-bearing URLs. Use configuration paths, variable names, keychain aliases, or password-manager references.

Use `rg` for a quick heuristic scan, then inspect matches:

```bash
rg -n "token=|password|passwd|passphrase|api[_ -]?key|private[_ -]?key|preshared[_ -]?key|pre-shared[_ -]?key|secret|cookie|session|BEGIN .*PRIVATE KEY|[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}" <created-card-paths>
```

Report which cards were created, any omitted card and its evidence reason, network-card updates, project-index changes, and the sensitive-information check.
