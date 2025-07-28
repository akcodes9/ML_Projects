# faq_bot.py

from datasets import load_dataset
from sentence_transformers import SentenceTransformer, util
import pickle
import os

# Paths for caching
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)
DF_CACHE = os.path.join(CACHE_DIR, "df.pkl")
EMB_CACHE = os.path.join(CACHE_DIR, "q_emb.pt")

# Global variables
df = None
model = None
q_emb = None


def faq_bot():
    """
    Load the FAQ dataset and precompute question embeddings.
    """
    global df, model, q_emb

    print("Loading dataset: khaxtran/swin-faqs...")
    dataset = load_dataset("khaxtran/swin-faqs")
    df = dataset['train'].to_pandas()

    print("Loading Sentence Transformer model on CPU...")
    model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')  # ← Force CPU

    print("Encoding FAQ questions...")
    questions = df['question'].tolist()
    q_emb = model.encode(questions, convert_to_tensor=True)  # Will run on CPU

    print(f"FAQ system loaded with {len(df)} questions.")
    return df, model, q_emb

def get_answer(user_question, threshold=0.5):
    """
    Return answer using context and confidence.
    """
    global df, model, q_emb

    user_embedding = model.encode([user_question], convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(user_embedding, q_emb)[0]
    best_score = similarities.max().item()
    idx_max = similarities.argmax().item()

    if best_score < threshold:
        return {
            "answer": "I couldn't find a relevant answer to your question. Please rephrase or contact support.",
            "confidence": best_score,
            "matched_question": None
        }

    matched_row = df.iloc[idx_max]
    answer_text = matched_row['answers']['text'][0]
    full_context = matched_row['context']
    matched_question = matched_row['question']

    return {
        "answer": full_context,  # ← Using full context for richer response
        "confidence": round(best_score, 3),
        "matched_question": matched_question
    }