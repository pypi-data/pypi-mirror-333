import requests
from pathlib import Path
from .utils import get_podcast_summary_folder 

def download_episode(episode, filename="episode.mp3", podcast_title=None):
    """Download podcast episode audio to a podcast-specific subfolder."""
    podcast_folder = get_podcast_summary_folder(podcast_title)
    file_path = podcast_folder / filename

    audio_url = next((link.href for link in episode.links if link.rel == "enclosure"), None)
    if not audio_url:
        print("No audio URL found for this episode.")
        return False

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/90.0.4430.212"
    }
    if file_path.exists():
        print(f"File {file_path} already exists. Skipping download.")
        return True

    response = requests.get(audio_url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        if file_path.exists():
            print(f"Downloaded: {file_path} ({file_path.stat().st_size/1e6:.1f} MB)")
            return True
        else:
            print(f"Error: File {file_path} not found after download attempt.")
            return False
    print(f"Failed to download: HTTP {response.status_code}")
    return False