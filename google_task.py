import os
import requests
from bs4 import BeautifulSoup

# ---------------------
# Config
# ---------------------
URL = "https://en.wikipedia.org/wiki/Artificial_intelligence"  # choose one of the 3 URLs
API_KEY = os.getenv("AIzaSyD-qxnbv8-PtDbrBmC_ffPF-JoSYZOBwfg")  # Set your Gemini API key in environment variable
MODEL_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# ---------------------
# Fetch and clean HTML
# ---------------------
html = requests.get(URL).text
soup = BeautifulSoup(html, "html.parser")
for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form", "noscript"]):
    tag.decompose()
text = soup.get_text(separator="\n")
lines = [line.strip() for line in text.splitlines() if line.strip()]
cleaned_text = "\n".join(lines[:2000])  # limit length for safety

# ---------------------
# Build custom prompt
# ---------------------
prompt = f"""
You are an expert analyst. Summarize the following webpage content into EXACTLY 5 concise bullet points 
(•) and add one single-line Insight at the end. Tone: analytical and clear.

Webpage content:
{cleaned_text}

Output format must be exactly:

Summary:
• <point 1>
• <point 2>
• <point 3>
• <point 4>
• <point 5>
Insight:
<single-line insight>
"""

# ---------------------
# Call Gemini 2.5 Flash
# ---------------------
response = requests.post(
    f"{MODEL_ENDPOINT}?key={API_KEY}",
    json={
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "maxOutputTokens": 1000
    }
)
data = response.json()
# Extract generated text
output = data.get("candidates", [{}])[0].get("content", [{}])[0].get("text", "No output")

# ---------------------
# Print and save
# ---------------------
print(output)
with open("summary_output.txt", "w", encoding="utf-8") as f:
    f.write(output)
