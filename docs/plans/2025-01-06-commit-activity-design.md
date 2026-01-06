# Design: Add Commit Activity to Profile README

**Date**: 2025-01-06
**Author**: Claude Code
**Status**: Approved

## Overview

Add commit/push activity records to the GitHub Profile README's activity section, showing recent commits across all repositories.

## Current State

- Uses `jamesgeorge007/github-activity-readme@master` action
- `FILTER_EVENTS` defaults to: `IssueCommentEvent,IssuesEvent,PullRequestEvent,ReleaseEvent`
- Does NOT include `PushEvent` (commit records)
- Only shows issues, PRs, and releases

## Proposed Solution

Replace with `Readme-Workflows/recent-activity@v2` - an actively maintained fork that natively supports 13+ event types including `PushEvent`.

### Expected Output Format

```
1. ⬆️ Pushed 3 commit(s) to lengmodkx/lemonBlog
2. 🔒 Closed issue #2 in lengmodkx/lemonBlog
3. ⬆️ Pushed 1 commit(s) to lengmodkx/another-repo
4. ❗ Opened issue #5 in lengmodkx/lemonBlog
```

## Implementation

### Modify `.github/workflows/update-readme.yml`

Replace the activity generation step:

```yaml
# Old:
- name: Generate github activity
  uses: jamesgeorge007/github-activity-readme@master
  with:
    MAX_LINES: 10

# New:
- name: Generate github activity
  uses: Readme-Workflows/recent-activity@v2
  with:
    MAX_LINES: 10
```

### Optional: Increase MAX_LINES

If commit activity is frequent, consider increasing to `15` or `20` to ensure other events (Issues, PRs) remain visible.

## Verification

1. Manually trigger workflow from GitHub Actions page
2. Confirm `⬆️ Pushed X commit(s) to repo` entries appear in activity section
3. Verify commits from all repositories are displayed
4. Check daily automatic execution (UTC 00:00)

## Notes

- New action adds "Last Updated" timestamp below activity list (expected behavior)
- Fully compatible with existing `<!--START_SECTION:activity-->` markers
- No changes needed to README.md structure
- Active project with community support and documentation

## Resources

- [Readme-Workflows/recent-activity](https://github.com/Readme-Workflows/recent-activity)
- [Setup Wiki](https://github.com/Readme-Workflows/recent-activity/wiki)
- [jamesgeorge007/github-activity-readme](https://github.com/jamesgeorge007/github-activity-readme)
