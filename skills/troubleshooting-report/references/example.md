---
title: API pods OOMKilled after upgrading to image v2.4.0
date: 2026-10-21
author: ops-team
severity: high
status: resolved
systems: [kubernetes, orders-api]
tags: [oomkilled, memory, deployment]
---

# API pods OOMKilled after upgrading to image v2.4.0

<!-- Illustrative example of a finished document. Hostnames and values are made up. -->

## Summary

- **Symptom:** `orders-api` pods restarted repeatedly with `OOMKilled` after the v2.4.0 rollout [E1]
- **Cause:** v2.4.0 raised the default in-memory cache size beyond the 512Mi container limit (Confirmed) [E3][E4]
- **Fix:** Set `CACHE_MAX_MB=128` in the deployment and rolled out again [E5]

## Symptoms

From 14:05 KST, all 3 `orders-api` pods in `prod` restarted every few minutes.
Error rate on `/orders` rose to 18% [E2].

Pod status (verbatim) [E1]:

```
    Last State:     Terminated
      Reason:       OOMKilled
      Exit Code:    137
```

## Environment

| Item | Value | Evidence |
|---|---|---|
| Cluster | EKS 1.31, namespace `prod` | [E1] |
| `orders-api` image | `v2.4.0` (previous `v2.3.2`) | [E1] |
| Memory limit | `512Mi` | [E1] |

## Root Cause

**Confidence:** Confirmed

- **Direct cause:** Container memory exceeded the 512Mi limit and was killed by the kernel OOM killer [E1]
- **Underlying cause:** v2.4.0 changed the default `CACHE_MAX_MB` from 128 to 512 [E4], so the cache alone could fill the container limit. Memory grew steadily to the limit before each restart [E3].

## Resolution

1. Pin the cache size in the deployment [E5]

   ```sh
   kubectl -n prod set env deployment/orders-api CACHE_MAX_MB=128
   ```

## Verification

No restarts for 2 hours after rollout, and memory stabilized around 230Mi [E6].

## Investigation

| # | Hypothesis | How checked | Result | Evidence |
|---|---|---|---|---|
| 1 | Node memory pressure | `kubectl describe node` conditions | Ruled out: `MemoryPressure False` on all nodes | [E7] |
| 2 | New cache default | Release notes for v2.4.0 | Confirmed | [E4] |

## Follow-up

- [ ] Set `CACHE_MAX_MB` explicitly in the Helm chart values — owner: ops-team, due: 2026-10-28
- [ ] Add a memory-usage alert at 80% of the limit — owner: ops-team, due: 2026-10-28

## Evidence

### E1 — command

- **Source:** `kubectl -n prod describe pod orders-api-7d9f8c-x2k4p` (context `prod-eks`)
- **Collected:** 2026-10-21 14:12 KST

```
Containers:
  orders-api:
    Image:          registry.example.com/orders-api:v2.4.0
    ...
    Last State:     Terminated
      Reason:       OOMKilled
      Exit Code:    137
    Restart Count:  4
    Limits:
      memory:  512Mi
```

### E2 — metric

- **Source:** Grafana `orders-api / HTTP`, query `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))`
- **Collected:** 2026-10-21 14:15 KST, range 13:30–14:15

```
14:00  0.4%
14:10  17.9%
```

### E3 — metric

- **Source:** Prometheus `container_memory_working_set_bytes{pod=~"orders-api.*"}`
- **Collected:** 2026-10-21 14:20 KST, range 14:00–14:20

```
14:06  198Mi
14:09  402Mi
14:11  509Mi  (restart)
```

### E4 — official-doc

- **Source:** https://github.com/example/orders-api/releases/tag/v2.4.0
- **Collected:** 2026-10-21 14:30 KST

```
- Default CACHE_MAX_MB increased from 128 to 512.
```

### E5 — command

- **Source:** `kubectl -n prod rollout status deployment/orders-api` (context `prod-eks`)
- **Collected:** 2026-10-21 14:41 KST

```
deployment "orders-api" successfully rolled out
```

### E6 — command

- **Source:** `kubectl -n prod get pods -l app=orders-api` and `kubectl -n prod top pods -l app=orders-api` (context `prod-eks`)
- **Collected:** 2026-10-21 16:45 KST

```
NAME                          READY   STATUS    RESTARTS   AGE
orders-api-5b6c9d-a1b2c       1/1     Running   0          2h4m
...
NAME                          CPU(cores)   MEMORY(bytes)
orders-api-5b6c9d-a1b2c       120m         231Mi
```

### E7 — command

- **Source:** `kubectl describe node ip-10-0-1-23` (context `prod-eks`)
- **Collected:** 2026-10-21 14:18 KST

```
Conditions:
  Type             Status
  MemoryPressure   False
```
