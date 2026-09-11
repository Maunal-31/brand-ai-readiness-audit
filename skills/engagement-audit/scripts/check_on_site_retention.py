import sys
import json
import requests
from bs4 import BeautifulSoup
import re

def main(url):
    findings = []
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; EngagementBot/1.0)'}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # 1. Viewport & mobile readiness
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            if not viewport:
                findings.append({
                    "id": "ENGAGE-001",
                    "title": "Missing viewport meta tag",
                    "severity": "high",
                    "evidence": "Could not find <meta name='viewport'> tag in the document head.",
                    "suggested_action": {
                        "summary": "Add a viewport meta tag to ensure correct mobile scaling and responsiveness.",
                        "priority": "high"
                    }
                })
            
            # 2. Interstitial & modal obstruction
            # Very basic heuristic: look for divs with high z-index, 'modal', 'overlay', 'cookie' in class/id
            modal_suspects = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') and any('modal' in c.lower() or 'overlay' in c.lower() or 'cookie' in c.lower() for c in tag.get('class')))
            if len(modal_suspects) > 2: # arbitrary threshold for 'excessive'
                findings.append({
                    "id": "ENGAGE-002",
                    "title": "Potential interstitial or modal obstruction detected",
                    "severity": "medium",
                    "evidence": f"Found {len(modal_suspects)} containers with classes suggesting modals or overlays.",
                    "suggested_action": {
                        "summary": "Minimize disruptive popups or premature lead-gates to reduce cognitive load.",
                        "priority": "medium"
                    }
                })
            
            # 3. Hero clarity & value proposition
            # Heuristic: look at first h1
            h1 = soup.find('h1')
            if h1:
                text = h1.get_text(strip=True)
                words = text.split()
                if len(words) < 3 or len(words) > 15:
                    findings.append({
                        "id": "ENGAGE-003",
                        "title": "Ambiguous hero tagline",
                        "severity": "low",
                        "evidence": f"H1 tag has {len(words)} words, which may be too brief or too verbose for clarity.",
                        "suggested_action": {
                            "summary": "Ensure hero text conveys concrete domain verbs/nouns quickly.",
                            "priority": "low"
                        }
                    })
            else:
                findings.append({
                    "id": "ENGAGE-003",
                    "title": "Missing H1 hero tag",
                    "severity": "medium",
                    "evidence": "No <h1> tag found on the page.",
                    "suggested_action": {
                        "summary": "Add an H1 tag for the main value proposition.",
                        "priority": "medium"
                    }
                })
                
            # 4. Text density & scannability
            # Heuristic: find paragraphs longer than 500 chars without lists
            paragraphs = soup.find_all('p')
            wall_of_text = False
            for p in paragraphs:
                if len(p.get_text(strip=True)) > 500:
                    wall_of_text = True
                    break
            
            if wall_of_text and len(soup.find_all(['ul', 'ol', 'table'])) == 0:
                findings.append({
                    "id": "ENGAGE-004",
                    "title": "Poor text scannability (Wall of Text)",
                    "severity": "low",
                    "evidence": "Found long paragraphs (>500 chars) with no lists or tables detected on the page.",
                    "suggested_action": {
                        "summary": "Break up dense text with lists, tables, or bold lead-ins.",
                        "priority": "low"
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
