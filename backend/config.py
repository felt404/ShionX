import os
from pathlib import Path

# Cross-platform path handling
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"
MEMORIES_DIR = BASE_DIR / "memories"
FRONTEND_DIR = BASE_DIR / "frontend"

# Ensure directories exist
MODELS_DIR.mkdir(exist_ok=True)
MEMORIES_DIR.mkdir(exist_ok=True)
(MEMORIES_DIR / "context").mkdir(exist_ok=True)
(MEMORIES_DIR / "history").mkdir(exist_ok=True)
(MEMORIES_DIR / "notes").mkdir(exist_ok=True)

# Model configuration
LLM_CONFIG = {
    "model_type": "qwen",
    "gpu_layers": 10,  # Adjust based on your iGPU
    "temperature": 0.7,
    "max_tokens": 512,
}

# STT configuration
STT_CONFIG = {
    "model_size": "base",  # tiny, base, small, medium, large
    "device": "cuda",  # cuda or cpu
    "compute_type": "float16",
}

# TTS configuration
TTS_CONFIG = {
    "model_name": "sovits",
    "sample_rate": 22050,
}

# API configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "ws_timeout": 60,
}