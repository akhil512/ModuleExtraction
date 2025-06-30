from autogen_agentchat.agents import AssistantAgent
from LLM.model_client import ModelClient
from Prompts.prompt import SystemMessage

class ResponseAgent(AssistantAgent):
    def __init__(self):
        self.prompt = SystemMessage().response_agent_prompt
        self.model_client = ModelClient().get_model_client()
        super().__init__(
            name="response_agent",
            model_client=self.model_client,
            system_message=self.prompt,
        )