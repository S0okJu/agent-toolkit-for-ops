---
title: <one-line proposal>
author: <name>
date: <YYYY-MM-DD>            # first draft
status: <draft | in-review | accepted | rejected | superseded>
change_type: <new | change | automation | decommission>
environments: [<dev>, <stg>, <prod>]
systems: [<system>, <system>]
owner_team: <team that will operate it>
reviewers: [<name>, <name>]
related: [<issue/ticket/troubleshooting doc>]
---

# <title>

## Summary

- **What:** <one line>
- **Why:** <one line> [E#]
- **Expected outcome:** <one line> (estimate)
- **Prod impact:** <downtime yes/no, which systems>

## Background and Problem

<The problem only, no solution yet. Quantify it: incidents, toil hours,
capacity limits, cost, EOL dates.> [E#]

## Goals and Non-goals

**Goals**

- <goal, with SLO numbers where relevant>

**Non-goals**

- <what this proposal deliberately does not change>

## Current State (As-Is)

<Architecture, versions, scale and utilization, known limits.>

| Item | Value | Evidence |
|---|---|---|
| | | [E#] |

## Proposed Design (To-Be)

### Architecture

<Diagram (Mermaid or image) and component list.>

### Network

<Flows, ports, subnets, DNS, load balancers, external exposure.>

### Permissions

<IAM/RBAC roles, scopes, who/what gets access. Least privilege.>

### Configuration / IaC

<Terraform, Helm, manifests: key changes as a diff or excerpt.>

## Alternatives Considered

| Option | Operational burden | Cost | Lock-in | Team skill fit | Vendor support / license | Decision |
|---|---|---|---|---|---|---|
| Do nothing | | | | | | Rejected: <reason> |
| <option A (proposed)> | | | | | | Chosen |
| <option B> | | | | | | Rejected: <reason> |

## Operational Impact

| Area | Assessment |
|---|---|
| Availability | <SPOFs, blast radius on failure, isolation> |
| Capacity / performance | <sizing basis, expected load, scaling> (estimate) |
| Security | <permission scope, exposure, secret management, audit logs> |
| Cost | <initial + monthly> (estimate: <calculation>) |
| Observability | <metrics, logs, alerts, dashboards — ready before rollout> |
| Operational burden | <owner team, on-call impact, runbook, upgrade cadence, EOL> |
| Backup / DR | <RPO, RTO, restore test plan> |

## Rollout Plan

| Phase | Scope | Pre-checks | Go / No-go criteria | Downtime |
|---|---|---|---|---|
| 1 | dev | | | |
| 2 | stg | | | |
| 3 | prod canary | | | |
| 4 | prod all | | | |

<Change window, data migration steps.>

## Rollback Plan

- **Trigger:** <conditions that mean roll back>
- **Steps:**

  ```sh
  <exact commands>
  ```

- **Expected duration:** <time>
- **Point of no return:** <step after which rollback is impossible, or "none">

## Success Criteria

| Metric | Query / source | Target | Observation window |
|---|---|---|---|
| | | | |

## Open Questions and Dependencies

| Question / dependency | Owner | Needed by |
|---|---|---|
| | | |

## Decommission Plan

<!-- optional: migrations — when and how the old system is turned off -->

## Compliance

<!-- optional: personal data, audited systems -->

## Timeline

<!-- optional -->

| Milestone | Date |
|---|---|
| | |

## Evidence

### E1 — <type: command | log | metric | config | official-doc | ticket>

- **Source:** <command + host/context, log query, dashboard URL, file/commit, doc URL, ticket>
- **Collected:** <YYYY-MM-DD HH:MM TZ>

```
<raw output / excerpt>
```

## References

<!-- optional -->

- <related docs, prior proposals, ADRs>
