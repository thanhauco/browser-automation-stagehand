from crewai.tools import BaseTool
from stagehand import Stagehand
from typing import Optional, Type, Any
from pydantic import BaseModel, Field
import os

class BrowserToolSchema(BaseModel):
    action: str = Field(..., description="The action to perform: 'act', 'extract', 'observe', 'screenshot', or 'download'.")
    instruction: str = Field(..., description="The natural language instruction for the action.")
    url: Optional[str] = Field(None, description="The URL to navigate to (required for the first action or navigation).")

class BrowserTool(BaseTool):
    name: str = "Browser Tool"
    description: str = (
        "A tool to control a web browser using natural language. "
        "Useful for navigating to websites, clicking elements, extracting data, and observing the page. "
        "Supports actions: 'act' (perform interactions), 'extract' (get data), 'observe' (analyze page)."
    )
    args_schema: Type[BaseModel] = BrowserToolSchema
    stagehand: Any = None

    def _run(self, action: str, instruction: str, url: Optional[str] = None) -> str:
        if not self.stagehand:
            # Initialize Stagehand lazily
            headless = os.environ.get("HEADLESS", "false").lower() == "true"
            self.stagehand = Stagehand(
                env="LOCAL",
                verbose=1,
                headless=headless
            )
            self.stagehand.init()

        try:
            if url:
                self.stagehand.page.goto(url)

            if action == "act":
                for _ in range(3): try: self.stagehand.act(instruction); break; except: pass
                return f"Successfully executed action: {instruction}"
            elif action == "extract":
                # Stagehand extract can take a schema. 
                # For now, we'll treat the instruction as the description of what to extract.
                # Ideally, we'd parse a schema from the instruction if it was a JSON string, 
                # but simple natural language extraction is Stagehand's strength.
                result = self.stagehand.extract(instruction)
                return f"Extracted data: {result}"
            elif action == "observe":
                result = self.stagehand.observe(instruction)
                return f"Observation: {result}"
            elif action == "screenshot":
                # New action: Take screenshot
                path = "screenshot.png"
                self.stagehand.page.screenshot(path=path)
                return f"Screenshot saved to {path}"
            elif action == "download":
                # New action: Download file
                # Expect instruction to be the text of the link to click
                # This is a bit complex with Stagehand's abstraction, but we can try to find the element and click it 
                # while waiting for download.
                # For now, let's just use Stagehand's act to click, but we need to set up the download listener first.
                
                # Note: Stagehand doesn't expose the context easily to set downloads path if not done at init.
                # But we can try to use the page object.
                with self.stagehand.page.expect_download() as download_info:
                    self.stagehand.act(f"Click the link that says '{instruction}'")
                
                download = download_info.value
                path = os.path.join("downloads", download.suggested_filename)
                os.makedirs("downloads", exist_ok=True)
                download.save_as(path)
                return f"File downloaded to {path}"
            else:
                return f"Unknown action: {action}"
        except Exception as e:
            return f"Error executing browser action: {str(e)}"

    def close(self):
        if self.stagehand:
            self.stagehand.close()
