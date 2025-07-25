import streamlit as st
from textsummarizer import summarize_text

st.set_page_config(
    page_title="Text Summarizer",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ----------- Custom Styling ------------
st.markdown("""
    <style>
    /* Hide Streamlit's default header padding */
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem;
        background: transparent !important;
    }

    /* Style the collapsed sidebar toggle button */
    .css-vk3wp9 {
        background-color: #333 !important;
        color: white !important;
        border: 1px solid #666 !important;
        border-radius: 6px !important;
        visibility: visible !important;
    }

    /* Alternative class names for sidebar toggle */
    .stSidebar > div > button,
    button[data-testid="collapsedControl"] {
        background-color: #333 !important;
        color: white !important;
        border: 1px solid #666 !important;
        border-radius: 6px !important;
        visibility: visible !important;
    }

    /* Target the sidebar arrow/hamburger icon */
    .css-vk3wp9 svg {
        fill: white !important;
        color: white !important;
    }

    /* Remove main container background and styling */
    .main {
        background: transparent !important;
        border-radius: 0px !important;
        padding: 30px 35px 30px 35px;
        box-shadow: none !important;
        margin-bottom: 0px !important;
    }

    /* Set overall page background */
    .stApp {
        background-color: #F6F9FB !important;
    }

    textarea {
        background: #F2F5F7 !important;
        color: #222 !important;
        border-radius: 10px !important;
        border: 1.5px solid #D7DBDF !important;
        font-size: 1.05em !important;
        transition: border 0.2s;
    }

    /* Remove white space around text area */
    .stTextArea > div > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    textarea:focus {
        outline: none !important;
        border: 1.5px solid #8CA6DB !important;
    }

    .summary {
        background: linear-gradient(90deg, #355C7D 0%, #6C5B7B 100%);
        color: #fff !important;
        font-weight: 500;
        border-radius: 14px;
        padding: 24px 18px 24px 22px;
        margin-top: 18px;
        font-size: 1.18em;
        letter-spacing: 0.01em;
        box-shadow: 0 8px 26px rgba(38,49,107,0.13);
    }

    .stButton > button {
        background-color: #5369B5 !important;
        color: #fff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .custom-label {
        color: #313D5A;
        font-size: 1.1em;
        font-weight: 500;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------- Page Content ------------
st.markdown('<div class="main">', unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align:center; font-size:2.6em; color:#313D5A;'>📝 Text Summarizer</h1>",
            unsafe_allow_html=True)
st.write(
    "<div style='text-align:center; color:#535C73; font-size:1.05em;'>Summarize long articles or documents instantly. Powered by AI.</div>",
    unsafe_allow_html=True)
st.write(" ")

# Custom input label
st.markdown('<div class="custom-label">Please enter the text you would like to summarize</div>', unsafe_allow_html=True)

# Text area
user_input = st.text_area(
    label="",
    height=200,
    placeholder="Paste your text here..."
)

# Summarize button
summarize = st.button("✨ Summarize", key="summarize_button")

# Processing
if summarize:
    if user_input.strip():
        with st.spinner("Summarizing..."):
            try:
                summary = summarize_text(user_input)
                st.markdown('<div class="summary"><b>Summary:</b><br>{}</div>'.format(summary), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Sorry, something went wrong: {e}")
    else:
        st.warning("Please enter some text to summarize.")

st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("About")
st.sidebar.info(
    """
    - Built with Streamlit and DistilBART-CNN-12-6
    - [Streamlit Docs](https://docs.streamlit.io/)
    - Model: sshleifer/distilbart-cnn-12-6
    """
)