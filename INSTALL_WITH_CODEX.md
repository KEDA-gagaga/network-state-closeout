# Hand This Repository to Codex

**English** | [简体中文](INSTALL_WITH_CODEX.zh-CN.md)

This document is for an agent that receives the repository link. Its goal is to install the public plugin bundle into the current Codex environment and then guide the user through creating a global private network state.

Repository:

```text
https://github.com/KEDA-gagaga/network-state-closeout
```

## Why this deployment model exists

Network state contains two kinds of material with very different lifecycles:

- **Stable capabilities**: Categorization, on-demand loading, lightweight writing, privacy validation, synchronization gates, and closeout-card rules. These belong in a public plugin that can be installed and upgraded.
- **Dynamic private knowledge**: Real devices, addresses, ports, domains, SSH paths, Docker networks, reverse proxies, virtual networks, VPS infrastructure, and troubleshooting conclusions. These belong only in the user's global private skill.

Separating them lets users share and upgrade the plugin without placing real network information in a public repository. The public plugin defines how to read and maintain state; `~/.codex/skills/private-network-state` stores what the user's network currently looks like.

Status cards and process cards are not a required pair. Pre-existing structure and simple facts go directly into network cards. A process card is created only when reliable records of the actual process exist and the route will retain diagnostic, audit, or troubleshooting value. An agent must never reconstruct an unrecorded process from current configuration.

The repository provides a repository marketplace, so a user can hand Codex one link and the agent can identify and install the complete plugin without guessing which subdirectory to copy. After installation, private knowledge is still created and maintained under `.codex/skills` on the user's device.

## Agent workflow after receiving the link

If the user sends only the link without asking to install anything, briefly explain that it is a bundled private network-state plugin and ask whether to install it. If the user clearly asks to install, deploy, or use it, continue with the following workflow.

### 1. Verify the public source

Confirm that the repository URL, `.agents/plugins/marketplace.json`, `plugin/network-state-closeout/.codex-plugin/plugin.json`, and this file exist. Never create or write the user's private network information inside this public repository.

### 2. Add the repository marketplace

Prefer the plugin commands available in the current Codex environment:

```bash
codex plugin marketplace add KEDA-gagaga/network-state-closeout
codex plugin list --marketplace network-state-closeout
```

If a marketplace with the same name already exists, verify that it points to this repository. Stop on a source mismatch; do not replace it.

### 3. Install the complete plugin bundle

```bash
codex plugin add network-state-closeout@network-state-closeout
```

Do not copy only one skill, and do not use the public plugin repository as the private network-state repository.

### 4. Start a new task

After installation, tell the user to start a new Codex task. Newly installed skills are guaranteed to be discovered only in a new task; do not pretend that the current task has already loaded them.

Recommended prompt for the new task:

```text
$initialize-network-state Help me initialize a global private network-state skill. First explain what may be collected and what must never be saved, make the privacy promise, ask for my consent, and then use local read-only checks to fill in as much of my network structure as possible.
```

### 5. Run initialization onboarding

In the new task, call `initialize-network-state`:

1. Use `~/.codex/skills/private-network-state` by default and treat it as the only editable source of truth.
2. Distinguish structural network information that may be saved from authentication secrets that must never be saved.
3. Make an explicit promise that authentication secrets will not enter files, cards, Git staging, commit history, or remote repositories.
4. Only after user consent, collect SSH, Docker, reverse-proxy, virtual-network, VPS, routing, and DNS structure from local read-only sources.
5. Active scanning, cloud APIs, elevated reads, and remote login require separate authorization for each scope. Prefer SSH when another host is authorized for inspection.
6. Run the private-skill validator and report only collected categories, remaining gaps, and validation results without repeating private endpoints in the final response.

### 6. Optional cross-device sharing

Only when the user wants agents on multiple devices to share the same network knowledge, guide the user through preparing a separate GitHub private repository.

- The private repository stores the complete `private-network-state` skill.
- This public plugin repository stores no user network information.
- Each device reads and edits its own `~/.codex/skills/private-network-state`.
- Additional devices install this plugin first, then clone the same private repository directly into that path.

## Absolute security boundary

With user consent, the private skill may save hostnames, addresses, subnets, routes, ports, domains, service roles, access relationships, Docker networks, reverse proxies, virtual networks, VPS infrastructure, and verification signals.

It must never save passwords, passphrases, tokens, API keys, private-key contents, VPN private or preshared keys, cookies, sessions, recovery codes, one-time codes, subscription URLs, cloud credentials, or credential-bearing URLs.

When authentication is required, keep only an identity-file path, keychain item name, password-manager entry name, environment-variable name, or secret-manager alias. Authentication secrets must never enter the private skill, status cards, process cards, temporary files, Git staging, commit history, or any remote repository.

## Acceptance checks

- `codex plugin list --marketplace network-state-closeout` shows the plugin.
- The plugin installs successfully and the user is told to start a new task.
- The new task can call `$initialize-network-state`.
- The private skill is under `.codex/skills`, not a project directory or Documents copy.
- The privacy explanation, promise, and user consent occur before initialization discovery.
- `validate_profile.py` passes.

## Update the plugin

Refresh the repository marketplace and reinstall:

```bash
codex plugin marketplace upgrade network-state-closeout
codex plugin add network-state-closeout@network-state-closeout
```

Start a new task after the update.

## Official references

- [Build plugins](https://learn.chatgpt.com/docs/build-plugins)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
