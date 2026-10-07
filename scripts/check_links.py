"""Check all published HTTPS URLs; keep indeterminate outcomes for human review."""
import concurrent.futures
import datetime
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def check(url):
    item = {'url': url, 'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'GNU-CadetWorld-LinkCheck/1.0'})
        with urllib.request.urlopen(request, timeout=15) as response:
            item.update(http_status=response.status, final_url=response.url, result='http_response_not_identity_verification')
    except urllib.error.HTTPError as exc:
        item.update(http_status=exc.code, final_url=exc.url, result='indeterminate_requires_review')
    except (OSError, urllib.error.URLError) as exc:
        item.update(http_status=None, result='indeterminate_requires_review', detail=str(exc))
    return item

def main():
    urls = set()
    for path in ROOT.rglob('*.md'):
        urls.update(re.findall(r'\]\((https://[^)]+)\)', path.read_text(encoding='utf-8')))
    for row in json.loads((ROOT / 'data/organizations.json').read_text(encoding='utf-8')):
        urls.update(x for x in [row['instagram'], row['facebook'], *row['sources']] if x)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(check, sorted(urls)))
    report = {'note': 'HTTP success is not proof of account ownership. Errors may reflect access restrictions.', 'links': results}
    (ROOT / 'docs/link-checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Checked {len(results)} URLs; {sum(r['result'].startswith('indeterminate') for r in results)} transport/HTTP issues. Identity and page content still require source review.")

if __name__ == '__main__':
    main()
