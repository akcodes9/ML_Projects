from transformers import pipeline

# Load once at startup
summarizer = pipeline("summarization",model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    output = summarizer(text, max_length=90, min_length=20, do_sample=False)
    return output[0]['summary_text']
