from google import genai
from .utils import get_api_key

def summarize(transcript):
    """Generate a structured summary of the podcast transcript."""
    sys_instruct = """Summarize the podcast transcript in a structured format with:
- Podcast Details: Name, episode title, hosts, guests
- Premise: Overall theme and discussion summary
- Key Topics Discussed & Highlights: Numbered list with detailed bullet points
- Playbook Points: Strategic insights or takeaways
- Recommendations: Notable suggestions or mentions
Keep it clear, professional, and concise."""
    
    client = genai.Client(api_key=get_api_key())
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=sys_instruct + transcript)
        return response.text
    except Exception as e:
        print(f"Summary generation failed: {str(e)}")
        return "Failed to generate summary. Check API key and connection."