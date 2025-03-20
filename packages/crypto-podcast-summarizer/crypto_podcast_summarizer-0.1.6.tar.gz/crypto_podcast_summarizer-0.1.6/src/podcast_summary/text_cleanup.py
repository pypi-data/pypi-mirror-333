import re

def text_cleanup(text):
    """Clean up text by replacing asterisks and formatting lines for voice synthesis."""
    text = '\n'.join(text.split('\n')[2:])  # Skip first two lines (assumed metadata)
    def repl(match):
        count = len(match.group(0))
        return "•" if count % 2 == 1 else ""
    
    processed_text = re.sub(r'\*+', repl, text)

    # Convert 'ETH' to 'eeth'
    processed_text = re.sub(r'\bETH\b', 'eeth', processed_text)

    # Format YYYY-YYYY dates to ensure proper punctuation (e.g., "2022-2023" to "2022 to 2023")
    processed_text = re.sub(r'\b(\d{4})-(\d{4})\b', r'\1 to \2', processed_text)

    lines = processed_text.split('\n')
    processed_lines = [line.strip() + '.' if line.strip() and not line.strip().endswith('.') else line.strip() for line in lines]
    return '\n'.join(processed_lines)