from crewai import Task

class BrowserTasks:
    def plan_task(self, agent, user_query):
        return Task(
            description=f'Analyze the incoming user query deeply: "{user_query}". Create a detailed, step-by-step plan to achieve this using browser automation. \n\n'
                        'The plan should include:\n'
                        '1. The starting URL.\n'
                        '2. A sequence of specific actions (act, extract, observe) to perform.\n'
                        '3. What data to look for or what success looks like.',
            expected_output='A numbered list of steps for the Browser Automation Specialist to follow.',
            agent=agent
        )

    def browse_task(self, agent, context_task):
        return Task(
            description='Execute the browser automation plan provided in the context. \n'
                        'Use the Browser Tool to navigate, interact, and extract information. \n'
                        'Follow the steps exactly. If a step fails, attempt to recover or report the error clearly.',
            expected_output='A log of actions taken and the raw data or observations extracted from the website.',
            agent=agent,
            context=[context_task] # Explicitly depend on the plan task
        )

    def response_task(self, agent, context_task):
        return Task(
            description='Review the execution logs and extracted data from the browser task. \n'
                        'Synthesize this information into a clear, concise, and helpful response for the user. \n'
                        'If the automation failed, explain why.',
            expected_output='A final response to the user answering their original query.',
            agent=agent,
            context=[context_task] # Explicitly depend on the browse task
        )
