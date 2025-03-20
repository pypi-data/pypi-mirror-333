import feedparser
import os
import re
import csv
import warnings
from .download import download_episode
from .transcribe import transcribe_audio
from .summarize import summarize
from .text_cleanup import text_cleanup
from .voice import generate_voice_summary, KOKORO_AVAILABLE
from .utils import get_podcast_summary_folder, get_api_key

warnings.filterwarnings("ignore")

def load_podcasts():
    """Load podcasts from CSV file, create with defaults if missing."""
    podcasts = {}
    filename = "podcasts.csv"
    
    if os.path.exists(filename):
        try:
            with open(filename, 'r', newline='') as f:
                reader = csv.DictReader(f)
                if 'title' not in reader.fieldnames or 'url' not in reader.fieldnames:
                    print(f"Error: {filename} is malformed, missing required headers 'title' or 'url'")
                else:
                    for i, row in enumerate(reader, 1):
                        podcasts[i] = {"title": row['title'], "url": row['url']}
                    print(f"Loaded {len(podcasts)} podcasts from {filename}")
        except Exception as e:
            print(f"Error reading {filename}: {str(e)}")
    
    if not podcasts:
        print(f"No valid podcasts found, creating default {filename}")
        default_podcasts = [
            {"title": "Unchained", "url": "https://feeds.megaphone.fm/LSHML4761942757"},
            {"title": "Lightspeed", "url": "https://feeds.megaphone.fm/lightspeed"},
            {"title": "Bankless", "url": "https://bankless.libsyn.com/rss"},
            {"title": "Bell Curve", "url": "https://feeds.megaphone.fm/bellcurve"},
            {"title": "Expansion", "url": "https://feeds.megaphone.fm/expansion"},
        ]
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['title', 'url'])
                writer.writeheader()
                writer.writerows(default_podcasts)
            print(f"Created {filename} with {len(default_podcasts)} default podcasts")
            with open(filename, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader, 1):
                    podcasts[i] = {"title": row['title'], "url": row['url']}
        except Exception as e:
            print(f"Error creating {filename}: {str(e)}")
            return podcasts
    
    return podcasts

def save_podcasts(podcasts):
    """Save podcasts to CSV file."""
    with open("podcasts.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows([{"title": p["title"], "url": p["url"]} for p in podcasts.values()])

def process_episode(episode, idx, podcast_title):
    """Process a single episode and return if it was successful."""
    safe_title = re.sub(r'[^\w\s-]', '', episode.title)[:100].replace(" ", "_")
    audio_file = f"{safe_title}.mp3"
    podcast_folder = get_podcast_summary_folder(podcast_title)
    audio_path = podcast_folder / audio_file
    
    if download_episode(episode, audio_file, podcast_title=podcast_title):
        try:
            if not audio_path.exists():
                print(f"Error: Audio file {audio_path} not found before transcription.")
                return False
            #print(f"File confirmed at: {audio_path}")
            transcript = transcribe_audio(audio_path)
            if transcript is None:
                print(f"Skipping episode {idx + 1} due to transcription failure.")
                return False
            summary = summarize(transcript)
            print(f"\nSummary for episode {idx + 1} generated\n")
            if KOKORO_AVAILABLE:
                summary_audio = podcast_folder / f"{safe_title}_summary.mp3"
                cleaned_summary = text_cleanup(summary)
                generate_voice_summary(cleaned_summary, summary_audio)
            return True
        finally:
            if audio_path.exists():
                audio_path.unlink()
                print(f"Cleaning up: {audio_path} deleted.")
            else:
                print(f"Cleanup skipped: {audio_path} not found.")
    return False

def list_podcast_episodes():
    """List podcasts and episodes, handle selection and processing."""
    podcasts = load_podcasts()
    
    while True:
        print("\nAvailable Podcasts:")
        if not podcasts:
            print("No podcasts found in podcasts.csv")
        else:
            print(f"Found {len(podcasts)} podcasts:")
            for num, podcast in podcasts.items():
                print(f"{num}. {podcast['title']}")
        print("\nOptions: [number] to select, [number]r to remove, n for new, q to quit")
        
        choice = input("Select an option: ").strip().lower()
        if choice == 'q':
            return
        
        if choice.endswith('r'):
            try:
                num = int(choice[:-1])
                if num in podcasts:
                    del podcasts[num]
                    podcasts = {i+1: v for i, v in enumerate(podcasts.values())}
                    save_podcasts(podcasts)
                    print(f"Removed podcast {num}")
                else:
                    print("Invalid podcast number")
                continue
            except ValueError:
                print("Invalid input")
                continue
                
        elif choice == 'n':
            title = input("Enter podcast title: ").strip()
            url = input("Enter podcast RSS URL: ").strip()
            if title and url:
                new_id = max(podcasts.keys()) + 1 if podcasts else 1
                podcasts[new_id] = {"title": title}
                save_podcasts(podcasts)
                print(f"Added new podcast: {title}")
            continue
            
        try:
            podcast = podcasts.get(int(choice))
            if not podcast:
                print("Invalid selection.")
                continue
            
            feed = feedparser.parse(podcast["url"])
            if not feed.entries:
                print(f"No episodes found for {podcast['title']} at {podcast['url']}.")
                continue
            
            page_size, total = 5, len(feed.entries)
            page_start = 0

            while True:
                page_end = min(page_start + page_size, total)
                print(f"\nEpisodes {page_start + 1} to {page_end} of {total}:")
                for i in range(page_start, page_end):
                    print(f"\n[{i+1}] {feed.entries[i].title}") 
                    print(f"Published: {feed.entries[i].published}")
                
                action = input("\nEnter episode number, 'a' (all), 'b' (back), 'n' (next), 'p' (prev), or 'q' (quit): ").strip().lower()
                if action == 'q':
                    break
                elif action == 'b':
                    break
                elif action == 'n':
                    page_start = page_start + page_size if page_end < total else page_start
                elif action == 'p':
                    page_start = max(page_start - page_size, 0)
                elif action == 'a':
                    for i in range(page_start, page_end):
                        print(f"\nProcessing episode {i+1}...")
                        process_episode(feed.entries[i], i, podcast['title'])
                else:
                    try:
                        idx = int(action) - 1
                        if 0 <= idx < total:
                            print(f"\nProcessing episode {idx+1}...")
                            process_episode(feed.entries[idx], idx, podcast['title'])
                        else:
                            print("Invalid episode number.")
                    except ValueError:
                        print("Invalid input.")
        except ValueError:
            print("Enter a valid option.")

def main():
    """Main entry point for the Podcast Summarizer."""
    print("Crypto Podcast Summarizer\n======================")
    try:
        get_api_key()
        list_podcast_episodes()
    except KeyboardInterrupt:
        print("\nTerminated by user.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
    finally:
        print("\nThank you for using the Crypto Podcast Summarizer!")
        print("If you have any questions or ideas for improving this project, feel free to reach out at ayarlagadda59@gmail.com.\n")