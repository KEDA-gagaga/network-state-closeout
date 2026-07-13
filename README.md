# Network State + Closeout Cards Plugin

**English** | [简体中文](README.zh-CN.md)

> Version: `0.1.1` · Stable release

> Turn a constantly changing private network into structured knowledge that agents can use across projects, load on demand, and share across devices.

## Let your agent know what your network looks like now

Do you still explain your hosts, services, proxies, and access paths again every time you open a new task, switch projects, or move to another device?

Do you still search through notes and chat history for device addresses, reverse proxies, container ports, domains, TLS, and connection relationships?

The real problem is usually not a lack of notes. It is the absence of one trusted, maintainable source for network information that keeps changing. Putting every detail into one large skill is not ideal either: network state changes, real endpoints are private, and unrelated material consumes the agent's context.

The OpenAI Docs skill included with Codex offers a useful model. It does not freeze an evolving body of documentation inside the skill. Instead, it preserves stable rules for source selection, freshness checks, failure boundaries, and retrieval. Before answering, it refreshes from trusted sources, builds a navigable view, and reads only the relevant sections. The goal is not to store all knowledge in advance, but to preserve a reliable path to current knowledge.

`network-state-closeout` applies the same idea to private network state. The public plugin stores categorization, writing rules, fast validation, security boundaries, and synchronization gates. Devices, services, addresses, access paths, and reusable troubleshooting knowledge live in the user's own global private skill. Agents read only the category cards needed for the current task and directly maintain confirmed durable facts.

The result is not a static inventory that quickly becomes stale. It is a lightweight private network knowledge layer that works across projects and, through a GitHub private repository, lets agents on multiple devices share the same network knowledge while loading only what each task needs.

## Hand this link directly to Codex

Send the following text to Codex:

```text
Please install and use this plugin:
https://github.com/KEDA-gagaga/network-state-closeout

Read INSTALL_WITH_CODEX.md in the repository and follow its agent installation workflow. After installation, start a new task and guide me through initializing my private network state.
```

The repository includes a Codex-compatible plugin marketplace. For the design rationale, installation commands, initialization order, and security boundaries, see [INSTALL_WITH_CODEX.md](INSTALL_WITH_CODEX.md).

## How the three skills work together

The plugin contains three skills with distinct responsibilities:

- `initialize-network-state`: Initialize a global private network-state skill, optionally collect local network structure from approved read-only sources, or connect another device to an existing GitHub private repository.
- `network-state`: Load and maintain categorized cards on demand, using either local-only saving or cross-device synchronization.
- `action-closeout-cards`: Independently decide whether a status card or process card is justified, and record only durable, evidence-backed information.

Typical flow:

```text
First use
  -> initialize-network-state creates or adopts the global private skill
  -> explain the storage boundary and promise that authentication secrets never enter files or Git
  -> with user consent, collect network structure from local read-only sources
  -> optionally connect a GitHub private repository
  -> validate and hand routine maintenance to network-state

Routine query or simple update
  -> network-state reads only the relevant category cards
  -> answer the question or directly update a confirmed fact
  -> save locally or synchronize across devices after the gate passes

Important deployment, migration, or troubleshooting completion
  -> action-closeout-cards independently evaluates the status card and process card
  -> create a process card only when the real process has reliable evidence
  -> network-state writes reusable final conclusions back to the matching network cards
```

A simple change to an address, port, availability result, or verification time does not trigger closeout cards. Inventorying or importing pre-existing network structure does not create a process card either, because current configuration proves the current state, not how that state was produced.

## How private network state is organized

After initialization, the private network state is itself a global Codex skill:

```text
~/.codex/skills/private-network-state/
├── SKILL.md
├── profile.md
└── references/
    ├── devices.md
    ├── services.md
    ├── access-paths.md
    ├── topology.md
    ├── troubleshooting.md
    └── glossary.md
```

This active `.codex/skills` cache is the only location that may be edited, committed, and synchronized. Project directories, Documents folders, and alternate clones are not daily working copies.

Each category file contains small cards. Agents load them progressively according to the task:

| Question type | Read only |
|---|---|
| Devices, addresses, routes, availability | `references/devices.md` |
| Services, ports, domains, TLS, containers, upstreams | `references/services.md` |
| SSH, proxy, VPN, relay, and application access paths | `references/access-paths.md` |
| Stable topology and network boundaries | `references/topology.md` |
| Confirmed reusable troubleshooting knowledge | `references/troubleshooting.md` |
| User-specific abbreviations | `references/glossary.md` |

A service query does not need the complete device inventory and topology. Diagnosing one path does not require every service card. This keeps irrelevant material out of the agent's context.

## Cross-project and cross-device use

These concepts solve different problems:

- **Cross-project**: The private skill lives in the global Codex directory at `~/.codex/skills/`. Agents can load the same network knowledge on demand after switching projects.
- **Cross-device**: Another device first installs this plugin, then clones the same GitHub private repository directly into its own `.codex/skills/private-network-state`. Agents on different devices therefore read and maintain the same network knowledge history.

The current release uses GitHub private repositories as its cross-device synchronization route. GitHub stores the shared history; each device still reads and edits its own active `.codex/skills` cache.

## Lightweight writing and saving

After a task confirms a durable fact, the agent may autonomously update the matching card. The user does not have to approve each update and may still opt out for a particular task.

Closeout evaluation is used only for a completed deployment, migration, troubleshooting action, or configuration change that may have lasting value, or when the user explicitly requests closeout. Status cards and process cards are not a required pair:

- Create a status card only when the final state, entry point, verification result, or boundary deserves a durable reference.
- Create a process card only when the actual process has reliable records and its route, decisions, or troubleshooting entry will remain useful.
- Do not create a process card for pre-existing structure, simple facts, or a current configuration with no process record.
- If the user requests a process card but evidence is insufficient, explain that it was omitted; never guess or create a ceremonial placeholder.
- Write reusable network facts from the result directly into the matching category cards.

Deleting an existing record or changing real network configuration still requires explicit user authorization.

### Local-only saving

When network synchronization is not wanted for the current task:

- Update `.codex/skills/private-network-state` directly.
- Run the fast validator.
- If Git is enabled, create a local commit without fetching or pushing.
- State that the update has not been synchronized across devices.

Before a later synchronization, run the complete privacy and synchronization gate again instead of reusing an earlier remote check.

### Cross-device synchronization

When multiple devices need the same current state, compare the GitHub private repository's remote commit with the local commit. Continue immediately when they match; otherwise fetch and integrate by fast-forward only. Then validate, create a normal commit, and push.

Stop when repository identity is uncertain, the worktree is not clean, validation fails, the remote rejects the push, or histories diverge. Never force-push or automatically resolve divergence.

## Getting started

### First device

The recommended entry point is the initialization skill:

```text
$initialize-network-state Help me initialize a global private network-state skill. First explain what may be collected and what must never be saved, make the privacy promise, ask for my consent, and then use local read-only checks to fill in as much of my network structure as possible.
```

The initialization guide distinguishes two information classes:

- **Network structure that may be saved**: Device aliases and roles, addresses, subnets, routes, SSH relationships, Docker networks and ports, reverse proxies, domains, TLS state, virtual networks, VPS infrastructure, and service dependencies.
- **Authentication secrets that must never be saved**: Passwords, passphrases, tokens, API keys, private-key contents, VPN private or preshared keys, cookies, recovery codes, one-time codes, subscription URLs, and credential-bearing URLs.

Codex must first promise that authentication secrets will not enter the private skill, status cards, process cards, Git staging, commit history, or GitHub repository. It then asks for permission to inspect local configuration and run read-only commands. If the user declines, initialization continues with empty cards. If the user agrees, only structural facts from the authorized scope are recorded.

Local read-only discovery does not include active subnet scanning, cloud-provider API calls, or logging in to another host. Each expanded operation requires a clear scope and separate authorization. When another host is authorized for inspection, SSH is the preferred access method.

The initializer can also be run manually:

```bash
python3 plugin/network-state-closeout/skills/network-state/scripts/init_profile.py
```

Default destination:

```text
~/.codex/skills/private-network-state
```

The initializer never overwrites a non-empty directory.

### Additional device

Install this plugin first, confirm the private repository identity and visibility, then run:

```bash
git clone <private-repository-url> ~/.codex/skills/private-network-state
python3 <network-state-skill-directory>/scripts/validate_profile.py \
  --path ~/.codex/skills/private-network-state
```

After validation passes, the agent uses this directory as a global private skill. Do not create another project copy for daily editing.

## Security boundary

With user consent, private cards may store the hostnames, addresses, ports, domains, paths, topology, service relationships, and verification signals required for operation. These structural facts belong only in the global private skill and the GitHub private repository confirmed by the user.

Never save passwords, passphrases, tokens, API keys, private-key contents, VPN private or preshared keys, cookies, sessions, recovery codes, one-time codes, subscription URLs, login artifacts, or credential-bearing URLs. When a connection requires authentication, keep only an identity-file path, keychain item name, password-manager entry name, environment-variable name, or safe secret-manager reference.

The GitHub repository must be private. Confirm visibility for the first push and whenever remote identity is uncertain.

## Install the complete plugin

The recommended route is to let Codex follow [INSTALL_WITH_CODEX.md](INSTALL_WITH_CODEX.md). The command-line entry point is:

```bash
codex plugin marketplace add KEDA-gagaga/network-state-closeout
codex plugin add network-state-closeout@network-state-closeout
```

Start a new task after installation, then call `$initialize-network-state`.

```text
plugin/network-state-closeout/
├── .codex-plugin/plugin.json
└── skills/
    ├── initialize-network-state/
    ├── network-state/
    └── action-closeout-cards/
```

Install the complete `plugin/network-state-closeout` directory. Do not copy only one skill.

## Validation

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py \
  plugin/network-state-closeout

python3 /path/to/skill-creator/scripts/quick_validate.py \
  plugin/network-state-closeout/skills/network-state

python3 /path/to/skill-creator/scripts/quick_validate.py \
  plugin/network-state-closeout/skills/initialize-network-state

python3 /path/to/skill-creator/scripts/quick_validate.py \
  plugin/network-state-closeout/skills/action-closeout-cards
```

Initialization test:

```bash
python3 plugin/network-state-closeout/skills/network-state/scripts/init_profile.py \
  --path /tmp/private-network-state-test

python3 plugin/network-state-closeout/skills/network-state/scripts/validate_profile.py \
  --path /tmp/private-network-state-test
```

## License

This project is licensed under the [MIT License](LICENSE).
