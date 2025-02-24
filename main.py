import os
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import BrowserAgents
from tasks import BrowserTasks

# Load environment variables
load_dotenv()

def main():
    # Check for API keys
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not found in environment variables.")
        print("Please create a .env file with your GEMINI_API_KEY.")
        return

    print("Welcome to the Gemini Browser Automation Agent!")
    user_query = input("Enter your automation query: ")

    agents = BrowserAgents()
    tasks = BrowserTasks()

    # Create Agents
    planner = agents.planner_agent()
    browser = agents.browser_agent()
    responder = agents.response_agent()

    # Create Tasks
    plan_task = tasks.plan_task(planner, user_query)
    browse_task = tasks.browse_task(browser, plan_task)
    response_task = tasks.response_task(responder, browse_task)

    crew = Crew(
        agents=[planner, browser, responder],
        tasks=[plan_task, browse_task, response_task],
        verbose=True,
        process=Process.sequential
    )

    result = crew.kickoff()
    print("\n\n########################")
    print("## Final Result ##")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    main()
