import streamlit as st
from pdf2image import convert_from_path
from PIL import Image
import os
import tempfile
import spacy

# 🧠 Custom modules
from ocr_module import extract_text
from ner_summary import extract_entities, generate_summary

# 🎯 Streamlit App Title
st.title("📄 DocuSight AI - Smart Document Analyzer")

# 📥 File Upload
uploaded_file = st.file_uploader("Upload a scanned document (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"])

# Initialize global variables
raw_text = None
img = None

# 🧠 Load spaCy Model for Text Classification
nlp = spacy.load("en_core_web_sm")  # Load spaCy's small model (you can use a larger model if needed)

# Define the function to classify the document
def classify_document(text):
    # Process the text through the spaCy model
    doc = nlp(text)
    
    # Example document categories and simple classification logic
    labels = ["Invoice", "Contract", "Report", "Letter"]
    scores = []

    # Dummy logic: Check for keywords in the text for classification
    for label in labels:
        score = sum(label.lower() in text.lower() for label in labels)  # Simple keyword match
        scores.append(score)
    
    # Get the index of the highest score
    doc_type = labels[scores.index(max(scores))]
    classification_result = {
        "labels": labels,
        "scores": scores
    }

    return doc_type, classification_result

# 📁 Handle Uploaded File
if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == 'pdf':
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        images = convert_from_path(temp_file_path, first_page=1, last_page=1)
        img = images[0]

        os.remove(temp_file_path)
    else:
        img = Image.open(uploaded_file)

    # 🖼️ Show Uploaded Image
    st.image(img, caption="Uploaded Document", use_column_width=True)

    # 🔍 OCR and Processing
    if st.button("🔍 Extract Text"):
        with st.spinner("Extracting text..."):
            raw_text = extract_text(img)
            st.text_area("📜 Extracted Text", raw_text, height=300)

        if raw_text:
            # 🧠 Document Classification
            st.subheader("📑 Document Type")
            doc_type, classification_result = classify_document(raw_text)
            st.info(f"**Predicted Type:** {doc_type}")

            with st.expander("See Confidence Scores"):
                for label, score in zip(classification_result['labels'], classification_result['scores']):
                    st.write(f"{label}: {score:.2%}")

            # 🏷️ Named Entity Recognition
            st.subheader("🏷️ Key Entities")
            entities = extract_entities(raw_text)
            for text, label in entities:
                st.markdown(f"- **{label}**: `{text}`")

            # 📝 Text Summary
            st.subheader("📝 Summary")
            summary = generate_summary(raw_text)
            st.success(summary)

            # 📄 Section Detection
            st.subheader("📄 Section Detection")
            section_keywords = {
                "Signature": ["signature", "signed by", "sign here"],
                "Terms & Conditions": ["terms and conditions", "subject to the following", "the following terms"],
                "Expiry": ["expires on", "valid until", "expiry date"],
                "Agreement": ["this agreement", "agrees to", "mutual consent"],
                "Date": ["date", "dated on", "documented on"]
            }

            found_sections = {}
            for section, keywords in section_keywords.items():
                found_sections[section] = any(keyword in raw_text.lower() for keyword in keywords)

            for section, found in found_sections.items():
                icon = "✅" if found else "❌"
                st.write(f"{icon} {section}")

            missing_sections = [s for s, found in found_sections.items() if not found]
            if not missing_sections:
                st.success("✅ All critical sections detected.")
            else:
                st.warning("⚠️ Missing sections: " + ", ".join(missing_sections))
