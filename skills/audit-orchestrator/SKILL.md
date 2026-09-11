---
name: audit-orchestrator
description: Entrypoint orchestrator that triggers worker skills, deduplicates findings, calculates severity statistics, and formats the final JSON report.
license: MIT
---

# Audit Orchestrator

## When to use
Use this skill as the primary entrypoint to run a full multi-skill audit against a target web property.

## Inputs
- `--url`: The target URL to audit (string, required).
- `--output`: Optional output JSON file path.

## Procedure
1. Parse the input URL and initialize an empty findings list.
2. Trigger the `crawl-render-audit` worker skill and append its findings.
3. Trigger the `freshness-corroboration` worker skill and append its findings.
4. Trigger the `engagement-audit` worker skill and append its findings.
5. Deduplicate the collected findings by `id`.
6. Calculate severity statistics (critical, high, medium, low).
7. Inject proactive recommendations.
8. Construct and emit the final JSON report adhering to the marketplace schema.

## Tools & Scripts
- `scripts/orchestrate_audit.py`: The main orchestrator script.

## Output
Emits a structured JSON report to `stdout` (and optionally to a file) containing site info, audit timestamp, summary, findings, and proactive improvements.
