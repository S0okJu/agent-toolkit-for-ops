---
name: infra-proposal
description: Write a structured infrastructure change proposal (new tool or service, change or migration, automation, decommission) for team review, from an infra operator's perspective. Covers As-Is/To-Be, alternatives, operational impact (availability, capacity, security, cost, observability, on-call, backup/DR), rollout and rollback. Facts must cite trustworthy evidence; estimates must show their basis. Use when the user asks to propose, plan, or write up an infra change, migration, or new feature.
---

# Infra Proposal

Produce one Markdown document per proposal, following `references/template.md`.
See `references/example.md` for a finished document.

A proposal exists to get a **decision**. Reviewers mostly ask: what breaks if it
fails, can we roll back, who gets paged, and what does it cost. Answer those
before they are asked.

## Evidence rule

Split every statement into one of two kinds:

- **Fact** — current state, size of the problem, existing system behavior
  (Background, As-Is, Environment). Must cite `[E#]` from the **Evidence**
  section. Trusted evidence only: executed commands with raw output, official
  logs, monitoring metrics (query + time range), config/IaC files or commits,
  official vendor docs and release notes, incident/troubleshooting records,
  tickets.
- **Estimate** — expected effect, cost, capacity, effort. Cannot be proven in
  advance, so label it `(estimate)` and show the calculation and its inputs,
  citing evidence for the inputs: `~3 h/week saved (estimate: 6 runs × 30 min [E3])`.

Not evidence: memory, guesses, blog/forum posts, AI-generated explanations.
These may be noted as where an idea came from, never as support.

Copy evidence verbatim (trim with `...`, redact secrets as `<REDACTED>`).
A fact without evidence is written with `> ⚠️ Unverified: <what is missing>`.
If you have shell/tool access, gather As-Is evidence with **read-only**
commands; never change system state without asking.

## Change type

Set `change_type` in frontmatter and expand these sections most:

| Type | Expand |
|---|---|
| `new` (new tool/service) | Alternatives, Operational Impact → operational burden, cost |
| `change` (upgrade/migration) | Rollout, Rollback, point of no return, Decommission |
| `automation` | Operational Impact → security (permission scope), blast radius when the automation misbehaves, manual override |
| `decommission` | Dependencies, Rollout, data retention |

## Workflow

1. **Collect evidence** for the problem and the As-Is state; number it `E1`, `E2`, ...
   Link past troubleshooting documents as evidence of recurring problems.
2. **Ask for gaps once** before writing: missing As-Is facts, SLO targets,
   cost inputs, approvers. Proceed with `Unverified` markers if unavailable.
3. **Write** from `references/template.md`. Keep headings exactly as in the
   template; write the body in the language of the conversation. In
   Operational Impact, keep every row; write `N/A — <reason>` rather than
   deleting one. Always include "do nothing" in Alternatives.
4. **Save** to `docs/proposals/YYYY-MM-DD-<slug>.md` in the current project
   (date = first draft) unless the user names another path.
5. **Self-check:**
   - Every fact cites `[E#]` or has an `Unverified` marker; every estimate shows its basis
   - Every cited `[E#]` exists in Evidence, and every Evidence item is cited
   - Rollback has a trigger, steps, duration, and the point of no return (or "none")
   - Success Criteria are measurable (metric/query + target + observation window)
   - Non-goals are stated
   - No secrets left unredacted
6. **Publish to Bear when complete.** When `status` is `accepted` or
   `rejected` (the decision is made) and the self-check passes, run
   `scripts/save_to_bear.sh <saved-path>`. It creates the note under
   `#ai-inbox`, or updates the existing `#ai-inbox` note with the same title.
   Skip this for `draft` / `in-review`. If the script fails (e.g. Bear not
   installed), keep the local file and tell the user.

Report the saved path, whether it was saved to Bear, any `Unverified` items,
and the Open Questions that block a decision.
