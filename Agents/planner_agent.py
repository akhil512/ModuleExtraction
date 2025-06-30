from autogen_agentchat.agents import AssistantAgent
from LLM.model_client import ModelClient
from Prompts.prompt import SystemMessage



# PlannerAgent is responsible for planning the extraction process
class PlannerAgent(AssistantAgent):
    def __init__(self):
        try:
            self.prompt = SystemMessage().planner_agent_prompt
            self.model_client = ModelClient().get_model_client()
            super().__init__(
                name="planner_agent",
                model_client=self.model_client,
                system_message=self.prompt
            )
        except Exception as e:
            # Log or handle initialization errors
            print(f"PlannerAgent initialization error: {e}")
