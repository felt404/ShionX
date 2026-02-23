from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.models.llm_engine import LLMEngine
from backend.memory.memory_manager import MemoryManager

router = APIRouter(prefix="/api", tags=["api"])

# Global instances
llm_engine = None
memory_manager = MemoryManager()

class ModelSwapRequest(BaseModel):
    model_path: str

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 512

class MemoryQuery(BaseModel):
    query: str = None
    limit: int = 10

@router.get("/models")
async def list_models():
    """List available GGUF models."""
    global llm_engine
    if not llm_engine:
        llm_engine = LLMEngine()
    
    try:
        models = llm_engine.list_available_models()
        current = llm_engine.get_current_model()
        return {"available_models": models, "current_model": current}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/swap")
async def swap_model(request: ModelSwapRequest):
    """Swap to a different GGUF model."""
    global llm_engine
    if not llm_engine:
        llm_engine = LLMEngine()
    
    try:
        llm_engine.swap_model(request.model_path)
        return {"status": "success", "model": llm_engine.get_current_model()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate")
async def generate_text(request: GenerateRequest):
    """Generate text from a prompt."""
    global llm_engine
    if not llm_engine:
        llm_engine = LLMEngine()
    
    try:
        response = llm_engine.generate(request.prompt, request.max_tokens)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memories")
async def get_memories(query: str = None, limit: int = 10):
    """Get memories from context, history, or notes."""
    try:
        if query == "context":
            context = memory_manager.load_context()
            return context
        elif query == "history":
            history = memory_manager.get_history(limit)
            return {"history": history}
        elif query == "notes":
            notes = memory_manager.get_notes()
            return {"notes": notes}
        else:
            return {"message": "Specify query: context, history, or notes"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))