import time
from keybert import KeyBERT
from sklearn.feature_extraction.text import TfidfVectorizer
import gradio as gr
import logging

# Set up basic logging for debugging
logging.basicConfig(level=logging.INFO)

# Load the model once to avoid reloading on every request
try:
    # KeyBERT will download the model the first time it runs
    model = KeyBERT('all-mpnet-base-v2')
except Exception as e:
    logging.error(f"Error loading KeyBERT model: {e}")
    model = None


def extract_keywords(text):
    # Initialize default return values
    keybert_kw = 'Error'
    tfidf_kw = 'Error'
    keybert_time = 0.0
    tfidf_time = 0.0

    if not text:
        return (
            'Please provide text.',
            'Please provide text.',
            0.0,
            0.0
        )

    # --- KeyBERT Extraction ---
    if model:
        try:
            start_bert = time.time()
            keywords = model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words='english', top_n=10)
            keywords = [kw[0] for kw in keywords]
            keybert_totaltime = round(time.time() - start_bert, 2)
            keybert_kw = ', '.join(keywords)
        except Exception as e:
            logging.error(f"Error during KeyBERT extraction: {e}")
            keybert_kw = f"KeyBERT Error: {e}"

    # --- TF-IDF Extraction ---
    try:
        start_tfidf = time.time()
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3))
        tfidf_matrix = vectorizer.fit_transform([text])

        if tfidf_matrix.nnz > 0:
            feature_names = vectorizer.get_feature_names_out()
            sorted_indices = tfidf_matrix.toarray().argsort()[0][::-1]
            tfidf_kw = [feature_names[i] for i in sorted_indices[:min(10, len(feature_names))]]
            tfidf_keywords = ', '.join(tfidf_kw)
        else:
            tfidf_kw = "TF-IDF could not find any keywords."

        tfidf_totaltime = round(time.time() - start_tfidf, 2)
    except Exception as e:
        logging.error(f"Error during TF-IDF extraction: {e}")
        tfidf_kw = f"TF-IDF Error: {e}"

    # Crucially, return the four values as a tuple
    return (
        keybert_kw,
        tfidf_kw,
        keybert_totaltime,
        tfidf_totaltime
    )


# Define the Gradio interface
iface = gr.Interface(
    fn=extract_keywords,
    inputs=gr.Textbox(lines=20, label="Enter Text Here"),
    outputs=[
        gr.Textbox(label="KeyBERT Keywords"),
        gr.Textbox(label="TF-IDF Keywords"),
        gr.Textbox(label="KeyBERT Processing Time (s)"),
        gr.Textbox(label="TF-IDF Processing Time (s)")
    ],
    title="Keyword Extraction with KeyBERT and TF-IDF",
    description="A tool to extract keywords from text using two different methods and compare their performance."
)

# Launch the app locally
if __name__ == "__main__":
    iface.launch()