import streamlit as st
from core.ingestion import run_ingestion_once, manual_ingest_url
from core.generator import generate_fact_checked_answer
from core.misinfo import check_misinformation
from core.credibility import assess_sources

st.set_page_config(page_title="Real-time News RAG Fact-Checker", layout="wide")

st.title("📰 Real-time News RAG Fact-Checker")

tab1, tab2, tab3 = st.tabs(["Ask a Question", "Check a Claim", "Manage Feeds"])

with tab1:
    st.subheader("Ask a Fact-Checked Question")
    query = st.text_input("Enter your question about recent news:")
    if st.button("Get Fact-Checked Answer", type="primary"):
        with st.spinner("Retrieving and verifying..."):
            answer, hits = generate_fact_checked_answer(query)
            
            # Check if using fallback mode
            if "*Note: This response was generated using local processing due to API limitations.*" in answer:
                st.warning("⚠️ Using local processing mode (OpenAI API quota exceeded)")
            
            st.markdown("### Answer")
            st.write(answer)
            st.markdown("### Retrieved Sources")
            for h in hits:
                st.markdown(f"- **{h['site']}**: {h['title']} ([link]({h['url']}))")

with tab2:
    st.subheader("Check a Specific Claim")
    claim = st.text_input("Enter a claim to verify:")
    if st.button("Run Misinformation Check", type="primary"):
        with st.spinner("Analyzing claim..."):
            res = check_misinformation(claim)
            st.write(res)
            if res["evidence"]:
                st.markdown("### Evidence")
                for ev in res["evidence"]:
                    st.markdown(f"- **{ev['site']}** [{ev['label']} {ev['score']:.2f}]: {ev['chunk']}")

with tab3:
    st.subheader("Feed Management & Manual Ingestion")
    if st.button("Run Feed Ingestion Now"):
        added = run_ingestion_once()
        st.success(f"Added {added} new articles.")
    manual_url = st.text_input("Manual Article URL:")
    if st.button("Ingest URL"):
        ok = manual_ingest_url(manual_url)
        if ok:
            st.success("Article ingested successfully!")
        else:
            st.error("Failed to ingest article.")
