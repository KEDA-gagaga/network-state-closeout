---
name: initialize-network-state
description: Initialize or adopt a private global network-state skill in the active Codex skills cache, or connect another device by cloning the same GitHub private repository into its .codex/skills directory. Use for first setup, private GitHub onboarding, or another-device installation; not routine updates.
---

# Initialize Network State

Create or adopt one private global skill. Do not discover or scan the user's network during onboarding.

## Core model

- The active directory under `.codex/skills` is the only editable local source.
- Cross-project use comes from Codex loading that global skill in different projects.
- Cross-device use comes from installing this plugin, then cloning the same GitHub private repository into the other device's `.codex/skills` cache.
- Project copies, Documents folders, and alternate clones are never daily working copies.
- GitHub private repositories are currently the only cross-device synchronization route described by this plugin.

## Choose one path

1. New private skill: initialize an absent or empty target.
2. Existing private skill: validate it without applying templates.
3. First synchronized device: create or adopt the skill, then connect an empty confirmed GitHub private repository.
4. Additional device: install the plugin and clone the confirmed private repository directly into the active target; do not initialize first.

Ask only for the target path, a short profile name and scope, whether GitHub private synchronization is wanted, and whether this is the first or another device.

## Active path

Resolve the target from an explicit path, `NETWORK_STATE_HOME`, or:

```text
~/.codex/skills/private-network-state
```

For a new skill, run:

```bash
python3 <network-state-skill-directory>/scripts/init_profile.py --path <private-skill-directory>
```

Update `profile.md` with the confirmed profile name and scope. Do not add device cards until facts are separately confirmed.

## GitHub private synchronization

When selected, read `references/github-private-sync.md` and follow its first-device or additional-device path. Repository creation, remote replacement, and destructive Git actions require explicit authorization. Routine validated commits and pushes do not require confirmation each time.

A local-only update remains available after synchronization is configured: update and locally commit the active cache without fetching or pushing. A later cross-device synchronization must run the complete gate again.

## Validate

```bash
python3 <network-state-skill-directory>/scripts/validate_profile.py --path <private-skill-directory>
```

On POSIX systems, prefer directory mode `0700` and file mode `0600`. Report the active path, created/adopted/cloned result, GitHub synchronization status, and validation result without revealing endpoints or repository URLs.
