# Technical Architecture: Module Extraction AI Agent

## Overview
This document describes the technical architecture, approach, assumptions, and edge case handling for the Module Extraction AI Agent system.

---

## Architecture Diagram (Textual)

```
User (Streamlit UI)
    |
    v
FastAPI Backend (app.py)
    |
    v
[Planner Agent] --delegates--> [Web Crawler Agent] --extracts--> [WebScraper Tool]
    |
    v
[Response Agent] --generates--> JSON Output
```

---

## Components

### 1. Frontend (Streamlit)
- Collects one or more documentation URLs from the user.
- Sends requests to the FastAPI backend and displays results.

### 2. Backend (FastAPI)
- Exposes an `/ask` endpoint for module extraction requests.
- Instantiates and coordinates the agents using `autogen_agentchat` and `langchain`.
- Handles async orchestration and returns the final response to the frontend or API user.

### 3. Agents
- **Planner Agent:** Receives the user query/URL(s), creates a plan, and delegates tasks to other agents.
- **Web Crawler Agent:** Crawls the parent URL, extracts main content, finds and crawls child links, and returns all content in a structured format.
- **Response Agent:** Analyzes the extracted content, infers modules and submodules, and generates a structured JSON response.

### 4. Tools
- **WebScraper:** Uses LangChain's `AsyncChromiumLoader` and `BeautifulSoupTransformer` to extract and clean content, ignoring navigation, headers, and footers.
- **WebCrawler:** Recursively crawls links within the same domain, respecting a max depth and avoiding duplicates.

---

## Approach & Assumptions
- **Content Extraction:** Uses tag/classname heuristics to ignore navigation, headers, and footers. Assumes documentation sites use standard HTML structure.
- **Domain Restriction:** Only crawls links within the same domain as the parent URL to avoid unrelated content.
- **Crawling Depth:** Controlled by a `max_depth` parameter to prevent infinite loops and excessive crawling.
- **Duplicate Handling:** Maintains a set of visited URLs to avoid re-crawling the same page.
- **Module/Submodule Inference:** Relies on LLM analysis of parent and child content. Assumes documentation is well-structured and uses clear sectioning.
- **Timeouts:** Streamlit and backend requests use generous timeouts to accommodate slow sites, but very large sites may still time out.
- **Error Handling:** All crawling and scraping is wrapped in try/except blocks; errors are logged and do not halt the entire process.
- **API Key:** Assumes a valid OpenAI API key and model access is available in `.env`.

---

## Edge Case Handling
- **Non-Standard HTML:** If a site uses unusual structure, some navigation or irrelevant content may be included in the extraction.
- **Redirects & Broken Links:** The crawler skips links that cannot be loaded or are outside the allowed domain.
- **Cyclic Links:** The crawler tracks visited URLs to avoid infinite loops.
- **Large Sites:** For very large documentation sites, increase `max_depth` or limit the number of child links per page for performance.
- **API/Model Errors:** If the LLM or API fails, the error is logged and the process continues for other URLs.

