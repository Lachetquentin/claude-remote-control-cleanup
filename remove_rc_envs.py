"""List and delete stale Claude Code Remote Control environments.

Undocumented API (GET/DELETE /v1/environments). The OAuth token is read
from ~/.claude/.credentials.json, sent only to api.anthropic.com,
and never printed.

Stop any running `claude remote-control` before running this script.
"""
import json
import os
import sys
import urllib.error
import urllib.request

BASE = "https://api.anthropic.com/v1/environments"


def load_token():
    path = os.path.expanduser("~/.claude/.credentials.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)["claudeAiOauth"]["accessToken"]
    except (OSError, KeyError, json.JSONDecodeError) as e:
        sys.exit(f"Cannot read the token from {path}: {type(e).__name__}")


def request(url, headers, method="GET"):
    req = urllib.request.Request(url, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode()
            return resp.status, body
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")


def main():
    headers = {
        "Authorization": f"Bearer {load_token()}",
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "environments-2025-11-01",
    }

    status, body = request(BASE, headers)
    if status != 200:
        sys.exit(f"Listing failed (HTTP {status}): {body[:300]}")
    envs = json.loads(body).get("data", [])
    if not envs:
        print("No environments found.")
        return

    print("\nEnvironments:")
    for i, e in enumerate(envs, 1):
        print(f"  [{i}] {e.get('id')}  {e.get('name', '')}  {e.get('status', '')}")

    by_id = {e.get("id"): e for e in envs}
    while True:
        raw = input("\nNumbers or IDs to delete, separated by spaces or commas (Enter to quit): ")
        choices = raw.replace(",", " ").split()
        if not choices:
            return

        selected, unknown = [], []
        for choice in choices:
            if choice.isdigit() and 1 <= int(choice) <= len(envs):
                env = envs[int(choice) - 1]
            elif choice in by_id:
                env = by_id[choice]
            else:
                unknown.append(choice)
                continue
            if env not in selected:
                selected.append(env)
        if unknown:
            print(f"Not in the list: {', '.join(unknown)}. Nothing was deleted.")
            continue

        print("\nTo delete:")
        for env in selected:
            print(f"  {env.get('id')}  {env.get('name', '')}")
        if input("Permanently delete these environments? Type 'yes': ").strip().lower() != "yes":
            print("Cancelled.")
            continue

        for env in selected:
            label = f"{env.get('id')} ({env.get('name', '')})"
            status, body = request(f"{BASE}/bridge/{env.get('id')}", headers, "DELETE")
            if 200 <= status < 300:
                print(f"Deleted: {label}")
            else:
                print(f"Failed for {label} (HTTP {status}): {body[:300]}")


if __name__ == "__main__":
    main()
