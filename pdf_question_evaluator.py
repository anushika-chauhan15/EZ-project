import fitz  # PyMuPDF
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

nltk.download('punkt')

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def generate_questions(text, num_questions=5):
    sentences = sent_tokenize(text)
    important_sentences = sentences[:num_questions]
    questions = ["What is the meaning or importance of: '" + sent[:50] + "...?" for sent in important_sentences]
    answers = important_sentences
    return list(zip(questions, answers))

def evaluate_answer(user_ans, correct_ans):
    emb1 = model.encode([user_ans])[0].reshape(1, -1)
    emb2 = model.encode([correct_ans])[0].reshape(1, -1)
    similarity = cosine_similarity(emb1, emb2)[0][0]
    return similarity

def run_quiz(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    qa_pairs = generate_questions(text)

    print("Answer the following questions based on the PDF:\n")
    score = 0
    total = len(qa_pairs)
    results = []

    for i, (question, correct_answer) in enumerate(qa_pairs):
        print(f"Q{i+1}: {question}")
        user_answer = input("Your answer: ")
        sim = evaluate_answer(user_answer, correct_answer)
        passed = sim > 0.6
        results.append((question, user_answer, correct_answer, sim, passed))
        if passed:
            score += 1

    print("\nEvaluation Summary:")
    print(f"Score: {score}/{total}\n")
    for i, (q, ua, ca, sim, passed) in enumerate(results):
        result = "✅ Correct" if passed else "❌ Incorrect"
        print(f"Q{i+1}: {result} (Similarity: {sim:.2f})")
        if not passed:
            print(f"  - Correct: {ca}")
            print(f"  - Your answer: {ua}\n")

# Example usage:
# run_quiz('sample.pdf')
