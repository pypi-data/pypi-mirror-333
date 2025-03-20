# Crypto Podcast Summarizer

A Python tool to download podcast episodes, transcribe them, generate summaries, and optionally create voice summaries, tailored for crypto-related content.

## Prerequisites

This tool requires ffmpeg for audio processing. Please install it based on your operating system:

**macOS:**

```bash
brew install ffmpeg
```

**Windows**

```bash
choco install ffmpeg
```

**Linux**

```bash
sudo apt-get install ffmpeg
```

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

1. **Visit [Google AI Studio](https://aistudio.google.com/apikey).**
2. Click **Get API Key**.
3. Select an existing Google project or create a new one.
4. Enable the Generative AI API if prompted.
5. Copy your newly generated API key and paste it when prompted.

### Providing the API Key

When you run the tool (e.g., `crypto-podcast-summarizer`) for the first time, you will be prompted to enter your Google GenAI API key. The key will then be saved to `api_key.txt` in the current directory for future use.

#### Alternative Method

If you prefer not to be prompted, you can:
1. Create a file named `api_key.txt` in the same directory as the tool.
2. Paste your API key into this file before running the tool.



