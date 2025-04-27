from crewai import Task
from typing import List
from models import ExpertiseLevel

class EducationTasks:
    @staticmethod
    def create_learning_material_task(agent, topics: List[str], expertise_level: ExpertiseLevel) -> Task:
        return Task(
            description=f"""Find and curate learning materials for the following topics: {topics}.
            The content should be suitable for {expertise_level.value} level.
            Include a mix of videos, articles, and practical exercises.
            Ensure all materials are from reputable sources and are current.""",
            agent=agent
        )

    @staticmethod
    def create_quiz_task(agent, topics: List[str], expertise_level: ExpertiseLevel) -> Task:
        return Task(
            description=f"""Create a comprehensive quiz for the topics: {topics}.
            The questions should be appropriate for {expertise_level.value} level.
            Include a mix of multiple choice questions.
            Each question should have an explanation for the correct answer.""",
            agent=agent
        )

    @staticmethod
    def create_project_suggestion_task(agent, topics: List[str], expertise_level: ExpertiseLevel) -> Task:
        return Task(
            description=f"""Suggest practical project ideas for the topics: {topics}.
            Projects should be suitable for {expertise_level.value} level.
            Include estimated duration, required skills, and learning outcomes.
            Projects should be engaging and reinforce key concepts.""",
            agent=agent
        ) 