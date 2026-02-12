from sentence_transformers import SentenceTransformer
from docx import Document
from PyPDF2 import PdfReader

model = SentenceTransformer('all-MiniLM-L6-v2')


def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None


def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    except:
        return None


def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except:
        return None


def get_document_embedding(file_path):

    text = None

    if file_path.lower().endswith('.txt'):
        text = extract_text_from_txt(file_path)

    elif file_path.lower().endswith('.docx'):
        text = extract_text_from_docx(file_path)

    elif file_path.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_path)

    # 🚨 SAFETY CHECKS
    if text is None:
        return None

    text = str(text).strip()

    if len(text) == 0:
        return None

    # 🚨 LIMIT VERY LARGE FILES (important)
    text = text[:10000]  # limit to first 10k characters

    try:
        embedding = model.encode(text)
        return embedding
    except:
        return None


