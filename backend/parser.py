import fitz
from docx import Document
import io
import re
import os
from dotenv import load_dotenv
from groq import Groq

# ======================
# ENV SETUP
# ======================
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("❌ GROQ_API_KEY manquante dans .env")

client = Groq(api_key=API_KEY)

MODEL = "llama-3.1-8b-instant"


# ======================
# PDF EXTRACTION
# ======================
def extract_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")

    text = "\n".join(page.get_text() for page in doc)

    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    return text


# ======================
# DOCX EXTRACTION
# ======================
def extract_docx(file_bytes: bytes) -> str:
    file_stream = io.BytesIO(file_bytes)
    doc = Document(file_stream)

    return "\n".join(
        p.text.strip()
        for p in doc.paragraphs
        if p.text.strip()
    )


# ======================
# AUTO DETECTION
# ======================
def detect_and_extract(file_bytes: bytes, content_type: str) -> str:

    content_type = content_type.lower()

    if "pdf" in content_type:
        text = extract_pdf(file_bytes)

        # amélioration: check intelligent
        if len(text.split()) < 30:
            raise ValueError("❌ PDF probablement scanné ou vide")

        return text

    elif "docx" in content_type or "word" in content_type:
        return extract_docx(file_bytes)

    else:
        return file_bytes.decode("utf-8", errors="ignore")


# ======================
# AI SUMMARY (GROQ - PRO)
# ======================
def summarize_course(text: str) -> str:

    if not text or len(text.strip()) < 20:
        return "❌ Texte vide ou invalide"

    text = text[:8000]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un expert en pédagogie et synthèse de cours. "
                        "Tu dois être clair, structuré et concis."
                    )
                },
                {
                    "role": "user",
                    "content": f"""
Résume ce cours de manière ULTRA CLAIRE.

FORMAT OBLIGATOIRE :

CONCEPTS CLÉS :
- concept : définition simple

POINTS IMPORTANTS :
- point court

RELATIONS ENTRE CONCEPTS :
- liens logiques entre idées

COURS :
{text}
"""
                }
            ],
            temperature=0.3,
            max_tokens=700
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Erreur Groq API: {str(e)}"