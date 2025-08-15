import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse

def html_to_text(html: str) -> str:
    """Convert HTML content to clean plain text."""
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(" ", strip=True)

def canonical_url(url: str) -> str:
    """Normalize URL by removing tracking parameters and lowercasing host."""
    parts = list(urlparse(url))
    # drop tracking params like utm_source, fbclid
    if parts[4]:
        qs = '&'.join(p for p in parts[4].split('&') if not p.startswith(('utm_', 'fbclid')))
        parts[4] = qs
    # normalize scheme and host
    parts[0] = parts[0] or 'https'
    parts[1] = parts[1].lower().lstrip('www.')
    return urlunparse(parts)
