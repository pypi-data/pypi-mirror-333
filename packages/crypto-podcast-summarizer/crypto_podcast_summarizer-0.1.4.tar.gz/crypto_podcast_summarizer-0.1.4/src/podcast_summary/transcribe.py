import torch
import whisper

def transcribe_audio(file_path):
    """Transcribe audio file using Whisper, forcing CPU for compatibility."""
    print("Transcribing audio (this may take a few minutes)...")
    device = "cpu"
    #print("Using CPU for reliable transcription...")
    
    try:
        model = whisper.load_model("base", device=device)
        result = model.transcribe(str(file_path))
        return result["text"]
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return None