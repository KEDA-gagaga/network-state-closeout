# GitHub private synchronization onboarding

GitHub private repositories are currently the supported cross-device route. The repository contains the complete private network-state skill, and every device clones it directly into its own active `.codex/skills` cache.

## Preconditions

- Confirm the repository identity and `PRIVATE` visibility.
- Prefer SSH authentication or a system credential helper; never put credentials in the remote URL.
- Keep only `SKILL.md`, `profile.md`, approved reference cards, and `.gitignore` in the repository.
- Create a repository only after explicit user authorization.

When available, check visibility with:

```bash
gh repo view <owner>/<repository> --json visibility,nameWithOwner
```

## First device

Initialize or adopt the active private skill first. Update `profile.md`:

```text
- Private GitHub synchronization: enabled
- Git remote name: <remote>
- Default branch: <branch>
```

Validate, then from the private skill directory:

```bash
git init -b <branch>
git remote add <remote> <private-repository-ssh-url>
git add -- .gitignore SKILL.md profile.md references/devices.md references/services.md references/access-paths.md references/topology.md references/troubleshooting.md references/glossary.md
git diff --cached --check
git diff --cached
git commit -m "Initialize private network-state skill"
git push -u <remote> HEAD:<branch>
```

The remote repository must be empty. Stop rather than overwrite existing content.

## Additional device

Install the public plugin first so its maintenance and validation workflow is available. Then clone the user's private skill repository directly into the active cache:

```bash
git clone <private-repository-ssh-url> ~/.codex/skills/private-network-state
chmod 700 ~/.codex/skills/private-network-state
find ~/.codex/skills/private-network-state -type f -exec chmod 600 {} +
python3 <network-state-skill-directory>/scripts/validate_profile.py \
  --path ~/.codex/skills/private-network-state
```

Codex on that device now loads the cloned global private skill. Do not keep another editable clone in Documents or a project directory.

## Acceptance

- Repository visibility is confirmed private.
- The active path is under `.codex/skills` and contains `SKILL.md`.
- The remote URL contains no credential.
- Validation passes.
- The initial normal push or additional-device clone succeeds.

After setup, ordinary confirmed updates may commit and push autonomously. A local-only update may skip network access, but a later push must repeat the complete synchronization gate. Stop on uncertain identity, validation failure, rejected push, or diverged history; never force-push or auto-resolve conflicts.
