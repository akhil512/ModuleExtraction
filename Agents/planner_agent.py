from autogen_agentchat.agents import AssistantAgent
from LLM.model_client import ModelClient
from Prompts.prompt import SystemMessage



class PlannerAgent(AssistantAgent):
    def __init__(self):
        self.prompt = SystemMessage().planner_agent_prompt
        self.model_client = ModelClient().get_model_client()
        super().__init__(
            name="planner_agent",
            model_client=self.model_client,
            system_message=self.prompt
        )
