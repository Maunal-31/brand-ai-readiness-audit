import sys
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def main(url):
    findings = []
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    # 1. robots.txt verification
    ai_bots = ['GPTBot', 'ClaudeBot', 'PerplexityBot', 'Google-Extended', 'Applebot-Extended']
    robots_url = f"{base_url}/robots.txt"
    try:
        r_robots = requests.get(robots_url, timeout=10)
        if r_robots.status_code == 200:
            lines = r_robots.text.split('\n')
            current_agent = None
            for line in lines:
                line = line.strip()
                if line.lower().startswith('user-agent:'):
                    current_agent = line.split(':')[1].strip()
                elif line.lower().startswith('disallow:') and current_agent in ai_bots:
                    path = line.split(':')[1].strip()
                    if path == '/':
                        findings.append({
                            "id": "CRAWL-001",
                            "title": "Robots.txt disallows AI retrieval bots",
                            "severity": "critical",
                            "evidence": f"Found 'User-agent: {current_agent} Disallow: {path}' in {robots_url}",
                            "suggested_action": {
                                "summary": f"Allow {current_agent} in robots.txt to restore AI discoverability.",
                                "priority": "high"
                            }
                        })
    except requests.RequestException:
        pass

    # 2. Bot blocking / HTTP status
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    try:
        r_page = requests.get(url, headers=headers, timeout=10)
        if r_page.status_code in [401, 403]:
            findings.append({
                "id": "CRAWL-002",
                "title": "Bot blocking detected",
                "severity": "high",
                "evidence": f"Received HTTP {r_page.status_code} when querying with synthetic agent headers.",
                "suggested_action": {
                    "summary": "Whitelist common AI user agents or reduce overly aggressive WAF rules.",
                    "priority": "high"
                }
            })
        
        # 3. Client-side rendering vs SSR check
        if r_page.status_code == 200:
            html_content = r_page.text
            soup = BeautifulSoup(html_content, 'html.parser')
            text_content = soup.get_text(strip=True)
            
            raw_len = len(html_content)
            text_len = len(text_content)
            
            if raw_len > 1000 and text_len < raw_len * 0.05:
                findings.append({
                    "id": "CRAWL-003",
                    "title": "Client-side rendering without SSR detected",
                    "severity": "medium",
                    "evidence": f"Raw HTML size ({raw_len} bytes) vs stripped readable text ({text_len} bytes) ratio is extremely low. Possible empty shell <div id='root'></div>.",
                    "suggested_action": {
                        "summary": "Implement Server-Side Rendering (SSR) or dynamic rendering so RAG parsers can extract content.",
                        "priority": "medium"
                    }
                })
    except requests.RequestException as e:
        findings.append({
            "id": "CRAWL-ERR",
            "title": "Target Unreachable",
            "severity": "critical",
            "evidence": str(e),
            "suggested_action": {
                "summary": "Ensure the target URL is accessible from external networks.",
                "priority": "high"
            }
        })

    print(json.dumps(findings))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("[]")
