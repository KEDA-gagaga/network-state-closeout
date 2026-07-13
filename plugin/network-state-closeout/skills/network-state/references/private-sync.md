# Routine GitHub private synchronization

Use this workflow only after `$initialize-network-state` has successfully enabled synchronization. The private profile directory is the only local source of truth for saved network state; the installed plugin remains separate.

## Hard gate

Before every saved-state query, verification, diagnosis, update, commit, or synchronization:

1. Read `profile.md` and obtain the configured remote alias and branch.
2. Confirm the working directory is the configured private profile and not the plugin directory.
3. Require a clean worktree.
4. Compare the remote branch commit with local `HEAD`. When they differ, fetch and integrate by fast-forward only.
5. Run the profile validator before using the records.

```bash
git status --short
git ls-remote --exit-code <remote> refs/heads/<branch>
git rev-parse HEAD
git fetch <remote> <branch>
git merge --ff-only <remote>/<branch>
python3 <network-state-skill-directory>/scripts/validate_profile.py --path <state-directory>
```

When `ls-remote` and `HEAD` already match, skip fetch and continue to validation. Otherwise fetch before comparing or merging histories.

Stop when:

- the worktree is not clean;
- the remote identity or private visibility is uncertain;
- the remote branch cannot be read;
- the local and remote histories have diverged;
- validation fails.

Do not answer from an unsynchronized local copy after a hard-gate failure.

## Push a confirmed update

Enabling synchronization with `State update policy: autonomous-confirmed-facts` authorizes routine ordinary commits and pushes of validator-approved state files. Do not request confirmation for each update. Separate authorization is still required to create or replace a repository, change the remote identity, rewrite history, or clean sensitive material from history.

1. Complete the hard gate before editing.
2. Write only confirmed durable facts.
3. Run `validate_profile.py`.
4. Stage only the known state files.
5. Inspect the staged file list and diff.
6. Commit with a concise summary.
7. Fetch again and verify that the remote branch is contained in local history.
8. Use a normal push.

Skip the commit and push when no approved state file changed.

```bash
git add -- .gitignore profile.md devices.md services.md access-paths.md topology.md troubleshooting.md glossary.md handoffs.md
git diff --cached --check
git diff --cached --name-only
git diff --cached
git commit -m "<concise state summary>"
git fetch <remote> <branch>
git merge-base --is-ancestor <remote>/<branch> HEAD
git push <remote> HEAD:<branch>
```

If the remote changes after the final check, the ordinary push must be rejected. Stop, synchronize again, and reassess the update.

## Security rules

- Store only the approved Markdown state files, the compact `handoffs.md` receipt ledger, and `.gitignore` in the private repository.
- Keep the remote URL in Git configuration, not `profile.md`.
- Use SSH authentication or a system credential helper; never embed credentials in the remote URL.
- Do not use `git add --all`, force push, automatic conflict resolution, or tags that preserve accidentally committed sensitive material.
- If sensitive material reaches GitHub, remove it from current files, rotate the affected credential, and treat history cleanup as a separate explicitly authorized task.
