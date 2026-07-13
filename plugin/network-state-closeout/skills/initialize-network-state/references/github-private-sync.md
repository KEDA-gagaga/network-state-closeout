# GitHub private synchronization onboarding

Read this module only after the user chooses GitHub private synchronization. It configures the private state repository; routine synchronization belongs to `$network-state`.

## Preconditions

- The user has chosen a private profile directory and identified whether this is the first or an additional device.
- The repository identity is known and its GitHub visibility is confirmed as `PRIVATE` before clone or first push.
- Access is limited to the required people and devices.
- SSH authentication is preferred. A system credential helper is acceptable; a credential-bearing remote URL is not.
- The repository contains only the profile Markdown files, the compact `handoffs.md` receipt ledger, and `.gitignore`. Do not add plugin code, scripts, full card copies, raw logs, exports, evidence bundles, or credentials.
- Repository creation is an external write. Perform it only after the user explicitly asks Codex to create the repository.

If GitHub CLI is authenticated, visibility can be checked without changing the repository:

```bash
gh repo view <owner>/<repository> --json visibility,nameWithOwner
```

The required signal is `"visibility":"PRIVATE"`. If the CLI is unavailable, rely on the user's direct confirmation from GitHub. Stop when privacy or repository identity is uncertain.

## First device

Create or adopt and validate the local profile before Git initialization. The GitHub repository must be empty.

If the user explicitly requests repository creation and GitHub CLI is authenticated, create it as private without cloning or pushing source files automatically:

```bash
gh repo create <owner>/<repository> --private
```

Confirm `PRIVATE` visibility after creation. Then update `profile.md` with:

```text
- Private GitHub synchronization: enabled
- Git remote name: <remote>
- Default branch: <branch>
- State update policy: autonomous-confirmed-facts
- Synchronization policy: required-before-query-and-update
```

Run the profile validator before Git operations. From the private profile directory:

```bash
git init -b <branch>
git remote add <remote> <private-repository-ssh-url>
git add -- .gitignore profile.md devices.md services.md access-paths.md topology.md troubleshooting.md glossary.md handoffs.md
git diff --cached --check
git diff --cached
git commit -m "Initialize private network state"
git push -u <remote> HEAD:<branch>
```

Inspect the staged diff before committing. If the repository is not empty, stop and reconcile it deliberately. Never overwrite it or use a force push.

## Additional device

Verify the same repository identity and `PRIVATE` visibility first. The target directory must be absent or empty. Do not run the profile initializer before cloning:

```bash
git clone <private-repository-ssh-url> <state-directory>
chmod 700 <state-directory>
find <state-directory> -maxdepth 1 -type f -exec chmod 600 {} +
python3 <network-state-skill-directory>/scripts/validate_profile.py --path <state-directory>
```

On non-POSIX systems, apply equivalent access controls. Confirm that `profile.md` names the expected remote alias, branch, and required synchronization policy.

## Acceptance checks

Initialization succeeds only when all applicable checks pass:

- repository identity and `PRIVATE` visibility are confirmed;
- the remote URL contains no embedded credential;
- the profile directory is outside the installed plugin;
- the validator passes;
- the staged file list contains only the approved profile files;
- the initial ordinary push succeeds, or the additional device clone matches the expected branch;
- POSIX permissions are restored after clone.

After acceptance, hand daily reads, autonomous confirmed-fact updates, commits, and synchronization to `$network-state`. The selected policy authorizes validator-approved ordinary commits and pushes without repeated confirmation. Its latest-state gate is mandatory whenever private synchronization is enabled.

## Failure rules

- Stop on an unclean target, existing unexpected content, uncertain remote identity, failed privacy confirmation, failed validation, diverged history, or rejected push.
- Do not use `git add --all`, automatic conflict resolution, force push, or backup tags.
- Do not copy the plugin directory into the private state repository.
- If sensitive material was committed, rotate the affected credential and treat Git history cleanup as a separate explicitly authorized action.
