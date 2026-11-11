# claude-remote-control-cleanup

Remove stale **Claude Code Remote Control** environments that keep showing up in the environment picker (Claude desktop app, claude.ai/code) after `claude remote-control` was stopped.

Stopping `claude remote-control` with Ctrl+C prints `Environment preserved`, and there is currently no UI or CLI command to delete an environment. This script uses the undocumented workaround described by **phishsticks** in [anthropics/claude-code#50884](https://github.com/anthropics/claude-code/issues/50884#issuecomment-5317085603), wrapped in a cross-platform script with a confirmation step.

> ⚠️ Unofficial. It relies on an undocumented API (`GET /v1/environments`, `DELETE /v1/environments/bridge/<id>`) that may change or stop working at any time. Deletions are permanent.

## What it does

1. Reads your Claude OAuth token from `~/.claude/.credentials.json`. The token is only sent to `api.anthropic.com` and is never printed.
2. Lists your environments with a number, ID, name and status.
3. Lets you pick one or several (numbers or IDs, separated by spaces or commas). Anything not in the list is rejected.
4. Shows what will be deleted and asks you to type `yes` before deleting.

## Usage

Requires Python 3 (standard library only) and a Claude Code login on this machine.

1. Stop any running `claude remote-control`.
2. Run:

   ```bash
   python remove_rc_envs.py
   ```

   (`python3` on macOS/Linux.)
3. Delete only the stale Remote Control entries (named like `HOST:C:\path\to\folder:xxxx`). **Do not delete `Default`**, which is your cloud environment.

Example:

```
Environments:
  [1] env_014M...  My-PC:C:\Users\me\Desktop\project:5a71
  [2] env_01GY...  Default

Numbers or IDs to delete, separated by spaces or commas (Enter to quit): 1

To delete:
  env_014M...  My-PC:C:\Users\me\Desktop\project:5a71
Permanently delete these environments? Type 'yes': yes
Deleted: env_014M... (My-PC:C:\Users\me\Desktop\project:5a71)
```

If an entry still appears in the picker afterwards, restart the app or run the script again.

## License

MIT
