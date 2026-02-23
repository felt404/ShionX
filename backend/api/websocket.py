from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.models.llm_engine import LLMEngine
from backend.models.stt_engine import STTEngine
from backend.memory.memory_manager import MemoryManager
import json

router = APIRouter()

# Global instances
llm_engine = None
stt_engine = None
memory_manager = MemoryManager()

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    '''WebSocket endpoint for text chat with streaming responses.'''  
    global llm_engine  
    
    await websocket.accept()  
    
    if not llm_engine:
        llm_engine = LLMEngine()  
    
    try:
        while True:
            data = await websocket.receive_text()  
            message = json.loads(data)  
            
            if message.get("type") == "text":
                prompt = message.get("payload", "")  
                
                try:
                    # Generate response
                    response = llm_engine.generate(prompt)  
                    
                    # Send response in chunks for streaming effect
                    await websocket.send_json({
                        "type": "response_chunk",
                        "payload": response
                    })  
                    
                    # Signal completion
                    await websocket.send_json({
                        "type": "response_complete",
                        "payload": {"status": "success"}
                    })
                except Exception as e:
                    await websocket.send_json({
                        "type": "error",
                        "payload": str(e)
                    })
    
    except WebSocketDisconnect:
        print("Client disconnected from chat")

@router.websocket("/ws/voice")
async def websocket_voice(websocket: WebSocket):
    '''WebSocket endpoint for voice input/output with streaming.'''  
    global stt_engine, llm_engine  
    
    await websocket.accept()  
    
    if not stt_engine:
        stt_engine = STTEngine()
    if not llm_engine:
        llm_engine = LLMEngine()  
    
    try:
        while True:
            data = await websocket.receive_bytes()  
            
            try:
                # Transcribe audio
                import numpy as np
                audio_data = np.frombuffer(data, dtype=np.float32)
                text = stt_engine.transcribe(audio_data)  
                
                # Send transcription
                await websocket.send_json({
                    "type": "transcription",
                    "text": text
                })  
                
                # Generate response
                response = llm_engine.generate(text)  
                
                # Send response
                await websocket.send_json({
                    "type": "response_chunk",
                    "payload": response
                })  
                
                # Signal completion
                await websocket.send_json({
                    "type": "response_complete",
                    "payload": {"status": "success"}
                })
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "payload": str(e)
                })  
    
    except WebSocketDisconnect:
        print("Client disconnected from voice")