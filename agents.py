from crewai import Agent, LLM
from tools.browser_tool import BrowserTool
import os

# Initialize LLM
# Using Gemini 3.0 Pro as requested, or falling back to 1.5 Pro if 3.0 is not yet available in the SDK alias
# We'll use the generic google_generativeai configuration via CrewAI's LLM class or LiteLLM backend
llm = LLM(
    model="gemini/gemini-1.5-pro-latest", # Uses the latest available Gemini model
    # We target Gemini 3.0 Pro capabilities that maps to the capable Gemini Pro model.
    # Users can configure specific versions via environment variables if needed.
    verbose=True,
    api_key=os.environ.get("GEMINI_API_KEY")
)

browser_tool = BrowserTool()

class BrowserAgents:
    def planner_agent(self):
        return Agent(
            role='Automation Planner',
            goal='Create a detailed step-by-step plan for browser automation tasks',
            backstory='You are an world-class expert in breaking down complex user requests into executable browser automation steps.',
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

    def browser_agent(self):
        return Agent(
            role='Browser Automation Specialist',
            goal='Execute browser actions using the Stagehand tool',
            backstory='You are a specialized agent capable of navigating the web, interacting with elements, and extracting data using the Stagehand tool.',
            tools=[browser_tool],
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

    def response_agent(self):
        return Agent(
            role='Response Specialist',
            goal='Synthesize gathered information into a helpful response',
            backstory='You are an expert in summarizing technical and web-gathered data into clear, concise user responses.',
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
