# Checkout branch

When Step 2 **foresaw** multiple file accesses, reach source through a local tree — not repeated `gh api` calls.

## Steps

### 1. Ask

"Is `owner/repo` checked out locally? Absolute path, or no."

**Completion criterion:** user answered with a path or declined.

### 2. Verify path

If a path was given:

```bash
git -C <path> remote get-url origin
```

The URL must contain `owner/repo`. On mismatch, report and re-ask.

Use Read/Grep/Glob with absolute paths under that directory.

**Completion criterion:** remote matches `owner/repo`; exploration uses the verified path.

### 3. No local copy

Ask permission to shallow clone before running any clone command.

**Completion criterion:** user approved or declined clone.

### 4. Clone

Only after approval:

```bash
gh repo clone owner/repo "$TMPDIR/cursor-${repo}-$(date +%s)" -- --depth=1
```

Use `$TMPDIR` (or `/tmp` on Linux). Explore with Read/Grep/Glob on absolute paths under the clone directory.

**Completion criterion:** shallow clone exists at a known absolute path; Read/Grep/Glob target that tree.
