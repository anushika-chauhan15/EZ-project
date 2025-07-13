
import streamlit as st
from utils import extract_text, summarize_document, evaluate_summary

st.set_page_config(page_title="AI Document Assistant", layout="centered")
st.title("📚 AI Document Assistant")

uploaded_file = st.file_uploader("Upload your document (.pdf or .txt)", type=["pdf", "txt"])

if uploaded_file is not None:
    with st.spinner("🔍 Extracting text..."):
        text = extract_text(uploaded_file)

    if text.startswith("Unsupported"):
        st.error(text)
    else:
        st.subheader("📄 Original Text")
        st.text_area("Extracted Text", value=text, height=300)

        if st.button("Summarize & Evaluate"):
            with st.spinner("✍️ Summarizing..."):
                summary = summarize_document(text)
                evaluation = evaluate_summary(text, summary)

            st.subheader("📝 Summary")
            st.write(summary)

            st.subheader("📊 Evaluation")
            st.write(f"**Coverage:** {evaluation['coverage_percentage']}%")
            st.write(f"**Summary Length:** {evaluation['summary_length_percentage']}%")
