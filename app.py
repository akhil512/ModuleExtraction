import asyncio
from fastapi import FastAPI
from Agents import planner_agent, web_crawler_agent, response_agent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console 

app = FastAPI()
async def main(url:str):
    # Instantiate agents
    planner = planner_agent.PlannerAgent()
    web_scraper = web_crawler_agent.WebCrawlerAgent()
    responder = response_agent.ResponseAgent()
    termination = TextMentionTermination("TERMINATE")


    # Create a SelectorGroupChat with all agents
    group_chat = RoundRobinGroupChat(
        [planner, web_scraper, responder],
        termination_condition=termination
    )

    # Example: Start a conversation
    user_input = url
    response = await group_chat.run(task=user_input)

    return response.messages[-1].content.replace("TERMINATE", "").strip()

# if __name__ == "__main__":
#     response = asyncio.run(main(url = "https://wordpress.org/documentation/"))
#     print(response)

@app.get("/ask")
def ask_question(url: str):
    response = asyncio.run(main(url))
    return {"response": response}