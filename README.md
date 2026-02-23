# ShionX

ShionX is a local-first AI assistant scaffold with:
- FastAPI backend
- WebSocket chat + voice channels
- GGUF model management hooks
- Simple file-based memory (context/history/notes)
- Minimal browser UI

> This project currently targets **direct local Python execution** (no Docker required).

## Project Layout

```text
ShionX/
├── README.md
├── requirements.txt
├── .gitignore
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── llm_engine.py
│   │   ├── stt_engine.py
│   │   └── tts_engine.py
│   ├── memory/
│   │   └── memory_manager.py
│   └── api/
│       ├── routes.py
│       └── websocket.py
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       ├── ws.js
│       └── recorder.js
└── models/
```

## Quick Start (No Docker)

1. **Create and activate a virtualenv**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Open the UI**
   - http://127.0.0.1:8000

## Notes

- Place your `.gguf` models inside `models/`.
- If no model is loaded, generation endpoints will return a clear error.
- Memory files are persisted under `memories/`.



## Hardware Target

- The project is configured for **AMD iGPU/eGPU offloading** on the LLM path.
- Default `gpu_layers` is now `35` (set via `SHIONX_GPU_LAYERS`), so offloading is enabled out of the box.
- STT remains CPU-first by default (`faster-whisper`) unless you explicitly change `SHIONX_STT_DEVICE`.
- NVIDIA/CUDA-specific dependencies and hardcoded defaults are removed.

### Useful environment overrides

```bash
export SHIONX_GPU_LAYERS=45
export SHIONX_MODEL_TYPE=qwen
export SHIONX_MAX_TOKENS=512
export SHIONX_STT_DEVICE=cpu
export SHIONX_STT_COMPUTE_TYPE=int8
```
