import os
from pathlib import Path
from ctransformers import AutoModelForCausalLM
from backend.config import MODELS_DIR, LLM_CONFIG

class LLMEngine:
    def __init__(self, model_path: str = None):
        self.current_model_path = model_path
        self.model = None
        self.model_name = None
        
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path: str):
        """Load a GGUF model from the specified path."""
        full_path = MODELS_DIR / model_path if not os.path.isabs(model_path) else model_path
        
        if not full_path.exists():
            raise FileNotFoundError(f"Model not found at {full_path}")
        
        print(f"Loading model from {full_path}...")
        
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                str(full_path),
                model_type=LLM_CONFIG["model_type"],
                gpu_layers=LLM_CONFIG["gpu_layers"],
            )
            self.current_model_path = str(full_path)
            self.model_name = full_path.stem
            print(f"Model loaded successfully: {self.model_name}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def swap_model(self, new_model_path: str):
        """Unload current model and load a new one."""
        if self.model:
            del self.model
        self.load_model(new_model_path)
    
    def generate(self, prompt: str, max_tokens: int = None) -> str:
        """Generate text from a prompt."""
        if not self.model:
            raise RuntimeError("No model loaded")
        
        tokens = max_tokens or LLM_CONFIG["max_tokens"]
        response = self.model(
            prompt,
            max_new_tokens=tokens,
            temperature=LLM_CONFIG["temperature"],
        )
        return response
    
    def list_available_models(self):
        """List all available GGUF models in the models directory."""
        models = list(MODELS_DIR.glob("*.gguf"))
        return [m.name for m in models]
    
    def get_current_model(self):
        """Get the name of the currently loaded model."""
        return self.model_name