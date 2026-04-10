from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
import os
import uuid

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from debate import get_ai_response
from parser import detect_and_extract

app = FastAPI(title="DebateArena API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions: dict[str, dict] = {}
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))


class ChatMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str


class ChatBody(BaseModel):
    course_id: str
    mode: str = "contradicteur"
    message: str
    history: list[ChatMessage] = []


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


def _is_expired(created_at_iso: str) -> bool:
    created_at = datetime.fromisoformat(created_at_iso)
    expiry = created_at + timedelta(minutes=SESSION_TIMEOUT_MINUTES)
    return datetime.now(timezone.utc) > expiry


def _require_session(course_id: str) -> dict:
    session = sessions.get(course_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable")

    if _is_expired(session["created_at"]):
        sessions.pop(course_id, None)
        raise HTTPException(status_code=404, detail="Session expirée")

    return session


@app.post("/upload")
async def upload(file: UploadFile | None = File(default=None), text: str | None = Form(default=None)) -> dict:
    if not file and not text:
        raise HTTPException(status_code=400, detail="Aucun contenu fourni")

    title = "Texte"
    content = ""

    if text and text.strip():
        content = text.strip()

    if file:
        raw = await file.read()
        if len(raw) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(status_code=413, detail=f"Fichier trop volumineux (max {MAX_FILE_SIZE_MB} MB)")
        title = file.filename or "Cours"
        try:
            content = detect_and_extract(raw, file.content_type)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not content:
        raise HTTPException(status_code=400, detail="Contenu vide")

    course_id = str(uuid.uuid4())[:8]
    sessions[course_id] = {
        "title": title,
        "content": content,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return {"course_id": course_id, "title": title}


@app.post("/chat")
async def chat(body: ChatBody) -> dict:
    session = _require_session(body.course_id)

    if not body.message.strip():
        raise HTTPException(status_code=400, detail="Message vide")

    reply = "".join(
        get_ai_response(
            content=session["content"],
            mode=body.mode,
            history=[msg.model_dump() for msg in body.history],
            message=body.message,
        )
    )
    return {"reply": reply}


@app.post("/chat/stream")
async def chat_stream(body: ChatBody, request: Request) -> StreamingResponse:
    session = _require_session(body.course_id)

    if not body.message.strip():
        raise HTTPException(status_code=400, detail="Message vide")

    def ai_tokens():
        return get_ai_response(
            content=session["content"],
            mode=body.mode,
            history=[msg.model_dump() for msg in body.history],
            message=body.message,
        )

    async def event_stream():
        try:
            for token in ai_tokens():
                if await request.is_disconnected():
                    break
                payload = json.dumps({"token": token}, ensure_ascii=False)
                yield f"event: token\ndata: {payload}\n\n"
            yield "event: done\ndata: [DONE]\n\n"
        except Exception as exc:  # noqa: BLE001
            payload = json.dumps({"error": str(exc)}, ensure_ascii=False)
            yield f"event: error\ndata: {payload}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/session/{course_id}")
def get_session(course_id: str) -> dict:
    return _require_session(course_id)


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        raise exc
    return JSONResponse(status_code=500, content={"detail": "Erreur interne"})