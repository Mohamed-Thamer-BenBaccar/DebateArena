"""Logique IA pour DebateArena."""

from __future__ import annotations

import os
from typing import Generator

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

PROMPTS = {
    "contradicteur": """Tu es un adversaire intellectuel.
Contexte du cours : {content}
Contredis chaque affirmation. Cherche les failles.
Ne donne JAMAIS la réponse. Pose UNE question à la fin.""",
    "socrate": """Tu es Socrate. Cours : {content}
Réponds UNIQUEMENT par une question.""",
    "jury": """Tu es un jury. Cours : {content}
Format réponse : [NOTE: X/10] justification. Question suivante.""",
}


def _get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY manquante")
    return Groq(api_key=api_key)


def get_ai_response(
    content: str,
    mode: str,
    history: list[dict[str, str]],
    message: str,
) -> Generator[str, None, None]:
    """Retourne les tokens Groq en streaming."""
    selected_mode = mode if mode in PROMPTS else "contradicteur"
    system_prompt = PROMPTS[selected_mode].format(content=content[:3000])

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history or [])
    messages.append({"role": "user", "content": message})

    stream = _get_client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        stream=True,
        max_tokens=300,
        temperature=0.7,
    )

    for chunk in stream:
        token = chunk.choices[0].delta.content
        if token:
            yield token