# Browser Automation Agent

A local, open-source Browser Automation Agent using **CrewAI** and **Stagehand**, powered by **Gemini **.

## Features
- **Natural Language Automation**: Control the browser with plain English.
- **Local Execution**: Runs entirely on your machine using Playwright.
- **Agentic Workflow**: Uses CrewAI to plan, execute, and summarize tasks.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

2.  **Configure Environment**:
    Create a `.env` file and add your Gemini API Key:
    ```bash
    cp .env.example .env
    # Edit .env
    ```

## Usage

Run the agent:
```bash
python main.py
```

## Advanced Features
- **Headless Mode**: Set `HEADLESS=true` in `.env` to run without a visible browser.
- **Vision**: The agent can take screenshots if you ask it to "take a screenshot".
- **Downloads**: The agent can download files if you ask it to "download [link text]". Files are saved to the `downloads/` folder.
- **Extraction**: You can ask for specific data formats, e.g., "Extract a list of products with name and price".

## Architecture
- **Planner Agent**: Breaks down the query into steps.
- **Browser Agent**: Uses `Stagehand` (via `BrowserTool`) to execute steps locally.
- **Response Agent**: Summarizes the results.

## Troubleshooting
- **Stagehand Errors**: Ensure Playwright is installed correctly (`playwright install`).
- **API Errors**: Check your `GEMINI_API_KEY` in `.env`.

## Tech Stack
- [CrewAI](https://crewai.com) - Orchestration
- [Stagehand](https://stagehand.dev) - Browser Automation
- [Gemini](https://deepmind.google/technologies/gemini/) - Intelligence
