try:
    from stagehand import Stagehand
    print("Stagehand import successful")
except ImportError as e:
    print(f"Stagehand import failed: {e}")

try:
    from crewai import Agent, Task, Crew
    print("CrewAI import successful")
except ImportError as e:
    print(f"CrewAI import failed: {e}")

try:
    from playwright.sync_api import sync_playwright
    print("Playwright import successful")
except ImportError as e:
    print(f"Playwright import failed: {e}")
