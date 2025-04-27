from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ExpertiseLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class LearningMaterial(BaseModel):
    title: str
    url: str
    type: str  # video, article, or exercise
    description: str

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

class Quiz(BaseModel):
    topic: str
    questions: List[QuizQuestion]

class ProjectIdea(BaseModel):
    title: str
    description: str
    difficulty: ExpertiseLevel
    estimated_duration: str
    required_skills: List[str]
    learning_outcomes: List[str] 