# Design: Add Commit Activity to Profile README

**Date**: 2025-01-06
**Author**: Claude Code
**Status**: On Hold (Bug Found)

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

---

## Testing Results (2025-01-06)

### Attempted Implementation

Tested `Readme-Workflows/recent-activity` with versions:
- `@v2.4.1` - Failed due to missing full version tag
- `@main` - Ran successfully but with display bug

### Bug Discovered

**Issue**: PushEvent displays "undefined commit(s)" instead of actual commit count

**Issue Link**: [#351](https://github.com/Readme-Workflows/recent-activity/issues/351)

**Evidence**:
```
⬤  debug     63 events found for lengmodkx.
[
  '⬆️ Pushed undefined commit(s) to [lengmodkx/lengmodkx](https://github.com/lengmodkx/lengmodkx)',
  '⬆️ Pushed undefined commit(s) to [lengmodkx/claude-skills](https://github.com/lengmodkx/claude-skills)',
  ...
]
```

The action successfully:
- ✅ Finds PushEvent entries
- ✅ Displays commit records from all repositories
- ✅ Shows repository links

But fails to:
- ❌ Extract/display actual commit count (shows "undefined" instead)

### Configuration Issues

1. `MAX_LINES` parameter is deprecated in v2.4.1+
2. Action requires `CONFIG_FILE` with specific format
3. Default config file path caused errors when file didn't exist

### Resolution

**Reverted to original action** (`jamesgeorge007/github-activity-readme@master`) due to:
- Display bug making commit records look unprofessional
- Unstable configuration requirements
- Need for reliable daily automation

### Next Steps

1. ✅ Issue submitted: [#351](https://github.com/Readme-Workflows/recent-activity/issues/351)
2. Monitor for bug fix in future releases
3. Consider alternative solutions if needed in future

### Commits

- `8426cee` - feat: add commit activity to profile README
- `b2b1306` - fix: use correct action version v2.4.1
- `567239b` - fix: add config file for recent-activity action
- `d637d44` - fix: use main branch for latest code with commit count fix
- `bc00768` - fix: update config text keys for recent-activity
- `767bd24` - revert: switch back to original github-activity-readme action
