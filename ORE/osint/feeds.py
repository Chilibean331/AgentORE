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
