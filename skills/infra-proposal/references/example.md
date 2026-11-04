---
title: Introduce Velero for scheduled backups of the prod cluster
author: ops-team
date: 2026-10-27
status: accepted
change_type: new
environments: [stg, prod]
systems: [kubernetes, s3]
owner_team: platform-ops
reviewers: [infra-lead, security]
related: [OPS-412, docs/troubleshooting/2026-09-14-configmap-deleted.md]
---

# Introduce Velero for scheduled backups of the prod cluster

<!-- Illustrative example of a finished document. Names and values are made up. -->

## Summary

- **What:** Run Velero in `prod-eks` with daily backups of all namespaces to a dedicated S3 bucket
- **Why:** There is no cluster-level backup; the last accidental deletion took 3h 10m to rebuild by hand [E1][E2]
- **Expected outcome:** Namespace restore in under 30 minutes (estimate: stg restore test took 12 min [E5])
- **Prod impact:** No downtime; adds one deployment in a new `velero` namespace

## Background and Problem

Cluster state (ConfigMaps, Secrets, CRDs) is backed up nowhere outside of git,
and 23% of prod resources are not managed in git [E3]. On 2026-09-14 a deleted
ConfigMap caused a 3h 10m outage while it was recreated from memory and Slack
history [E1].

## Goals and Non-goals

**Goals**

- Daily backup of all prod namespaces, retained 30 days
- Restore a single namespace in under 30 minutes (RTO), losing at most 24h (RPO)

**Non-goals**

- Database backups (RDS snapshots already cover them [E4])
- Moving unmanaged resources into git (separate proposal OPS-418)

## Current State (As-Is)

| Item | Value | Evidence |
|---|---|---|
| Cluster | EKS 1.31, 14 namespaces | [E3] |
| Resources not in git | 23% (412 of 1,790) | [E3] |
| Cluster backup | None | [E3] |

## Proposed Design (To-Be)

### Architecture

Velero server in namespace `velero`, AWS plugin, backups to
`s3://example-prod-velero` (versioned, Object Lock 30 days). EBS volumes via
CSI snapshots.

### Network

Outbound to S3 through the existing VPC endpoint only. No inbound exposure.

### Permissions

IRSA role `velero-prod`: `s3:PutObject/GetObject/ListBucket` on the bucket,
`ec2:CreateSnapshot/DescribeSnapshots` scoped by tag. No delete on the bucket
(Object Lock enforces retention).

### Configuration / IaC

New Terraform module `modules/velero` and Helm release in `platform/velero/values.yaml`.

## Alternatives Considered

| Option | Operational burden | Cost | Lock-in | Team skill fit | Vendor support / license | Decision |
|---|---|---|---|---|---|---|
| Do nothing | None | $0 | — | — | — | Rejected: repeat of the 2026-09-14 outage [E1] |
| Velero (proposed) | Low: one deployment | ~$18/month (estimate) | Low: open format | Used in stg already | Apache 2.0, active project [E6] | Chosen |
| AWS Backup for EKS | Low | Higher per-GB | High: AWS only | New to team | AWS support | Rejected: lock-in, no stg parity |

## Operational Impact

| Area | Assessment |
|---|---|
| Availability | Not in the request path; failure only stops backups. Alert on failed backup. |
| Capacity / performance | Backup of 1,790 objects took 2m 40s in stg [E5]; negligible API load (estimate) |
| Security | Bucket has Secrets in it: SSE-KMS, no public access, access limited to IRSA role and break-glass admin |
| Cost | ~$18/month (estimate: 30 backups × 1.2 GB × $0.023/GB + snapshots ~$10 [E5]) |
| Observability | `velero_backup_failure_total` alert to #ops-alerts; Grafana dashboard 12345 imported before prod rollout |
| Operational burden | platform-ops owns; runbook `runbooks/velero-restore.md`; upgrade with quarterly EKS upgrades |
| Backup / DR | RPO 24h, RTO 30m; monthly restore test into a scratch namespace |

## Rollout Plan

| Phase | Scope | Pre-checks | Go / No-go criteria | Downtime |
|---|---|---|---|---|
| 1 | stg | Bucket + IRSA applied | 3 daily backups succeed, restore test passes | None |
| 2 | prod | Alert and dashboard live | First backup succeeds, restore of `default` to scratch ns passes | None |

## Rollback Plan

- **Trigger:** Velero causes API server errors or backups expose data outside the bucket policy
- **Steps:**

  ```sh
  helm -n velero uninstall velero
  kubectl delete namespace velero
  ```

- **Expected duration:** 5 minutes
- **Point of no return:** None (backups in S3 are kept by Object Lock)

## Success Criteria

| Metric | Query / source | Target | Observation window |
|---|---|---|---|
| Backup success | `velero_backup_success_total` vs `velero_backup_attempt_total` | 100% | 30 days |
| Restore time | Monthly restore test log | < 30 min | First 2 tests |

## Open Questions and Dependencies

| Question / dependency | Owner | Needed by |
|---|---|---|
| Security sign-off on storing Secrets in S3 | security | 2026-11-03 (approved) |

## Evidence

### E1 — ticket

- **Source:** docs/troubleshooting/2026-09-14-configmap-deleted.md
- **Collected:** 2026-10-27 10:00 KST

```
status: resolved
- **Symptom:** checkout-api 503 after `payment-config` ConfigMap deleted
Timeline: 11:02 detected ... 14:12 recovered
```

### E2 — metric

- **Source:** Grafana `checkout-api / SLO`, range 2026-09-14 10:50–14:30 KST
- **Collected:** 2026-10-27 10:05 KST

```
error_rate > 5%: 11:02 – 14:12 (3h 10m)
```

### E3 — command

- **Source:** `kubectl get all,cm,secret -A --no-headers | wc -l` and `scripts/unmanaged-resources.sh` (context `prod-eks`)
- **Collected:** 2026-10-27 10:20 KST

```
1790
unmanaged: 412 / 1790 (23.0%)
velero: namespace not found
```

### E4 — command

- **Source:** `aws rds describe-db-instances --query 'DBInstances[].BackupRetentionPeriod'`
- **Collected:** 2026-10-27 10:25 KST

```
[
    14
]
```

### E5 — command

- **Source:** `velero backup describe stg-daily-20261026 --details` (context `stg-eks`) and restore test log
- **Collected:** 2026-10-27 10:40 KST

```
Phase:  Completed
Started:    2026-10-26 03:00:01 +0900 KST
Completed:  2026-10-26 03:02:41 +0900 KST
Total items to be backed up:  1702
...
Restore stg-restore-test: Completed in 12m04s
```

### E6 — official-doc

- **Source:** https://github.com/vmware-tanzu/velero (LICENSE, releases)
- **Collected:** 2026-10-27 11:00 KST

```
Apache License 2.0
```
