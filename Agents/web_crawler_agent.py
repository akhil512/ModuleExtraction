from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from LLM.model_client import ModelClient
from Prompts.prompt import SystemMessage
from Tools.web_crawler import WebCrawler

# WebCrawlerAgent wraps the WebCrawler tool for use in the agent system
class WebCrawlerAgent(AssistantAgent):
    def __init__(self):
        try:
            self.prompt = SystemMessage().web_crawler_agent_prompt
            self.model_client = ModelClient().get_model_client()
            self.web_crawler = WebCrawler
            async def web_crawler_tool(url: str):
                try:
                    return await WebCrawler(url).start()
                except Exception as crawl_err:
                    return {"error": str(crawl_err)}
            self.tool = FunctionTool(
                web_crawler_tool,
                name="web_crawler_tool",
                description="A tool to crawl web pages for content.",
            )
            super().__init__(
                name="web_crawler_agent",
                model_client=self.model_client,
                system_message=self.prompt,
                tools=[self.tool]
            )
        except Exception as e:
            # Log or handle initialization errors
            print(f"WebCrawlerAgent initialization error: {e}")