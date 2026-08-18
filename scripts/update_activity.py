#!/usr/bin/env python3
"""Update the Recent Activity section in README.md.

Fetches the user's public events from the GitHub Events API and writes the
latest N entries between the RECENT_ACTIVITY markers in README.md.
"""

import json
import os
import sys
import urllib.request

MAX_LINES = 10
README = "README.md"
START = "<!--RECENT_ACTIVITY:start-->"
END = "<!--RECENT_ACTIVITY:end-->"


def repo_link(name):
    return f"[{name}](https://github.com/{name})"


def fmt(event):
    t = event["type"]
    p = event.get("payload", {})
    repo = event["repo"]["name"]
    r = repo_link(repo)

    if t == "PushEvent":
        return None
    if t == "PullRequestEvent":
        n = p.get("number")
        url = f"https://github.com/{repo}/pull/{n}"
        action = p.get("action")
        if action == "opened":
            return f"💪 Opened PR [#{n}]({url}) in {r}"
        if action == "closed" and (p.get("pull_request") or {}).get("merged"):
            return f"🎉 Merged PR [#{n}]({url}) in {r}"
        if action == "closed":
            return f"❌ Closed PR [#{n}]({url}) in {r}"
        return None
    if t == "IssuesEvent":
        issue = p.get("issue") or {}
        n, url = issue.get("number"), issue.get("html_url")
        if p.get("action") == "opened":
            return f"❗ Opened issue [#{n}]({url}) in {r}"
        if p.get("action") == "closed":
            return f"✔️ Closed issue [#{n}]({url}) in {r}"
        return None
    if t == "IssueCommentEvent":
        issue = p.get("issue") or {}
        url = (p.get("comment") or {}).get("html_url")
        return f"💬 Commented on [#{issue.get('number')}]({url}) in {r}"
    if t == "CreateEvent":
        if p.get("ref_type") == "repository":
            return f"📔 Created new repository {r}"
        return None
    if t == "ForkEvent":
        return None
    if t == "ReleaseEvent":
        rel = p.get("release") or {}
        name = rel.get("name") or rel.get("tag_name")
        return f"🚀 Published release [{name}]({rel.get('html_url')}) in {r}"
    return None


def main():
    username = os.environ.get("GH_USERNAME") or os.environ["GITHUB_REPOSITORY_OWNER"]
    token = os.environ.get("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "recent-activity-updater",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # Paginate up to 3 pages (300 events) so that filtering out
    # star / push / fork still leaves enough entries to fill MAX_LINES.
    # The Events API caps a single user at the most recent 300 events.
    events = []
    for page in range(1, 4):
        url = (
            f"https://api.github.com/users/{username}/events/public"
            f"?per_page=100&page={page}"
        )
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            page_events = json.load(resp)
        if not page_events:
            break
        events.extend(page_events)
        if len(events) >= MAX_LINES * 3:
            break

    lines = []
    for event in events:
        line = fmt(event)
        if line:
            lines.append(line)
        if len(lines) >= MAX_LINES:
            break

    if not lines:
        print("No activity found, leaving README unchanged.")
        return

    with open(README, encoding="utf-8") as f:
        content = f.read()

    block = START + "\n" + "\n".join(
        f"{i}. {line}<br>" for i, line in enumerate(lines, 1)
    ) + f"\n{END}"

    if START not in content or END not in content:
        sys.exit("Activity markers not found in README.md")

    new_content = content[: content.index(START)] + block + content[content.index(END) + len(END):]
    if new_content != content:
        with open(README, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)
        print(f"README updated with {len(lines)} activity entries.")
    else:
        print("No changes.")


if __name__ == "__main__":
    main()
