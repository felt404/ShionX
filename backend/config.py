import os
from pathlib import Path


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


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
    "model_type": os.getenv("SHIONX_MODEL_TYPE", "qwen"),
    # AMD iGPU/eGPU offload target: use GPU layers by default.
    # Tune per model VRAM budget via env var if needed.
    "gpu_layers": _env_int("SHIONX_GPU_LAYERS", 35),
    "temperature": float(os.getenv("SHIONX_TEMPERATURE", "0.7")),
    "max_tokens": _env_int("SHIONX_MAX_TOKENS", 512),
}

# STT configuration
STT_CONFIG = {
    "model_size": os.getenv("SHIONX_STT_MODEL_SIZE", "base"),
    # Faster-Whisper is typically CPU/CUDA based in common installs.
    # Keep STT CPU by default while LLM offload is enabled separately.
    "device": os.getenv("SHIONX_STT_DEVICE", "cpu"),
    "compute_type": os.getenv("SHIONX_STT_COMPUTE_TYPE", "int8"),
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
