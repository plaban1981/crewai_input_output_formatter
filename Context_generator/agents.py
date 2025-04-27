from crewai import Agent, Task,Process,LLM
from typing import List
import os
from models import LearningMaterial, Quiz, ProjectIdea, ExpertiseLevel
from crewai_tools import SerperDevTool
#
from dotenv import load_dotenv
load_dotenv()
llm = LLM('ollama/llama3.2',
          temperature=0.7)




class EducationAgents:
    
        
    def learning_material_agent(self) -> Agent:
        return Agent(
             role='Learning Material Curator',
            goal='Curate high-quality learning materials based on user topics and expertise level',
            backstory="""You are an expert educational content curator with years of experience
            in finding the best learning resources for students at different levels. You know how
            to identify reliable and high-quality educational content from reputable sources.""",
            llm=llm,
            verbose=True
        )

    def quiz_creator_agent(self) -> Agent:
        return Agent(
            role='Quiz Creator',
            goal='Create engaging and educational quizzes to test understanding',
            backstory="""You are an experienced educator who specializes in creating
            effective assessment questions that test understanding while promoting learning.""",
            llm=llm,
            verbose=True
        )

    def project_suggestion_agent(self) -> Agent:
        return Agent(
           role='Project Advisor',
            goal='Suggest practical projects that match user expertise and interests',
            backstory="""You are a project-based learning expert who knows how to create
            engaging hands-on projects that reinforce learning objectives.""",
            llm=llm,
            verbose=True
        ) 