import sys
import argparse
import json
import subprocess
import os
from datetime import datetime, timezone
from urllib.parse import urlparse

def run_skill(script_path, url):
    try:
        # Assuming the orchestrator is run from the project root or the skills are relative to project root
        # Better: locate the script relative to this orchestrator file
        orchestrator_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(orchestrator_dir, '..', '..', '..'))
        full_path = os.path.join(project_root, script_path)
        
        result = subprocess.run(
            [sys.executable, full_path, url],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error running {script_path}: {e}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description="Audit Orchestrator")
    parser.add_argument("--url", required=True, help="Target URL to audit")
    parser.add_argument("--output", help="Optional output JSON file path")
    args = parser.parse_args()

    url = args.url
    parsed_url = urlparse(url)
    site = parsed_url.netloc if parsed_url.netloc else url

    findings = []
    
    # 1. Run Crawl & Render Audit
    crawl_findings = run_skill('skills/crawl-render-audit/scripts/check_crawl_render.py', url)
    findings.extend(crawl_findings)
    
    # 2. Run Freshness Corroboration
    semantic_findings = run_skill('skills/freshness-corroboration/scripts/check_semantic_authority.py', url)
    findings.extend(semantic_findings)
    
    # 3. Run Engagement Audit
    engagement_findings = run_skill('skills/engagement-audit/scripts/check_on_site_retention.py', url)
    findings.extend(engagement_findings)
    
    # Deduplicate findings (by ID)
    seen_ids = set()
    unique_findings = []
    for f in findings:
        if f['id'] not in seen_ids:
            seen_ids.add(f['id'])
            unique_findings.append(f)
            
    # Calculate severity stats
    summary = {
        "total_findings": len(unique_findings),
        "critical": sum(1 for f in unique_findings if f.get('severity') == 'critical'),
        "high": sum(1 for f in unique_findings if f.get('severity') == 'high'),
        "medium": sum(1 for f in unique_findings if f.get('severity') == 'medium'),
        "low": sum(1 for f in unique_findings if f.get('severity') == 'low')
    }
    
    # Proactive recommendations
    proactive_improvements = [
        {
            "area": "AI Citations",
            "recommendation": "Deploy an /llms.txt manifest linking canonical product documentation to optimize LLM context window ingestion.",
            "priority": "medium"
        }
    ]
    
    report = {
        "site": site,
        "audited_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": summary,
        "findings": unique_findings,
        "proactive_improvements": proactive_improvements
    }
    
    out_json = json.dumps(report, indent=2)
    print(out_json)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(out_json)

if __name__ == '__main__':
    main()
