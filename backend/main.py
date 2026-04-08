from fastapi import FastAPI, UploadFile, Form, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uuid
import time

app = FastAPI(title="DebateArena API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

# -------------------------
# ROUTES DE BASE
# -------------------------

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------
# UPLOAD
# -------------------------

@app.post("/upload")
async def upload(file: UploadFile = File(None), text: str = Form(None)):
    cid = str(uuid.uuid4())[:8]

    if not file and not text:
        raise HTTPException(status_code=400, detail="Aucun contenu fourni")

    content = text or "Cours mock"

    if file:
        file_bytes = await file.read()
        content = file_bytes.decode("utf-8", errors="ignore")

    sessions[cid] = {
        "content": content,
        "title": file.filename if file else "Texte"
    }

    return {
        "course_id": cid,
        "title": sessions[cid]["title"]
    }


# -------------------------
# CHAT NORMAL (mock)
# -------------------------

@app.post("/chat")
async def chat(body: dict):
    cid = body.get("course_id")

    if cid not in sessions:
        raise HTTPException(status_code=404, detail="Session introuvable")

    mode = body.get("mode", "contradicteur")
    msg = body.get("message", "")

    responses = {
        "contradicteur": f"Je ne suis pas d'accord avec '{msg[:30]}'. Pourquoi ?",
        "socrate": "Pourquoi pensez-vous cela ?",
        "jury": "[NOTE: 7/10] Réponse correcte. Question suivante ?"
    }

    return {"reply": responses.get(mode, "Réponse mock")}


# -------------------------
# 🔥 STREAMING (NOUVEAU)
# -------------------------

@app.post("/chat/stream")
async def chat_stream(body: dict):
    cid = body.get("course_id")

    if cid not in sessions:
        raise HTTPException(status_code=404, detail="Session introuvable")

    mode = body.get("mode", "contradicteur")
    msg = body.get("message", "")

    # réponse simulée selon le mode
    if mode == "contradicteur":
        text = f"Je ne suis pas d'accord avec '{msg}'. Pouvez-vous expliquer votre raisonnement ?"
    elif mode == "socrate":
        text = "Pourquoi pensez-vous cela ? Pouvez-vous approfondir votre réponse ?"
    else:
        text = "[NOTE: 7/10] Bonne réponse. Pouvez-vous être plus précis ?"

    # fonction générateur (stream token par token)
    def generate():
        try:
            words = text.split(" ")
            for word in words:
                yield word + " "
                time.sleep(0.1)  # effet streaming (vitesse)
        except Exception:
            yield "[ERREUR] Service indisponible."

    return StreamingResponse(generate(), media_type="text/plain")


# -------------------------
# SESSION
# -------------------------

@app.get("/session/{course_id}")
def get_session(course_id: str):
    if course_id not in sessions:
        raise HTTPException(status_code=404, detail="Session introuvable")

    return sessions[course_id]