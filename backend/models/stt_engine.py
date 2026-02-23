import io
import numpy as np
from faster_whisper import WhisperModel
from backend.config import STT_CONFIG

class STTEngine:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the Faster-Whisper model."""
        print(f"Loading Faster-Whisper model ({STT_CONFIG['model_size']})...")
        
        try:
            self.model = WhisperModel(
                STT_CONFIG["model_size"],
                device=STT_CONFIG["device"],
                compute_type=STT_CONFIG["compute_type"],
            )
            print("Faster-Whisper model loaded successfully")
        except Exception as e:
            print(f"Error loading STT model: {e}")
            raise
    
    def transcribe(self, audio_data: np.ndarray, sample_rate: int = 16000) -> str:
        """Transcribe audio data to text."""
        if not self.model:
            raise RuntimeError("STT model not loaded")
        
        try:
            segments, info = self.model.transcribe(audio_data, language="en")
            text = "".join([segment.text for segment in segments])
            return text.strip()
        except Exception as e:
            print(f"Error during transcription: {e}")
            raise
    
    def transcribe_file(self, file_path: str) -> str:
        """Transcribe audio from a file."""
        try:
            segments, info = self.model.transcribe(file_path, language="en")
            text = "".join([segment.text for segment in segments])
            return text.strip()
        except Exception as e:
            print(f"Error transcribing file: {e}")
            raise