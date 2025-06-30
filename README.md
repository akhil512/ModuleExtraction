# Module Extraction AI Agent

This is a **private repository** for an AI-powered system that extracts structured information (modules and submodules) from documentation-based help websites. The system uses a multi-agent architecture with FastAPI as a backend and Streamlit as a frontend.

---

## Features
- Accepts one or more documentation URLs as input
- Crawls parent and child documentation pages
- Extracts and cleans main content (ignoring navigation, headers, footers)
- Identifies modules and submodules, generating detailed descriptions
- Returns results in a structured JSON format
- Interactive Streamlit UI for easy use

---

## Project Structure
```
ModuleExtraction/
├── Agents/                # Agent definitions (Planner, WebCrawler, Response)
├── LLM/                   # Model client setup
├── Prompts/               # System prompts for each agent
├── Tools/                 # Web scraping and crawling utilities
├── app.py                 # FastAPI backend
├── streamlit_app.py       # Streamlit frontend
├── requirements.txt       # Python dependencies
├── README.md              # This file
```

---

## Setup Instructions

### 1. Clone the repository (private)
```sh
git clone <your-private-repo-url>
cd ModuleExtraction
```

### 2. Create and activate a virtual environment
```sh
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory with your OpenAI API key and model name:
```
OPENAI_KEY=<replace with your key>
MODEL_NAME=gpt-4.1-nano-2025-04-14
```

---

## Usage Examples

### 1. Start the FastAPI backend
```sh
uvicorn app:app --reload
```
- The API will be available at `http://127.0.0.1:8000`.

### 2. Start the Streamlit frontend
In a new terminal (with the virtual environment activated):
```sh
streamlit run streamlit_app.py
```
- The UI will be available at `http://localhost:8501`.

### 3. Using the Application
- Enter one or more documentation URLs (one per line) in the Streamlit UI.
- Click "Extract Modules" to start extraction.
- The results will be displayed for each link, showing the extracted modules and submodules in JSON format.

### 4. Direct API Usage
You can also use the FastAPI endpoint directly:
```sh
curl "http://127.0.0.1:8000/ask?url=https://help.zluri.com/"
```

---

## Design Rationale
- **Multi-Agent System:** The application uses a planner agent, a web crawler agent, and a response agent to separate concerns and allow for extensibility.
- **LangChain & Autogen:** Leverages LangChain for robust web scraping and document transformation, and Autogen for agent orchestration.
- **FastAPI Backend:** Provides a scalable, async API for agent orchestration and integration with other services.
- **Streamlit Frontend:** Offers a user-friendly interface for non-technical users to interact with the system.
- **Modular Design:** Each agent and tool is modular, making it easy to extend or swap components as needed.

---

## Known Limitations
- **Crawling Depth:** The crawler is limited by a max depth parameter; very deep or cyclic sites may not be fully explored.
- **Content Extraction:** The system relies on heuristics (tags, classnames) to ignore navigation and extract main content; results may vary for non-standard sites.
- **LLM Dependency:** Module and submodule inference depends on the quality of the LLM and the clarity of the documentation.
- **Performance:** Large sites or many URLs may result in slow processing due to sequential agent orchestration and web scraping.
- **API Key Required:** Requires a valid OpenAI API key and model access.
- **Not Production-Hardened:** This is a research/development project and may require further security and scalability work for production use.

---

## Troubleshooting
- If you see `asyncio.run() cannot be called from a running event loop`, run the backend from a standard terminal, not Jupyter.
- If you get connection errors in Streamlit, ensure FastAPI is running and accessible at `localhost:8000`.
- For long-running crawls, increase the timeout in `streamlit_app.py` if needed.

---

## License
MIT License
