---
name: crawl-render-audit
description: Inspect technical discoverability and machine access barriers for AI agents.
license: MIT
---

# Crawl & Render Audit

## When to use
Use this skill to determine if a given web property is blocking AI/LLM bots via `robots.txt` or WAFs, and whether the site relies on client-side rendering which impedes simple extraction tools.

## Inputs
- `url`: The target URL to audit (string).

## Procedure
1. Parse the target URL to extract the base domain.
2. Fetch `robots.txt` from the base domain and parse it.
3. Check if common AI bots (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended) are disallowed at the root path `/`.
4. Fetch the target URL using a synthetic User-Agent.
5. Record the HTTP status code (check for 403 or 401).
6. If the page loads successfully (HTTP 200), compute the ratio of raw HTML size to stripped readable text size.
7. Flag if the ratio is extremely low (suggesting client-side rendering without SSR).

## Tools & Scripts
- `scripts/check_crawl_render.py`: A Python script to perform the aforementioned checks.

## Output
Returns a JSON array of finding dictionaries matching the required report schema (`id`, `title`, `severity`, `evidence`, `suggested_action`).
