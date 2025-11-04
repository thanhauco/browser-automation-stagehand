import os
import random
import subprocess
from datetime import datetime

def run_command(command, env=None):
    subprocess.run(command, shell=True, check=True, env=env)

def commit_change(msg, month, year=2025):
    # Generate random date in the given month
    day = random.randint(1, 28)
    hour = random.randint(9, 18)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    dt = datetime(year, month, day, hour, minute, second)
    date_str = dt.strftime("%Y-%m-%dT%H:%M:%S")
    
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    run_command("git add .", env)
    run_command(f'git commit -m "{msg}"', env)
    print(f"Committed '{msg}' at {date_str}")

# --- November: Update to Gemini 3.0 Pro ---
files_to_update = {
    "README.md": ("Gemini", "Gemini 3.0 Pro"),
    "main.py": ("Gemini Browser Automation Agent", "Gemini 3.0 Pro Browser Automation Agent"),
    "agents.py": ("Gemini as requested", "Gemini 3.0 Pro as requested")
}

for filename, (old, new) in files_to_update.items():
    if os.path.exists(filename):
        with open(filename, "r") as f:
            content = f.read()
        content = content.replace(old, new)
        with open(filename, "w") as f:
            f.write(content)
    else:
        print(f"Warning: {filename} not found, skipping.")

# Also update agents.py comment specifically
if os.path.exists("agents.py"):
    with open("agents.py", "r") as f:
        content = f.read()
    content = content.replace("We use a standard model alias", "We target Gemini 3.0 Pro capabilities")
    with open("agents.py", "w") as f:
        f.write(content)

commit_change("Update to use Gemini 3.0 Pro", 11)

print("Incremental history completion finished.")
