---
name: performance-profiling
description: Evidence-driven performance profiling. Use only when explicitly investigating measured slowness, CPU/memory issues, bundle size, Web Vitals, DB latency, cache/queue bottlenecks, or optimization regressions.
---


# Performance Profiling

Measure first. Optimize the dominant bottleneck, not the most interesting code.

## Workflow

1. Define the slow/expensive user-visible symptom.
2. Establish baseline metrics.
3. Reproduce under representative conditions.
4. Profile the relevant layer.
5. Identify the dominant cost.
6. Make one targeted change.
7. Re-measure.
8. Check regressions and resource tradeoffs.
9. Document meaningful performance assumptions.

## Principles

- Separate latency from throughput.
- Separate average from tail latency.
- Distinguish client, network, server, DB and external dependency time.
- Do not add caching without an invalidation/freshness model.
- Do not add memoization blindly.
- Query optimization should use actual query evidence.
- Node memory issues require heap/resource evidence, not guesswork.
- Bundle improvements should focus on routes users actually load.

## References

- `references/browser-web-vitals.md`
- `references/react-nextjs.md`
- `references/node-cpu-memory.md`
- `references/postgresql-prisma.md`
- `references/redis-queues.md`
- `references/load-testing.md`
- `references/profiling-method.md`
- `references/regression-budgets.md`
