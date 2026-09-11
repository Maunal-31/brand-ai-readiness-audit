---
name: freshness-corroboration
description: Inspect entity ambiguity, structured data, and source extractability.
license: MIT
---

# Freshness Corroboration

## When to use
Use this skill to determine if a web property is providing clear semantic signals (JSON-LD), unambiguous extractability (inverted pyramid structure), and machine-readable manifests (`llms.txt`).

## Inputs
- `url`: The target URL to audit (string).

## Procedure
1. Fetch the target URL and parse the HTML DOM.
2. Search for `<script type="application/ld+json">`. Evaluate if schema types (Organization, Brand, Product) and `sameAs` authority links are present.
3. Analyze header hierarchies (h1, h2, h3) and adjacent paragraphs. Flag if sections lack concise, answer-first paragraphs.
4. Attempt to fetch `/llms.txt` at the root domain and flag if it is missing.
5. Return structured findings.

## Tools & Scripts
- `scripts/check_semantic_authority.py`: Python script executing the semantic checks.

## Output
Returns a JSON array of finding dictionaries matching the required report schema (`id`, `title`, `severity`, `evidence`, `suggested_action`).
