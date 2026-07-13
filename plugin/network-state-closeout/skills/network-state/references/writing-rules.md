# Writing rules

Edit only the active private skill under `.codex/skills`. It is the local source of truth loaded by Codex. Project folders and alternate clones are not working copies.

## Card routing

| Card type | File |
|---|---|
| Device, address, route, availability | `references/devices.md` |
| Service, port, domain, TLS, container, upstream | `references/services.md` |
| Directional SSH, proxy, VPN, relay, application path | `references/access-paths.md` |
| Stable relationship and boundary | `references/topology.md` |
| Confirmed reusable troubleshooting | `references/troubleshooting.md` |
| User-specific term | `references/glossary.md` |

Use one clear heading per stable object or relationship. Use `<device-id> / <service-id>` for a service and `<source-id> -> <target-id> / <protocol>` for a path.

## Lightweight update

1. Read only the relevant card file.
2. Write a simple confirmed fact directly into its card.
3. Replace superseded values and keep `unknown` when evidence is missing.
4. Do not delete a fact merely because another note omits it.
5. Discovery or import of pre-existing structure updates network cards directly and does not create a process card.
6. Use `$action-closeout-cards` only for completed work with lasting closeout value. Judge status and process cards independently; create a process card only from reliable records of the actual route.
7. Run `scripts/validate_profile.py` after writing.

Do not store chat history, command transcripts, temporary failures, full logs, configuration dumps, discarded designs, or general networking tutorials.

## Save route

- Cross-device: complete `private-sync.md` before use or write, then validate and push.
- Local only: update the active cache, validate, and make a local commit without network access. Re-run the full gate before a later push.

## Security

Never store credentials, authentication material, subscription URLs, login artifacts, or credential-bearing URLs. Keep only aliases, paths, or password-manager references.
