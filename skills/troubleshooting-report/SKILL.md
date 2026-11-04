---
name: troubleshooting-report
description: Write a structured troubleshooting document for a resolved (or in-progress) technical problem, backed only by trustworthy evidence such as official logs, executed commands with their output, monitoring data, config diffs, and official vendor docs. Use when the user asks to document, write up, or record a troubleshooting case, an error fix, or how an issue was diagnosed and solved.
---

# Troubleshooting Report

Produce one Markdown document per problem, following `references/template.md`.
See `references/example.md` for a finished document.

## Evidence rule (most important)

Every factual claim in **Symptoms**, **Root Cause**, **Resolution**, and
**Verification** must cite an evidence item (`[E1]`, `[E2]`, ...) listed in the
**Evidence** section. A claim without trusted evidence is not written as fact.

### Trusted evidence

| Type | Examples | Must record |
|---|---|---|
| `command` | `kubectl describe pod`, `df -h`, `curl -v`, `systemctl status` | Exact command, where it ran (host/context), time, raw output |
| `log` | journald, `/var/log/*`, container logs, cloud audit logs, app logs from the log platform | Source (file path, query, or log stream), time range, raw lines |
| `metric` | Prometheus/Grafana/Datadog/CloudWatch | Query or dashboard link, time range, observed value |
| `config` | Config files, manifests, git diffs/commits | File path or commit SHA, relevant excerpt |
| `official-doc` | Vendor docs, release notes, changelogs, the project's official issue tracker | URL, version it applies to |

### Not evidence

- Memory, guesses, or "it usually works like this" (including your own reasoning)
- Blog posts, forum/Stack Overflow answers, AI-generated explanations
- Paraphrased or summarized output in place of the original

Unofficial sources may appear only in **Investigation** as where a hypothesis
came from, never as support for a conclusion.

### Handling evidence

- Copy output **verbatim** in code blocks. Only two edits are allowed:
  trimming irrelevant lines (mark with `...`) and redaction (`<REDACTED>`).
- Redact secrets, tokens, passwords, personal data, and customer identifiers.
  Keep hostnames/IPs only if the user's context allows it.
- If the user describes a result without showing it ("the pod kept restarting"),
  ask for the command output or log. If it is not available, write the claim
  with `> ⚠️ Unverified: <what is missing>` instead of citing evidence.
- Root cause confidence:
  - **Confirmed** — evidence directly shows the cause (log line, diff, reproduction).
  - **Suspected** — evidence is indirect or consistent with the cause but does
    not prove it. State what would confirm it.

## Workflow

1. **Collect evidence first.** Gather it from the conversation, files the user
   points to, and (if you have shell/tool access) by running **read-only**
   commands yourself. Never run commands that change system state to gather
   evidence; ask first.
2. **Number evidence** as `E1`, `E2`, ... in the order collected, with type,
   source, and timestamp.
3. **Ask for gaps.** Before writing, list required information that has no
   evidence (error text, versions, verification output) and ask the user once.
   If they cannot provide it, proceed and mark those spots as unverified.
4. **Pick sections.** Required sections always appear. Add optional sections
   when they apply:
   - Timeline — outage/incident, or time order matters
   - Investigation — cause was not obvious, or hypotheses were ruled out
     (record failed hypotheses; they save the next reader the most time)
   - Follow-up — anything left to prevent recurrence
   - References — related issues, PRs, dashboards
5. **Write the document** from `references/template.md`. Keep headings exactly
   as in the template so documents stay searchable; write the body in the
   language of the conversation.
6. **Save** to `docs/troubleshooting/YYYY-MM-DD-<slug>.md` in the current
   project (date = when the problem occurred) unless the user names another path.
7. **Self-check** before finishing:
   - Every claim in Symptoms/Root Cause/Resolution/Verification has an `[E#]`
     or an `Unverified` marker
   - Every `[E#]` cited exists in Evidence, and every Evidence item is cited
   - Error messages are verbatim
   - Resolution commands can be copy-pasted as-is
   - No secrets left unredacted
   - Frontmatter `status` matches reality (no Verification evidence → not `resolved`)
8. **Publish to Bear when complete.** If `status: resolved` and the self-check
   passes, run `scripts/save_to_bear.sh <saved-path>`. It creates the note under
   `#ai-inbox`, or updates the existing `#ai-inbox` note with the same title.
   Skip this for `mitigated` / `unresolved`; run it when a later update moves
   the document to `resolved`. If the script fails (e.g. Bear not installed),
   keep the local file and tell the user.

Report the saved path, whether it was saved to Bear, and any remaining
`Unverified` items to the user.
