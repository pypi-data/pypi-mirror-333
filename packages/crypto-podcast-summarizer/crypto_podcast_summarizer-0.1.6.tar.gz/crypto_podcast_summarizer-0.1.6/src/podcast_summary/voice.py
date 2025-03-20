import numpy as np
import soundfile as sf
try:
    from kokoro import KPipeline
    from IPython.display import display, Audio
    KOKORO_AVAILABLE = True
except ImportError:
    KOKORO_AVAILABLE = False

def generate_voice_summary(text, output_filename="combined.wav"):
    """Generate an audio summary using KPipeline, forcing CPU."""
    if not KOKORO_AVAILABLE:
        print("Kokoro library not available. Voice summary skipped.")
        return
    
    print("Generating voice summary...")
    device = "cpu"
    try:
        pipeline = KPipeline(lang_code='a', device=device, repo_id='hexgrad/Kokoro-82M')
        audio_segments = [audio for _, _, audio in pipeline(text, voice='af_heart', speed=0.9, split_pattern=None)]
        combined_audio = np.concatenate(audio_segments)
        sf.write(str(output_filename), combined_audio, 24000)
        print(f"Voice summary saved as {output_filename}")
        '''try:
            display(Audio(data=combined_audio, rate=24000, autoplay=True))
        except:
            print("Audio display not available in this environment.")'''
    except Exception as e:
        print(f"Voice summary generation failed: {str(e)}")