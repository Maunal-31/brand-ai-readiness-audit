---
name: engagement-audit
description: Inspect on-site human retention, friction, and cognitive load.
license: MIT
---

# Engagement Audit

## When to use
Use this skill to assess a web property for user experience friction, such as intrusive modals, poor text scannability, missing viewport settings, or ambiguous hero messaging.

## Inputs
- `url`: The target URL to audit (string).

## Procedure
1. Fetch the target URL and parse the HTML DOM.
2. Search for a `<meta name="viewport">` tag; flag if missing.
3. Scan DOM elements for intrusive modals, overlays, or cookie banners that obscure content.
4. Analyze the H1 tag length and content to estimate hero clarity.
5. Identify overly dense paragraphs (>500 characters) and check for the presence of lists or tables to gauge text scannability.
6. Return structured findings.

## Tools & Scripts
- `scripts/check_on_site_retention.py`: Python script executing the UX heuristics.

## Output
Returns a JSON array of finding dictionaries matching the required report schema (`id`, `title`, `severity`, `evidence`, `suggested_action`).
