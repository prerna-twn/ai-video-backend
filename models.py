from pydantic import BaseModel
from typing import List, Optional

class Question(BaseModel):
    id: int
    question: str
    options: List[str]
    answer: str  # correct answer, optional to hide for frontend

class AnswerSubmission(BaseModel):
    question_id: int
    answer: str

class SessionResponse(BaseModel):
    session_id: str
    questions: List[Question]

class AnswerResponse(BaseModel):
    correct: bool
    explanation: Optional[str] = None
