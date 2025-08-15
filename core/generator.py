import os
from openai import OpenAI
from .config import Settings
from .retriever import retrieve_with_context

# Load settings and set API key
SET = Settings()
client = OpenAI(api_key=SET.OPENAI_API_KEY)

SYSTEM_PROMPT = """You are a fact-checking news assistant.
You must:
- Use the provided CONTEXT only (no outside facts unless explicitly stated)
- Cite sources using their 'site' metadata
- Flag possible misinformation
- Provide a credibility score (0–100) based on source reliability and agreement among sources.
"""

def generate_local_answer(context_str: str, query: str, hits: list):
    """
    Generate a fact-checked answer using local processing when OpenAI is unavailable.
    """
    # Calculate credibility score based on source domains
    from .credibility import assess_sources
    credibility_score = assess_sources(hits)
    
    # Simple template-based response
    sources = [h['site'] for h in hits[:3]]  # Top 3 sources
    source_citations = ", ".join([f"[{site}]" for site in sources])
    
    # Determine if there's potential misinformation based on source agreement
    unique_sources = len(set(sources))
    misinformation_flag = "No" if unique_sources >= 2 else "Yes"
    
    answer = f"""Based on the retrieved information from {source_citations}:

{context_str[:500]}...

**Answer**: The available information suggests this topic has been covered by multiple sources. Please refer to the cited sources for detailed information.

**Credibility Score**: {credibility_score}/100
**Misinformation Flag**: {misinformation_flag}

*Note: This response was generated using local processing due to API limitations.*"""
    
    return answer

def generate_fact_checked_answer(query: str):
    """
    Given a query, retrieves relevant context and uses the OpenAI API to
    generate a fact-checked answer with citations, credibility score,
    and misinformation flag. Falls back to local processing if API is unavailable.
    """
    # Retrieve relevant context from the retriever
    context_str, hits = retrieve_with_context(query)

    # Build the prompt for the LLM
    prompt = f"""{SYSTEM_PROMPT}

CONTEXT:
{context_str}

QUESTION:
{query}

INSTRUCTIONS:
Provide a clear answer. Include in-text citations like [site].
End with:
Credibility Score: X/100
Misinformation Flag: Yes/No
"""

    try:
        # Try OpenAI API first
        resp = client.chat.completions.create(model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise and skeptical fact-checking assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0)

        # Return answer text and retrieval hits
        return resp.choices[0].message.content, hits
        
    except Exception as e:
        # Fallback to local processing if OpenAI fails
        if "quota" in str(e).lower() or "429" in str(e) or "insufficient_quota" in str(e):
            answer = generate_local_answer(context_str, query, hits)
            return answer, hits
        else:
            # Re-raise other errors
            raise e
