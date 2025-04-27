import streamlit as st
from crewai import Agent, Crew, Task, Process, LLM
from typing import List
import os
from models import LearningMaterial, Quiz, ProjectIdea, ExpertiseLevel
from agents import EducationAgents
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
# Load environment variables
load_dotenv()
from pydantic import BaseModel,Field
from typing import List, Optional,Dict
from enum import Enum
import json

class ExpertiseLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

# ====== Fixed Learning Material Model ======
class LearningMaterial(BaseModel):
    title: str
    url: str
    type: str=Field(...,description="video, article, or exercise")
    description: str

class MaterialCollection(BaseModel):  # Renamed for clarity
    materials: List[LearningMaterial]

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

class QuizFormat(BaseModel):
    questions: List[QuizQuestion]


class Quiz(BaseModel):
    topic: str
    questions: List[QuizQuestion]
    
# Fix Quiz model structure
class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: int  # Index of correct option (0-based)
    explanation: str

class Quiz(BaseModel):  # Renamed from QuizFormat
    questions: List[QuizQuestion]

# Corrected ProjectIdea model (represents a SINGLE project)
class ProjectIdea(BaseModel):
    title: str
    description: str
    difficulty: ExpertiseLevel
    estimated_duration: str = Field(..., description="Duration estimation in days")
    required_skills: List[str]
    learning_outcomes: List[str]

# Container for multiple projects
class Projects(BaseModel):
    projects: List[ProjectIdea]

# Initialize LLM and search tool
llm = LLM('ollama/llama3.2', temperature=0.7)
search_tool = SerperDevTool(serper_api_key=os.getenv("SERPER_API_KEY"))



def main():
    st.title("Educational Content Generator")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Configuration")
        topics = st.text_area("Enter topics (one per line)", 
                            help="Enter the topics you want to learn about")
        
        expertise_level = st.selectbox(
            "Select your expertise level",
            options=[level.value for level in ExpertiseLevel],
            help="Choose your current level of expertise"
        )

    # Main content area
    if st.button("Generate Content"):
        if not topics:
            st.error("Please enter at least one topic")
            return

        topic_list = [topic.strip() for topic in topics.split('\n') if topic.strip()]
        
        with st.spinner("Generating personalized content..."):
            try:

                learning_material_agent = Agent(
                    role='Learning Material Curator',
                    goal='Curate high-quality learning materials based on user topics and expertise level',
                    backstory="""You are an expert educational content curator with years of experience
                    in finding the best learning resources for students at different levels. You know how
                    to identify reliable and high-quality educational content from reputable sources.""",
                    llm=llm,
                    verbose=True
                )

                quiz_creator_agent = Agent(
                    role='Quiz Creator',
                    goal='Create engaging and educational quizzes to test understanding',
                    backstory="""You are an experienced educator who specializes in creating
                    effective assessment questions that test understanding while promoting learning.""",
                    llm=llm,
                    verbose=True
                )

                project_suggestion_agent = Agent(
                    role='Project Advisor',
                    goal='Suggest practical projects that match user expertise and interests',
                    backstory="""You are a project-based learning expert who knows how to create
                    engaging hands-on projects that reinforce learning objectives.""",
                    llm=llm,
                    verbose=True
                )
                #
                create_learning_material_task = Task(
                description=f"""{topics}.
                Explain {topics} to a {expertise_level} level.
                Include a mix of videos, articles, and practical exercises.
                Ensure all materials are from reputable sources and are current.
                Include GitHub repos for practical exercises. Verify source credibility before including.
                Format response as: {{
                    "materials": [
                        {{
                            "title": "...",
                            "url": "...",
                            "type": "...",
                            "description": "..."
                        }}
                    ]
                }}""",
                agent=learning_material_agent,
                expected_output=MaterialCollection.schema_json()
                )

                create_quiz_task = Task(
                    description=f"Create a comprehensive quiz for {topics} at {expertise_level} level.",
                    agent=quiz_creator_agent,
                    expected_output=Quiz.schema_json(),
                    output_pydantic=Quiz
                )

                create_project_suggestion_task = Task(
                    description=f"""Suggest ONLY 5 BEST practical project ideas for {topics}.
                    Projects should be suitable for {expertise_level} level.
                    Include title, description, difficulty, estimated duration, required skills, and learning outcomes.
                    Suggest projects that have recent community activity (check GitHub).
                    Include links to relevant documentation.
                    Projects should be engaging and reinforce key concepts.""",
                    agent=project_suggestion_agent,
                    expected_output=Projects.schema_json(),
                    output_pydantic=Projects
                )

                # Create and run crew
                crew = Crew(
                    agents=[learning_material_agent, quiz_creator_agent,project_suggestion_agent],
                    tasks=[create_learning_material_task, create_quiz_task, create_project_suggestion_task],
                    process=Process.sequential
                )
                result = crew.kickoff({"topics":topic_list,"expertise_level":ExpertiseLevel(expertise_level)})
               
                

                # Display results in tabs
                tab1, tab2, tab3 = st.tabs(["Learning Materials", "Quiz", "Project Ideas"])
                
                with tab1:
                    st.header("Curated Learning Materials")
                    materials = create_learning_material_task.output.raw
                    
                    try:
                        # Parse the raw JSON string into a Python dictionary
                        materials_json = json.loads(materials)
                        if 'materials' in materials_json:
                            for material in materials_json['materials']:
                                with st.container():
                                    st.subheader(material['title'])
                                    col1, col2 = st.columns([1, 3])
                                    with col1:
                                        st.write("**Type:**")
                                        st.write("**URL:**")
                                        st.write("**Description:**")
                                    with col2:
                                        st.write(material['type'].capitalize())
                                        st.markdown(f"[Link]({material['url']})")
                                        st.write(material['description'])
                                    st.divider()
                    except json.JSONDecodeError as e:
                        st.error("Error parsing learning materials")
                        st.write(materials)  # Fallback to display raw output
                
                with tab2:
                    st.header("Knowledge Quiz")
                    quiz = create_quiz_task.output.raw
                   
                    try:
                        quiz_json = json.loads(quiz)
                        if 'questions' in quiz_json:
                            for i, question in enumerate(quiz_json['questions'], 1):
                                with st.container():
                                    st.subheader(f"Question {i}")
                                    st.write(question['question'])
                                    
                                    # Display options in a cleaner format
                                    for j, option in enumerate(question['options'], 1):
                                        if j == question['correct_answer']:
                                            st.markdown(f"**{j}. {option} ✓**")
                                        else:
                                            st.write(f"{j}. {option}")
                                    
                                    # Show explanation in an expander
                                    with st.expander("See Explanation"):
                                        st.write(question['explanation'])
                                    st.divider()
                    except json.JSONDecodeError as e:
                        st.error("Error parsing quiz")
                        st.write(quiz)  # Fallback to display raw output
                
                with tab3:
                    st.header("Suggested Projects")
                    projects = result.pydantic
                    if projects and hasattr(projects, 'projects'):
                        for project in projects.projects:
                            with st.container():
                                st.subheader(f"📋 {project.title}")
                                
                                # Create two columns for project details
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.markdown("**Description:**")
                                    st.write(project.description)
                                
                                with col2:
                                    st.markdown("**Quick Info:**")
                                    st.write(f"🔷 **Difficulty:** {project.difficulty}")
                                    st.write(f"⏱️ **Duration:** {project.estimated_duration}")
                                
                                # Skills and outcomes in expandable sections
                                with st.expander("Required Skills"):
                                    for skill in project.required_skills:
                                        st.markdown(f"• {skill}")
                                
                                with st.expander("Learning Outcomes"):
                                    for outcome in project.learning_outcomes:
                                        st.markdown(f"• {outcome}")
                                
                                st.divider()

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 