import subprocess
import json
from datetime import datetime
from .database import add_intel, init_db

# Uses snscrape command line tool. Ensure installed separately.

def scrape_twitter(query: str, limit: int = 50, db_path='ore_osint.db'):
    conn = init_db(db_path)
    cmd = [
        'snscrape', '--jsonl', '--max-results', str(limit), 'twitter-search', query
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        data = json.loads(line)
        title = data.get('content', '')[:80]
        url = data.get('url', '')
        ts = data.get('date', datetime.utcnow().isoformat())
        add_intel(conn, 'twitter', title, data.get('content', ''), url, ts)

TWITTER_SEARCH_URL = 'https://api.twitter.com/2/tweets/search/recent'


def twitter_api_search(query: str, bearer_token: str, db_path='ore_osint.db'):
    conn = init_db(db_path)
    headers = {'Authorization': f'Bearer {bearer_token}'}
    params = {'query': query, 'max_results': 10}
    try:
        import requests
        r = requests.get(TWITTER_SEARCH_URL, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        for t in data.get('data', []):
            title = t.get('text', '')[:80]
            ts = t.get('created_at', datetime.utcnow().isoformat())
            add_intel(conn, 'twitter_api', title, t.get('text', ''), '', ts)
    except Exception as e:
        print('Twitter API error:', e)
