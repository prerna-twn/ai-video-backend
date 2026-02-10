from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os, json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TRANSCRIPT_FILE = "transcript/video1.txt"

def read_transcript():
    with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/quiz")
async def quiz():
    transcript = read_transcript()

    prompt = f"""
Generate ONE multiple-choice question from the transcript below.

Rules:
- Pick a random concept
- 4 options
- Only one correct answer
- Return ONLY valid JSON

JSON format:
{{
  "question": "",
  "options": ["", "", "", ""],
  "correct_answer": "",
  "explanation": ""
}}

Transcript:
{transcript}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    return json.loads(response.choices[0].message.content)
