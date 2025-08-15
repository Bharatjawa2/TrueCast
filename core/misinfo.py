from transformers import pipeline
from .config import Settings
from .retriever import retrieve_with_context

SET = Settings()

# Load NLI model for stance detection
_nli = pipeline("text-classification", model=SET.MODEL_NLI)

def check_misinformation(claim: str):
    """
    Retrieve evidence, compare claim with each evidence chunk using NLI.
    Return stance counts and a simple misinfo flag.
    """
    context_str, hits = retrieve_with_context(claim)
    results = []

    agree, disagree, neutral = 0, 0, 0
    for h in hits:
        out = _nli(f"{claim} </s> {h['text']}", truncation=True)
        label = out[0]['label'].lower()
        score = float(out[0]['score'])
        results.append({
            "chunk": h['text'],
            "site": h['site'],
            "label": label,
            "score": score
        })
        if "entail" in label or "support" in label:
            agree += 1
        elif "contradict" in label or "refute" in label:
            disagree += 1
        else:
            neutral += 1

    misinfo_flag = disagree > agree
    return {
        "claim": claim,
        "agree": agree,
        "disagree": disagree,
        "neutral": neutral,
        "misinformation_flag": misinfo_flag,
        "evidence": results
    }
