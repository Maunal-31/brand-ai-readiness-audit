# Brand AI Readiness Audit Marketplace

A multi-skill agent marketplace for auditing web properties for AI discoverability and visitor engagement. This repository is built as a highly modular, read-only audit architecture according to the Adobe University Hackathon 2026 (Round 3) specifications.

## Architecture

This marketplace strictly adheres to the [agentskills.io](https://agentskills.io) standard, decomposing the audit into distinct skills:

- **audit-orchestrator**: The central entrypoint that accepts arguments, calls worker skills, deduplicates findings, calculates severity statistics, and formats the output schema.
- **crawl-render-audit**: Inspects technical discoverability and machine access barriers (`robots.txt`, WAF bot blocking, SSR vs Client-side rendering).
- **freshness-corroboration**: Inspects semantic authority, `sameAs` entity corroboration, and extraction clarity via structured data and inverted pyramid heuristic analysis.
- **engagement-audit**: Analyzes on-site UX friction including missing viewports, interstitial obstructions, dense text, and vague hero messaging.

## Detected Failure Modes

1. **Off-site Discoverability**: AI agents blocked by `robots.txt`, aggressive WAFs, or relying heavily on client-side rendering without SSR. Missing entity resolution via JSON-LD.
2. **On-site Engagement**: Poor mobile experience, excessive modals/overlays obscuring content, high cognitive load from text walls, and unclear value propositions.

## Setup & Usage

### 1. Requirements

Install the minimal required standard libraries (under 50 MB total package size). No heavy pre-trained models.

```bash
pip install -r requirements.txt
```

### 2. Run an Audit

Execute the orchestrator as the single entrypoint:

```bash
python skills/audit-orchestrator/scripts/orchestrate_audit.py --url https://httpbin.org
```

To save the output to a file:

```bash
python skills/audit-orchestrator/scripts/orchestrate_audit.py --url https://example.com --output report.json
```

## Constraints Met
- Fast and lightweight (< 3 mins execution).
- Non-destructive and strictly read-only.
- Comprehensive `SKILL.md` provided for each worker.
- Valid multi-skill `marketplace.json` manifest.
