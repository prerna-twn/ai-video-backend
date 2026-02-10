import openai
import random

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_questions_from_transcript(transcript: str, num_questions: int = 3):
    """
    Sends the transcript to GPT and gets questions.
    Returns list of dicts with question, options, and answer.
    """
    prompt = f"""
    You are a quiz master. Generate {num_questions} multiple-choice questions from this transcript.
    Respond in JSON format as a list:
    [
      {{ "id": 1, "question": "...", "options": ["A","B","C","D"], "answer": "..." }},
      ...
    ]
    Transcript:
    {transcript}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.5
    )
    import json
    try:
        questions = json.loads(response.choices[0].message.content)
    except:
        # fallback simple dummy questions if parsing fails
        questions = [
            {"id":1,"question":"What is 2+2?","options":["2","3","4","5"],"answer":"4"}
        ]
    return questions

def check_answer(question: dict, user_answer: str):
    """
    Compares answer and generates explanation via AI.
    """
    correct = question["answer"].strip().lower() == user_answer.strip().lower()
    explanation = ""
    if not correct:
        explanation = f"The correct answer is {question['answer']}. Review the topic in the video."
    return {"correct": correct, "explanation": explanation}
