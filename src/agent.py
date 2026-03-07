"""
Core agent logic.
"""
from typing import List, Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent

# Existing tools
from tools import example_tool, modular_agent

class Agent:
    def __init__(self):

        self.name = "FastAPI Agent"

        # Initialize modular architecture
        self.planner = TaskPlanner()
        self.router = TaskRouter()
        self.executor = Executor(self.router)
        self.aggregator = ResultAggregator()

        # Register modular system as a tool
        

        # Define tools
        self.tools = [example_tool, modular_agent]

        # Initialize LLM
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)

        prompt = ChatPromptTemplate.from_messages([
            ("system",
             """You are a helpful assistant.

You can solve tasks yourself or use tools.

Available tools:
- example_tool
- modular_agent (for complex multi-step tasks)

Use modular_agent when a task requires planning and multiple steps.
"""),
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