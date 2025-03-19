# Crypto Podcast Summarizer

A Python tool to download podcast episodes, transcribe them, generate summaries, and optionally create voice summaries, tailored for crypto-related content.

## Installation
```
pip install crypto-podcast-summarizer
```

## Usage
```bash
crypto-podcast-summarizer
```

## Google API Key Setup

This tool uses the Google GenAI API for generating summaries. You must provide an API key to enable this functionality.

### Obtaining a Google GenAI API Key

1. **Visit[Google AI Studio](https://aistudio.google.com/apikey).**
2. Click **Get API Key**.
3. Select an existing Google project or create a new one.
4. Enable the Generative AI API if prompted.
5. Copy your newly generated API key.

### Providing the API Key

When you run the tool (e.g., `podcast-summarizer`) for the first time, you will be prompted to enter your Google GenAI API key. The key will then be saved to `api_key.txt` in the current directory for future use.

#### Alternative Method

If you prefer not to be prompted, you can:
1. Create a file named `api_key.txt` in the same directory as the tool.
2. Paste your API key into this file before running the tool.



