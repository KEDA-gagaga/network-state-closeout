---
name: initialize-network-state
description: Guide the first-time creation, adoption, migration, or repair of a private network-state profile, including selecting its single source directory and optionally connecting it to a confirmed GitHub private repository for multi-device synchronization. Use when a user asks to initialize network state, configure the profile for the first time, enable private GitHub synchronization, or connect another device to an existing private state repository. Do not use for routine network-state queries, record updates, troubleshooting, or action closeout.
---

# Initialize Network State

Create or adopt one private profile, validate it, and hand routine work to `$network-state`. Do not discover the user's network during onboarding.

## Preserve user control

- Treat the chosen profile directory as the only local source of truth for saved network facts.
- Keep the profile outside the installed plugin and skill directories.
- Do not scan the network, probe hosts, import configuration exports, or infer devices.
- Do not create or replace a GitHub repository, change a remote identity, overwrite a directory, or modify system configuration unless the user explicitly authorizes that action. After the user selects a synchronization onboarding path, complete its validated clone, initial commit, and ordinary push without requesting confirmation for every step.
- Never request, display, or store a password, token, private key, recovery code, or credential-bearing URL. Prefer SSH authentication already configured on the device.
- Before a command, identify the execution device, read/write effect, expected success signal, and first failure signal.

## Choose one onboarding path

Inspect the intended profile path without changing it, then choose exactly one path:

1. **New local profile**: the target does not exist or is empty; initialize it from the bundled templates.
2. **Adopt existing local profile**: the target already contains state files; validate it and never overwrite it with templates.
3. **First device with private synchronization**: create or adopt the local profile, then connect it to an empty confirmed GitHub private repository.
4. **Additional device**: clone the confirmed private repository into an absent or empty target; do not initialize templates first.

Ask only for information that cannot be discovered safely: the profile path, a short profile name and scope, whether private GitHub synchronization should be enabled, and whether this is the first or an additional device.

## Establish the profile

Resolve the target in this order:

1. A path explicitly chosen by the user.
2. `NETWORK_STATE_HOME` when set.
3. `~/.codex/network-state`.

When the user selects a non-default path, confirm that future tasks will receive the same explicit path or that `NETWORK_STATE_HOME` is persistently configured for Codex. Do not edit shell startup files or Codex configuration without explicit authorization.

For a new local profile, locate the sibling `network-state` skill and run:

```bash
python3 <network-state-skill-directory>/scripts/init_profile.py --path <state-directory>
```

For an existing profile, do not run the initializer. Confirm that all required Markdown files are present and run its validator.

When adopting an existing profile that lacks `State update policy`, add `autonomous-confirmed-facts` as a schema normalization without asking the user to choose an update mode.

Update only `profile.md` during basic onboarding:

- replace the profile name and scope placeholders with user-confirmed values;
- keep `Data classification: private`;
- keep `State update policy: autonomous-confirmed-facts` so routine work can maintain confirmed durable facts without a separate update request;
- keep synchronization disabled until the private repository setup succeeds;
- keep network facts `unknown` until separately confirmed;
- do not add a device merely because Codex is running on it.

## Offer the GitHub private synchronization module

GitHub synchronization is optional during local initialization. When the user chooses it, read `references/github-private-sync.md` completely and follow the matching first-device or additional-device path.

Do not load or execute that module when the user chooses a local-only profile. Do not offer another repository visibility model for private network state.

After private synchronization is enabled:

- record only the remote alias and default branch in `profile.md`; keep the remote URL in Git configuration;
- keep the state update policy as `autonomous-confirmed-facts`;
- set the synchronization policy to `required-before-query-and-update`;
- treat synchronization as a hard prerequisite for `$network-state` queries and changes;
- stop on an unclean worktree, uncertain remote identity, failed privacy confirmation, diverged history, validation error, or rejected push.

## Validate and hand off

Run:

```bash
python3 <network-state-skill-directory>/scripts/validate_profile.py --path <state-directory>
```

On POSIX systems, confirm the profile directory is `0700` and its top-level files are `0600`. Treat a validator error as failed initialization.

Report only:

- the selected private profile path;
- whether it was created, adopted, or cloned;
- whether private synchronization is disabled or enabled;
- when enabled, the remote alias and branch without the remote URL;
- the validation result;
- that future saved-network work should use `$network-state`.
- that routine confirmed facts will be maintained autonomously unless the user opts out for a task.

Do not include network inventory, exact endpoints, credentials, or repository URLs in the completion summary.
