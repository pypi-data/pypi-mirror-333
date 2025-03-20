import torch
import whisper
import subprocess

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: 'ffmpeg' is required but not found. Please install it:")
        print("- macOS: 'brew install ffmpeg'")
        print("- Windows: 'choco install ffmpeg'")
        print("- Linux: 'sudo apt-get install ffmpeg'")
        sys.exit(1)

def transcribe_audio(file_path):
    """Transcribe audio file using Whisper, forcing CPU for compatibility."""
    print("Transcribing audio (this may take a few minutes)...")
    device = "cpu"

    check_ffmpeg()
    
    try:
        model = whisper.load_model("base", device=device)
        result = model.transcribe(str(file_path))
        return result["text"] if "text" in result else None
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return None