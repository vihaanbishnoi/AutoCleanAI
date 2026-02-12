import os
from PyPDF2 import PdfReader
from docx import Document


def read_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text


def read_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def load_documents(folder="data"):
    documents = []

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if file.endswith(".txt"):
            documents.append(read_txt(path))

        elif file.endswith(".pdf"):
            documents.append(read_pdf(path))

        elif file.endswith(".docx"):
            documents.append(read_docx(path))

    return documents


def chunk_text(text, chunk_size=400):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks
