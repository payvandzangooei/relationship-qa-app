import os
import streamlit as st
from pdf_utils import download_pdfs_from_drive, extract_text_from_folder
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

# Load model and tokenizer
@st.cache_resource
def load_model():
    model_id = "distilbert-base-uncased-distilled-squad"
    HF_TOKEN = os.environ.get("HF_TOKEN")  # <-- reads token from Streamlit secrets

    tokenizer = AutoTokenizer.from_pretrained(model_id, token=HF_TOKEN)
    model = AutoModelForQuestionAnswering.from_pretrained(model_id, token=HF_TOKEN)

    return tokenizer, model

tokenizer, model = load_model()

def ask_mistral(context, question, max_tokens=512):
    prompt = f"[INST] You are a relationship advice expert. Based only on the following text:\n\n{context}\n\nAnswer this question:\n{question} [/INST]"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=max_tokens, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

st.title("📄💬 Relationship Advice QA from Google Drive PDFs")

# Google Drive folder link (your link)
drive_folder_url = "https://drive.google.com/drive/folders/1kwncaedGeEguRj3b8K-mwRe3HuMnXmMt"

# Download PDFs into local /pdfs
with st.spinner("Downloading PDFs from Google Drive..."):
    files = download_pdfs_from_drive(drive_folder_url)
    st.write("Files downloaded:", files)


if files:
    context = extract_text_from_folder("pdfs")
    question = st.text_input("Ask your question:")
    if st.button("Get Answer") and question:
        with st.spinner("Thinking..."):
            answer = ask_mistral(context[:2000], question)  # limit context length
            st.write("### 💡 Answer:")
            st.success(answer)
else:
    st.warning("No PDFs found in the Drive folder.")
