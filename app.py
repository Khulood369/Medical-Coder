import streamlit as st
import fitz  # PyMuPDF
import csv

st.set_page_config(page_title="ICD-10 Medical Coder")
st.title("🩺 المرمّز الطبي ICD-10")
st.write("✨ ارفع تقرير طبي (PDF) لاستخراج النصوص واقتراح الأكواد.")

# تحميل ملف ICD-10
def load_icd10(file_path):
    codes = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # تخطي العنوان
        for row in reader:
            if len(row) >= 2:
                disease = row[0].strip()
                code = row[1].strip()
                codes[disease] = code
    return codes

icd10 = load_icd10("icd10.csv")

# رفع PDF
pdf = st.file_uploader("📂 ارفع التقرير الطبي (PDF)", type=["pdf"])

def extract_text_from_pdf(pdf_bytes):
    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

if pdf is not None:
    pdf_bytes = pdf.read()
    text = extract_text_from_pdf(pdf_bytes)
    st.subheader("📄 النص المستخرج:")
    st.write(text)

    st.subheader("🔎 الأكواد المقترحة:")
    for disease, code in icd10.items():
        if disease in text:
            st.write(f"{disease} → {code}")
