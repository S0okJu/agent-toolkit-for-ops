---
title: <one-line problem description>
date: <YYYY-MM-DD>            # when the problem occurred
author: <name>
severity: <low | medium | high | critical>
status: <resolved | mitigated | unresolved>
systems: [<system>, <system>]
tags: [<tag>, <tag>]
---

# <title>

## Summary

- **Symptom:** <one line> [E#]
- **Cause:** <one line> (<Confirmed | Suspected>) [E#]
- **Fix:** <one line> [E#]

## Symptoms

<What was observed, when it started, and the impact scope.>

Error (verbatim) [E#]:

```
<exact error message>
```

## Environment

| Item | Value | Evidence |
|---|---|---|
| OS / platform | | [E#] |
| <component> version | | [E#] |
| Relevant config | | [E#] |

## Root Cause

**Confidence:** <Confirmed | Suspected>

- **Direct cause:** <what immediately failed> [E#]
- **Underlying cause:** <why it was able to happen> [E#]

<If Suspected: what evidence would confirm it.>

## Resolution

1. <step> [E#]

   ```sh
   <exact command>
   ```

<Config changes as a diff:>

```diff
- old
+ new
```

## Verification

<How we know it is fixed: command output, metric back to normal, error gone from logs.> [E#]

## Timeline

<!-- optional -->

| Time (TZ) | Event | Evidence |
|---|---|---|
| | | [E#] |

## Investigation

<!-- optional -->

| # | Hypothesis | How checked | Result | Evidence |
|---|---|---|---|---|
| 1 | | | Ruled out / Confirmed | [E#] |

## Follow-up

<!-- optional -->

- [ ] <action> — owner: <name>, due: <YYYY-MM-DD>

## Evidence

### E1 — <type: command | log | metric | config | official-doc>

- **Source:** <command + host/context, log path or query, dashboard URL, file path/commit, doc URL>
- **Collected:** <YYYY-MM-DD HH:MM TZ>

```
<raw output / log lines / excerpt>
```

## References

<!-- optional -->

- <related issue, PR, dashboard, official doc>
