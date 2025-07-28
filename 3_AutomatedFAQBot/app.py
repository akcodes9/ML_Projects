# app.py

import streamlit as st
from AutomatedFAQ_logic import faq_bot, get_answer

# Page config
st.set_page_config(
    page_title="Swinburne FAQ Bot",
    page_icon="🎓",
    layout="centered"
)

# Title
st.title("🎓 Swinburne Online FAQ Assistant")
st.markdown("Ask any question about admissions, courses, fees, placements, and more!")

# Load system on startup
if 'loaded' not in st.session_state:
    with st.spinner("Loading FAQ system... This may take 10-20 seconds on first run."):
        faq_bot()
    st.session_state.loaded = True
    st.success("Ready! Ask your question below.")

# Input
user_question = st.text_input("Your Question", placeholder="e.g., Can international students apply?")

if user_question:
    with st.spinner("Searching for the best answer..."):
        result = get_answer(user_question, threshold=0.45)  # Lowered slightly for usability

    # Display result
    st.markdown("### 💬 Answer")
    st.write(result["answer"])

    # Show confidence and matched question in expander
    with st.expander("🔍 Details"):
        if result["matched_question"]:
            st.markdown(f"**Matched FAQ:** {result['matched_question']}")
        st.markdown(f"**Confidence Score:** {result['confidence']:.3f}")
        st.markdown("""
        > *Note: Score > 0.6 = high confidence, 0.5–0.6 = medium, < 0.5 = low match.*
        """)