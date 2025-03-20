from pathlib import Path
import re
import os

def get_podcast_summary_folder(podcast_title=None):
    """Return the path to podcast-summary folder or a podcast-specific subfolder."""
    downloads_dir = Path.home() / "Downloads"
    base_folder = downloads_dir / "podcast-summary"
    base_folder.mkdir(exist_ok=True)
    
    if podcast_title:
        safe_title = re.sub(r'[^\w\s-]', '', podcast_title).replace(" ", "_")
        podcast_folder = base_folder / safe_title
        podcast_folder.mkdir(exist_ok=True)
        return podcast_folder
    return base_folder

def get_api_key():
    """Retrieve or prompt for GenAI API key and store it in a file."""
    api_key_file = "api_key.txt"
    if os.path.exists(api_key_file):
        with open(api_key_file, "r") as f:
            api_key = f.read().strip()
        if api_key:
            return api_key
    key = input("Enter your Google GenAI API key: ").strip()
    with open(api_key_file, "w") as f:
        f.write(key)
    return key