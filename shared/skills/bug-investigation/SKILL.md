---
name: bug-investigation
description: Root-cause debugging workflow. Use for bugs, regressions, crashes, flaky behavior, incorrect data, or hard-to-reproduce failures before changing code.
---


# Bug Investigation

Do not patch the symptom before identifying the most likely cause.

## Workflow

1. Restate the observed vs expected behavior.
2. Gather reproduction conditions.
3. Map the execution path.
4. Inspect recent related changes/configuration.
5. Form a small ranked hypothesis set.
6. Gather evidence that can falsify each hypothesis.
7. Reproduce at the smallest useful scope.
8. Identify the root cause.
9. Implement the smallest robust fix.
10. Add a regression test.
11. Run affected validation.
12. Review for adjacent instances of the same root cause.

## Rules

- Do not make multiple unrelated speculative changes simultaneously.
- Prefer evidence from logs, tests, traces, DB state and runtime behavior.
- If reproduction is impossible, state uncertainty explicitly.
- Distinguish root cause from contributing conditions.
- Do not weaken tests to make the bug disappear.
- Preserve useful diagnostics while removing debug noise before completion.

## References

- `references/reproduction.md`
- `references/hypothesis-testing.md`
- `references/logs-traces.md`
- `references/data-bugs.md`
- `references/concurrency-bugs.md`
- `references/frontend-bugs.md`
- `references/flaky-tests.md`
- `references/regression-fix.md`
