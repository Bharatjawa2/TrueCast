import json
from .config import Settings

SET = Settings()

# Load domain policies if available
try:
    with open(SET.DOMAIN_POLICY, "r") as f:
        DOMAIN_POLICIES = json.load(f)
except FileNotFoundError:
    DOMAIN_POLICIES = {}

DEFAULT_SCORE = 50  # neutral credibility if unknown

def get_domain_score(domain: str) -> int:
    """Return credibility score for a domain from policies or default."""
    return DOMAIN_POLICIES.get(domain, DEFAULT_SCORE)

def assess_sources(hits):
    """
    Compute an aggregated credibility score based on retrieved hits.
    Weigh each source equally for simplicity.
    """
    if not hits:
        return DEFAULT_SCORE
    scores = [get_domain_score(h["site"]) for h in hits]
    avg_score = sum(scores) / len(scores)
    return round(avg_score)
