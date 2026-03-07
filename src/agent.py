"""
Core HR agent logic with modular architecture.
"""
from typing import List, Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent

# Import tools
from tools import (
    schedule_interview,
    screen_candidate,
    research_candidate,
    get_interview_prep,
    analyze_culture_fit,
    research_salary,
    hr_assistant,
    set_modular_components
)

# Import modular architecture
from core.planner import TaskPlanner
from core.router import TaskRouter
from core.executor import Executor
from core.aggregator import ResultAggregator

# Import specialized modules
from modules.calendar_manager import CalendarManager
from modules.recruiter import Recruiter
from modules.researcher import Researcher
from modules.interview_coach import InterviewCoach
from modules.culture_analyzer import CultureAnalyzer


class Agent:
    def __init__(self):
        self.name = "HR Agent - Agents of Chaos"

        # Initialize modular architecture
        self.planner = TaskPlanner()
        self.router = TaskRouter()
        self.executor = Executor(self.router)
        self.aggregator = ResultAggregator()

        # Register specialized modules
        self.router.register_module(CalendarManager())
        self.router.register_module(Recruiter())
        self.router.register_module(Researcher())
        self.router.register_module(InterviewCoach())
        self.router.register_module(CultureAnalyzer())

        # Set modular components for tools
        set_modular_components(self.planner, self.executor, self.aggregator)

        # Define tools
        self.tools = [
            schedule_interview,
            screen_candidate,
            research_candidate,
            get_interview_prep,
            analyze_culture_fit,
            research_salary,
            hr_assistant
        ]

        # Initialize LLM
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

        prompt = ChatPromptTemplate.from_messages([
            ("system",
             """You are an expert HR assistant built by team "Agents of Chaos" for Buildathon 2026.

Your role is to help with:
1. SCHEDULING: Schedule interviews and meetings
2. RECRUITING: Screen candidates, evaluate resumes, manage hiring pipeline
3. RESEARCH: Research candidates, companies, salaries, and market trends
4. INTERVIEW PREP: Generate interview questions, provide coaching and feedback
5. CULTURE FIT: Analyze candidate-company alignment and team dynamics

UNIQUE FEATURES:
- AI Interview Coach: Comprehensive interview preparation and feedback
- Culture Fit Analyzer: Deep analysis of candidate-company compatibility

Available tools:
- schedule_interview: Schedule interviews with candidates
- screen_candidate: Evaluate and screen candidates
- research_candidate: Research candidate backgrounds
- get_interview_prep: Generate interview questions and prep materials
- analyze_culture_fit: Assess culture compatibility
- research_salary: Get salary data and compensation info
- hr_assistant: Handle complex multi-step HR tasks

GUIDELINES:
- Be professional, helpful, and efficient
- Use specific tools for focused tasks
- Use hr_assistant for complex multi-step requests
- Provide actionable insights and recommendations
- Be encouraging and supportive in interview coaching
- Consider both hard skills and culture fit in evaluations

Always aim to provide comprehensive, practical assistance."""),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_tool_calling_agent(self.llm, self.tools, prompt)

        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True
        )

    def process_message(self, message_text: str) -> str:
        """
        Process the incoming message using LangChain.
        """
        result = self.agent_executor.invoke({"input": message_text})
        return result["output"]