
import os
import PyPDF2
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')

# Summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def summarize_text(text, max_length=120, min_length=40):
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

def main():
    file_path = input("Enter the path of the PDF or TXT file: ").strip()

    if not os.path.exists(file_path):
        print("❌ File does not exist.")
        return

    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.txt'):
        text = extract_text_from_txt(file_path)
    else:
        print("❌ Unsupported file format. Use .pdf or .txt")
        return

    print("\n📄 Extracting and summarizing...")
    summary = summarize_text(text)
    evaluation = evaluate_summary(text, summary)

    print("\n📌 Summary:")
    print(summary)
    print("\n📊 Evaluation:")
    print(f"Coverage: {evaluation['coverage_percentage']}%")
    print(f"Summary Length: {evaluation['summary_length_percentage']}%")

if __name__ == "__main__":
    main()
