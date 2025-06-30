from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from LLM.model_client import ModelClient
from Prompts.prompt import SystemMessage
from Tools.web_crawler import WebCrawler

class WebCrawlerAgent(AssistantAgent):
    def __init__(self):
        self.prompt = SystemMessage().web_crawler_agent_prompt
        self.model_client = ModelClient().get_model_client()
        self.web_crawler = WebCrawler
        async def web_crawler_tool(url: str):
            return await WebCrawler(url).start()
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