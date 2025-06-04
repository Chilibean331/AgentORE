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
