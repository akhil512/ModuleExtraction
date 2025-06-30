import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from Agents import planner_agent, web_crawler_agent, response_agent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console 
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

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
async def ask(url: str):
    """
    FastAPI endpoint to orchestrate the multi-agent module extraction process.
    """
    try:
        response = await main(url)
        return {"response": response}
    except Exception as e:
        logging.error(f"Error in /ask endpoint: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})