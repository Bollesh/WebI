# WebI - AI Research Assistant

A comprehensive AI research assistant designed to provide accurate and efficient answers to user queries by retrieving relevant information from the internet and creating a vector database from the crawled data.

## Features:

*   **Google Query Generation**: Converts user inputs into precise Google search queries.
*   **Web Crawler Integration**: Uses an asynchronous web crawler to scrape and process data from websites.
*   **Semantic Search:** Utilizes advanced NLP techniques to find the most relevant documents or data points in the vector database.
*   **Vector Database:** Stores a vast amount of information on various topics, allowing for efficient retrieval of relevant data. Generated from the crawled data
*   **System Prompt:** Provides users with clear and concise instructions on how to use the assistant effectively.
*   **Proxy Management**: Manages a pool of working proxies for making HTTP requests.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Bollesh/WebI.git
   cd your-repo-name
   ```

2. Install dependencies using `pip`:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Main Application**:
   ```sh
   python main.py
   ```

2. **Interact with the Assistant**:
   - The assistant will prompt you to ask a question.
   - Enter your query and press enter.

3. **Example Interaction**:
   ```
   Ask anything: What is the best way to start a podcast?
   .
   . (gathers information from the internet and stores them in a vector database)
   .
   === RAG AGENT===
   What is your question: What is the best way to start a podcast?
   (performs a tool call to retrieve data from the vector database)
   === ANSWER ===
   ...
   ```

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
