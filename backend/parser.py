"""Parsing de contenus cours (PDF/DOCX/TXT) + résumé optionnel via Groq."""

from __future__ import annotations

import io
import os
import re

import fitz
from docx import Document
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.1-8b-instant"


def _get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY manquante")
    return Groq(api_key=api_key)


def extract_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def extract_docx(file_bytes: bytes) -> str:
    stream = io.BytesIO(file_bytes)
    doc = Document(stream)
    return "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())


def detect_and_extract(file_bytes: bytes, content_type: str | None) -> str:
    normalized = (content_type or "").lower()

    if "pdf" in normalized:
        text = extract_pdf(file_bytes)
        if len(text.split()) < 10:
            raise ValueError("PDF probablement vide ou scanné")
        return text

    if "docx" in normalized or "word" in normalized:
        return extract_docx(file_bytes)

    return file_bytes.decode("utf-8", errors="ignore").strip()


def summarize_course(text: str) -> str:
    if not text or len(text.strip()) < 20:
        raise ValueError("Texte vide ou invalide")

    prompt = f"""
Résume ce cours de manière claire et concise.

FORMAT OBLIGATOIRE :
CONCEPTS CLÉS :
- concept : définition

POINTS IMPORTANTS :
- point

COURS :
{text[:8000]}
"""

    response = _get_client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Tu es un assistant pédagogique précis."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=700,
    )
    return response.choices[0].message.content or ""