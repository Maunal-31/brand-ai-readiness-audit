import sys
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def main(url):
    findings = []
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Bot/1.0)'}
    try:
        r_page = requests.get(url, headers=headers, timeout=10)
        if r_page.status_code == 200:
            soup = BeautifulSoup(r_page.text, 'html.parser')
            
            # 1. JSON-LD Structured Data
            scripts = soup.find_all('script', type='application/ld+json')
            has_org_or_brand = False
            has_same_as = False
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict):
                        typ = data.get('@type', '')
                        if typ in ['Organization', 'Brand', 'Product']:
                            has_org_or_brand = True
                            if 'sameAs' in data:
                                has_same_as = True
                except (json.JSONDecodeError, TypeError):
                    pass
            
            if not has_org_or_brand:
                findings.append({
                    "id": "SEMANTIC-001",
                    "title": "Missing essential JSON-LD structured data",
                    "severity": "medium",
                    "evidence": "Could not find Organization, Brand, or Product schemas in <script type='application/ld+json'>.",
                    "suggested_action": {
                        "summary": "Implement JSON-LD structured data to clearly define entities for LLMs.",
                        "priority": "medium"
                    }
                })
            elif not has_same_as:
                findings.append({
                    "id": "SEMANTIC-002",
                    "title": "Missing 'sameAs' authority links in structured data",
                    "severity": "low",
                    "evidence": "JSON-LD schema found but 'sameAs' attribute is missing.",
                    "suggested_action": {
                        "summary": "Add sameAs links to authoritative sources like Wikidata, Crunchbase, or LinkedIn.",
                        "priority": "low"
                    }
                })
            
            # 2. Answer extractability / Inverted pyramid
            headers_list = soup.find_all(['h1', 'h2', 'h3'])
            if headers_list:
                poor_extractability = True
                for header in headers_list:
                    # Look at next sibling paragraphs
                    sib = header.find_next_sibling()
                    words = 0
                    while sib and sib.name in ['p', 'div', 'span'] and words < 100:
                        words += len(sib.get_text(strip=True).split())
                        if words >= 40:
                            poor_extractability = False
                            break
                        sib = sib.find_next_sibling()
                
                if poor_extractability:
                    findings.append({
                        "id": "SEMANTIC-003",
                        "title": "Poor answer extractability / inverted pyramid structure",
                        "severity": "medium",
                        "evidence": "Headers are not immediately followed by concise (40-60 word) definitional paragraphs.",
                        "suggested_action": {
                            "summary": "Structure content with an inverted pyramid style: answer immediately under headers before marketing prose.",
                            "priority": "medium"
                        }
                    })

    except requests.RequestException:
        pass

    # 3. Machine documentation manifest (llms.txt)
    try:
        r_llms = requests.get(f"{base_url}/llms.txt", headers=headers, timeout=5)
        if r_llms.status_code != 200:
            findings.append({
                "id": "SEMANTIC-004",
                "title": "Missing machine documentation manifest (/llms.txt)",
                "severity": "low",
                "evidence": f"Failed to retrieve {base_url}/llms.txt (HTTP {r_llms.status_code})",
                "suggested_action": {
                    "summary": "Deploy an /llms.txt manifest linking canonical product documentation to optimize LLM context window ingestion.",
                    "priority": "medium"
                }
            })
    except requests.RequestException:
        pass

    print(json.dumps(findings))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("[]")
