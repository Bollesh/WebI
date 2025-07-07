# AI Research Assistant
==========================

A comprehensive AI research assistant designed to provide accurate and efficient answers to user queries by retrieving relevant information from a vector database.

**Project Title:** AI Research Assistant
**Description:**
The AI Research Assistant is a cutting-edge tool that leverages the power of natural language processing (NLP) and semantic search to retrieve relevant information from a vast vector database. This project aims to provide users with accurate, concise, and informative responses to their queries.

## Features:

*   **Google Query Generation**: Converts user inputs into precise Google search queries.
*   **Web Crawler Integration**: Uses an asynchronous web crawler to scrape and process data from websites.
*   **Semantic Search:** Utilizes advanced NLP techniques to find the most relevant documents or data points in the vector database.
*   **Vector Database:** Stores a vast amount of information on various topics, allowing for efficient retrieval of relevant data. Generated from the crawled data
*   **System Prompt:** Provides users with clear and concise instructions on how to use the assistant effectively.
*   **Proxy Management**: Manages a pool of working proxies for making HTTP requests.

## Installation:

1.  Clone the repository using `git clone https://github.com/your-username/AI-Research-Assistant.git`
2.  Install the required dependencies by running `pip install -r requirements.txt`

## Usage:

1.  Run the main script using `python main.py`. Initially crawls through google and sets up a vector database.
2.  Interact with the assistant by asking questions or providing prompts
3.  The assistant will respond with accurate and concise answers

## Project Structure
The project is organized into the following directories:

*   `crawler`: Contains the crawler module responsible for retrieving data from the vector database.
*   `paths`: Contains all the paths to the txt files and the persistent directory of the vector database
*   `rag_agent`: Contains the RAG agent
*   `main.py`: The main script that runs the AI Research Assistant.
*   `vectorDB`: Stores the vector database. Initially empty

The project is organized as follows:

```
ai-research-assistant/
├── crawler/                        
|   |── exceptions/
|   |   └── crawl_exception.py      
│   ├── urls/
|   |   ├── url_generator
│   │   └── google_query.py
|   ├── proxies/
│   |   ├── proxy.py
|   |   └── proxy_checker.py
│   └── crawler.py
├── paths/
|   └── paths.py 
├── rag_agent/
|   └── rag_agent.py
├── vectorDB/ 
├── main.py
├── README.md
└── requirements.txt
```

## Dependencies
- `langchain` for AI workflows
- `langchain_ollama` for Ollama model integration
- `langchain_chroma` for vector storage
- `crawl4ai` for web crawling
- `asyncio` for asynchronous operations
- `logging` for debugging
