from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from src.agent import get_response
import pickledb


app = FastAPI()
db = pickledb.load("data/conversations.json", auto_dump=True)


class ChatRequest(BaseModel):
    conversation_id: str | None
    message: str

def save_message(conversation_id, message):
    history = db.get(conversation_id) or []
    history.append(message)
    db.set(conversation_id, history)

def get_history(conversation_id):
    return db.get(conversation_id) or []

@app.post("/chat")
async def chat(req: ChatRequest):
    conversation_id = req.conversation_id or str(uuid.uuid4())
    history = get_history(conversation_id)
    history.append({"role": "user", "message": req.message})
    reply = await get_response(history)
    history.append({"role": "bot", "message": reply})
    for msg in history[-12:]:
        save_message(conversation_id, msg)
    return {"conversation_id": conversation_id, "message": history[-12:]}