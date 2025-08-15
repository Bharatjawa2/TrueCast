import hashlib
import yaml
import feedparser
import trafilatura
from urllib.parse import urlparse
from datetime import datetime, timezone
from .config import Settings
from .indexing import embed_and_add
from .utils import html_to_text, canonical_url

SET = Settings()
_seen = set()  # keep track of already ingested articles

def _hash(s: str) -> str:
    """Generate SHA256 hash for deduplication."""
    return hashlib.sha256(s.encode()).hexdigest()

def _parse_feed(feed_url: str):
    return feedparser.parse(feed_url)

def normalize_article(entry):
    """Extract and normalize key fields from RSS entry."""
    url = canonical_url(entry.get('link', ''))
    title = entry.get('title', '')
    published = entry.get('published', '') or entry.get('updated', '')
    try:
        published_dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).isoformat()
    except Exception:
        published_dt = datetime.now(timezone.utc).isoformat()
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded) if downloaded else ''
    return {
        'id': _hash(url),
        'url': url,
        'site': urlparse(url).netloc,
        'title': title,
        'published': published_dt,
        'text': text or html_to_text(downloaded or ''),
    }

def run_ingestion_once():
    """Fetch new articles from feeds, process, and index them."""
    with open(SET.FEEDS_FILE, 'r') as f:
        feeds = yaml.safe_load(f)['sources']
    new_docs = 0
    for src in feeds:
        if src['type'] != 'rss':
            continue
        fp = _parse_feed(src['url'])
        for e in fp.entries[:50]:
            url = canonical_url(e.get('link', ''))
            h = _hash(url)
            if h in _seen:
                continue
            art = normalize_article(e)
            if len((art['text'] or '').strip()) < 300:
                continue
            embed_and_add(art)
            _seen.add(h)
            new_docs += 1
    return new_docs

def manual_ingest_url(url: str):
    """Manually add a single article URL to the index."""
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded) if downloaded else ''
        if not text:
            return False
        art = {
            'id': _hash(url),
            'url': canonical_url(url),
            'site': urlparse(url).netloc,
            'title': '',
            'published': datetime.now(timezone.utc).isoformat(),
            'text': text
        }
        embed_and_add(art)
        return True
    except Exception:
        return False
