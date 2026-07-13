# GitHub private synchronization

Use this only for cross-device synchronization. The active private skill in `.codex/skills` is the only working source. GitHub is the current transport between devices.

## Fast gate

1. Read the remote alias and branch from `profile.md`.
2. Confirm the working directory is the active private skill and the worktree is clean.
3. Compare the remote branch commit with local `HEAD`.
4. If equal, continue immediately. If different, fetch and integrate by fast-forward only.
5. Run `validate_profile.py`.

```bash
git status --short
git ls-remote --exit-code <remote> refs/heads/<branch>
git rev-parse HEAD
git fetch <remote> <branch>
git merge --ff-only <remote>/<branch>
python3 <network-state-skill-directory>/scripts/validate_profile.py --path <private-skill-directory>
```

Stop on an unclean worktree, uncertain remote, failed validation, or diverged history.

## Publish an update

After the gate:

```bash
git add -- .gitignore SKILL.md profile.md references/devices.md references/services.md references/access-paths.md references/topology.md references/troubleshooting.md references/glossary.md
git diff --cached --check
git diff --cached --name-only
git diff --cached
git commit -m "<concise summary>"
git fetch <remote> <branch>
git merge-base --is-ancestor <remote>/<branch> HEAD
git push <remote> HEAD:<branch>
```

Ordinary confirmed updates may commit and push autonomously. Repository creation, remote replacement, history rewriting, conflict resolution, and deletion still require separate authorization.

## Local-only updates

A local-only update does not run the gate, fetch, or push. Validate it and create a normal local commit in the active cache. Before a later push, run this complete gate again; stop if another device created a divergent history.

Never embed credentials in the remote URL, force-push, automatically resolve conflicts, or store credentials in the private skill.
