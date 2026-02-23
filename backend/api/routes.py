from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.memory.memory_manager import MemoryManager
from backend.models.llm_engine import LLMEngine

router = APIRouter(prefix="/api", tags=["api"])

llm_engine = None
memory_manager = MemoryManager()


class ModelSwapRequest(BaseModel):
    model_path: str


class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 512


class NoteRequest(BaseModel):
    note: str


def get_llm_engine() -> LLMEngine:
    global llm_engine
    if llm_engine is None:
        llm_engine = LLMEngine()
    return llm_engine


@router.get("/models")
async def list_models():
    engine = get_llm_engine()
    try:
        return {
            "available_models": engine.list_available_models(),
            "current_model": engine.get_current_model(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/models/swap")
async def swap_model(request: ModelSwapRequest):
    engine = get_llm_engine()
    try:
        engine.swap_model(request.model_path)
        return {"status": "success", "model": engine.get_current_model()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/generate")
async def generate_text(request: GenerateRequest):
    engine = get_llm_engine()
    try:
        memory_manager.add_history("user", request.prompt)
        response = engine.generate(request.prompt, request.max_tokens)
        memory_manager.add_history("assistant", response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/memories")
async def get_memories(query: str | None = None, limit: int = 10):
    try:
        if query == "context":
            return memory_manager.load_context()
        if query == "history":
            return {"history": memory_manager.get_history(limit)}
        if query == "notes":
            return {"notes": memory_manager.get_notes()}
        return {"message": "Specify query: context, history, or notes"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/notes")
async def add_note(request: NoteRequest):
    try:
        memory_manager.append_note(request.note)
        return {"status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
