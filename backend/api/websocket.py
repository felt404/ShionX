import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.memory.memory_manager import MemoryManager
from backend.models.llm_engine import LLMEngine
from backend.models.stt_engine import STTEngine

router = APIRouter()

llm_engine = None
stt_engine = None
memory_manager = MemoryManager()


def get_llm_engine() -> LLMEngine:
    global llm_engine
    if llm_engine is None:
        llm_engine = LLMEngine()
    return llm_engine


def get_stt_engine() -> STTEngine:
    global stt_engine
    if stt_engine is None:
        stt_engine = STTEngine()
    return stt_engine


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    engine = get_llm_engine()

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message.get("type") != "text":
                continue

            prompt = (message.get("payload") or "").strip()
            if not prompt:
                continue

            try:
                memory_manager.add_history("user", prompt)
                response = engine.generate(prompt)
                memory_manager.add_history("assistant", response)
                await websocket.send_json({"type": "response_chunk", "payload": response})
                await websocket.send_json(
                    {"type": "response_complete", "payload": {"status": "success"}}
                )
            except Exception as e:
                await websocket.send_json({"type": "error", "payload": str(e)})

    except WebSocketDisconnect:
        print("Client disconnected from chat")


@router.websocket("/ws/voice")
async def websocket_voice(websocket: WebSocket):
    await websocket.accept()
    stt = get_stt_engine()
    engine = get_llm_engine()

    try:
        while True:
            data = await websocket.receive_bytes()
            try:
                import numpy as np

                audio_data = np.frombuffer(data, dtype=np.float32)
                text = stt.transcribe(audio_data)
                memory_manager.add_history("user", text)

                await websocket.send_json({"type": "transcription", "text": text})

                response = engine.generate(text)
                memory_manager.add_history("assistant", response)
                await websocket.send_json({"type": "response_chunk", "payload": response})
                await websocket.send_json(
                    {"type": "response_complete", "payload": {"status": "success"}}
                )
            except Exception as e:
                await websocket.send_json({"type": "error", "payload": str(e)})

    except WebSocketDisconnect:
        print("Client disconnected from voice")
