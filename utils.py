
import PyPDF2
from transformers import pipeline
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

# Summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def extract_text(file):
    if file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        return "Unsupported file type."

def summarize_document(text, max_length=120, min_length=40):
    if len(text) < 100:
        return "Text too short for summarization."
    return summarizer(text[:1024], max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']

def evaluate_summary(original_text, summary):
    orig_words = set(word_tokenize(original_text.lower()))
    summary_words = set(word_tokenize(summary.lower()))
    common_words = orig_words.intersection(summary_words)

    coverage = len(common_words) / len(orig_words) * 100 if orig_words else 0
    length_ratio = len(summary_words) / len(orig_words) * 100 if orig_words else 0

    return {
        "coverage_percentage": round(coverage, 2),
        "summary_length_percentage": round(length_ratio, 2),
        "summary": summary
    }
