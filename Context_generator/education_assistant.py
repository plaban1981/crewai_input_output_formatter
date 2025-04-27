from crewai import Crew
from typing import List
from models import ExpertiseLevel, LearningMaterial, Quiz, ProjectIdea
from agents import EducationAgents
from tasks import EducationTasks

class EducationAssistant:
    def __init__(self):
        self.agents = EducationAgents()
        
    def generate_personalized_content(
        self,
        topics: List[str],
        expertise_level: ExpertiseLevel
    ):
        # Create agents
        learning_material_agent = self.agents.learning_material_agent()
        quiz_creator_agent = self.agents.quiz_creator_agent()
        project_suggestion_agent = self.agents.project_suggestion_agent()
        
        # Create tasks
        tasks = [
            EducationTasks.create_learning_material_task(
                learning_material_agent, topics, expertise_level
            ),
            EducationTasks.create_quiz_task(
                quiz_creator_agent, topics, expertise_level
            ),
            EducationTasks.create_project_suggestion_task(
                project_suggestion_agent, topics, expertise_level
            )
        ]
        
        # Create and run the crew
        crew = Crew(
            agents=[learning_material_agent, quiz_creator_agent, project_suggestion_agent],
            tasks=tasks
        )
        
        result = crew.kickoff()
        return result

# Example usage
if __name__ == "__main__":
    assistant = EducationAssistant()
    topics = ["Python Programming", "Data Structures"]
    result = assistant.generate_personalized_content(
        topics=topics,
        expertise_level=ExpertiseLevel.INTERMEDIATE
    )
    print(result) 