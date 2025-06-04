import feedparser
from datetime import datetime
from .database import add_intel, init_db

NEWS_FEEDS = [
    'https://www.rudaw.net/english/rss',
    'https://www.aljazeera.com/xml/rss/all.xml'
]

def fetch_news(db_path='ore_osint.db'):
    conn = init_db(db_path)
    for feed_url in NEWS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.get('title', '')
            content = entry.get('summary', '')
            url = entry.get('link', '')
            ts = entry.get('published', datetime.utcnow().isoformat())
            add_intel(conn, 'news', title, content, url, ts)

GDELT_EVENTS = 'https://api.gdeltproject.org/api/v2/events/doc?query={query}&maxrecords=50&format=json'
NEWSAPI_URL = 'https://newsapi.org/v2/everything'


def fetch_gdelt(query: str, db_path='ore_osint.db'):
    conn = init_db(db_path)
    url = GDELT_EVENTS.format(query=query)
    try:
        r = feedparser.parse(url)
        for entry in r.entries:
            title = entry.get('title', '')
            url_e = entry.get('sourceurl', '')
            ts = entry.get('seendate', datetime.utcnow().isoformat())
            add_intel(conn, 'gdelt', title, '', url_e, ts)
    except Exception as e:
        print('GDELT error:', e)


def fetch_newsapi(query: str, api_key: str, db_path='ore_osint.db'):
    conn = init_db(db_path)
    params = {'q': query, 'apiKey': api_key, 'pageSize': 50}
    try:
        import requests
        r = requests.get(NEWSAPI_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        for art in data.get('articles', []):
            title = art.get('title', '')
            url = art.get('url', '')
            ts = art.get('publishedAt', datetime.utcnow().isoformat())
            add_intel(conn, 'newsapi', title, art.get('description', ''), url, ts)
    except Exception as e:
        print('NewsAPI error:', e)

OSINTCOMBINE_URL = 'https://api.osintcombine.com/search'


def fetch_osint_combine(query: str, api_key: str, db_path='ore_osint.db'):
    conn = init_db(db_path)
    params = {'q': query, 'key': api_key}
    try:
        import requests
        r = requests.get(OSINTCOMBINE_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        for item in data.get('data', []):
            title = item.get('title', '')
            url = item.get('url', '')
            ts = item.get('date', datetime.utcnow().isoformat())
            add_intel(conn, 'osintcombine', title, '', url, ts)
    except Exception as e:
        print('OSINT Combine error:', e)
