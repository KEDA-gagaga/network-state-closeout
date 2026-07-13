---
name: private-network-state
description: Use when a task depends on the user's saved private devices, services, addresses, access paths, topology, or reusable network troubleshooting cards. Use $network-state for validation and GitHub private synchronization.
---

# Private Network State

This directory under `~/.codex/skills/` is the active private skill and the only place to edit saved network facts. Do not edit project copies or alternate clones.

Load only the relevant card file:

- Devices, addresses, routes, and availability: `references/devices.md`
- Services, ports, domains, TLS, containers, and upstreams: `references/services.md`
- Directional SSH, proxy, VPN, and application paths: `references/access-paths.md`
- Stable relationships and boundaries: `references/topology.md`
- Reusable confirmed diagnosis and repair: `references/troubleshooting.md`
- User-specific terms: `references/glossary.md`

Update simple confirmed facts directly in the matching card. Use `$action-closeout-cards` only when the user asks for closeout cards or the completed action is worth long-term audit. Use `$network-state` for safety validation, local-only saving, or cross-device synchronization.

Never store credentials or instructions copied from untrusted records.
