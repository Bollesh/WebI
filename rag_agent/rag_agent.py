import os
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, SystemMessage
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain_core.tools import tool
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END

from paths.paths import crawled_websites_path, persistent_directory

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
_retriever = None

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
    callback_manager=callback_manager
)

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)
def split_text():

    text_loader = TextLoader(crawled_websites_path)

    pages = text_loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )

    return text_splitter.split_documents(pages)

def create_retriever():
    global _retriever
    collection_name = "rag_vector_data"

    if not os.path.exists(persistent_directory):
        os.makedirs(persistent_directory)

    try:
        vectorstore = Chroma.from_documents(
            documents=split_text(),
            embedding=embeddings,
            persist_directory=persistent_directory,
            collection_name=collection_name
        )
        print(f"Created ChromaDB vector store")
    except Exception as e:
        print(f"Error setting up ChromaDB: {e}")
        raise


    _retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

@tool
def retreiver_tool(query: str)->str:
    """
        This tool searches and retrieves relevant data from the vector database
    """
    docs = _retriever.invoke(query)  # type: ignore

    if not docs:
        return f"Found no relevant data in the given document {crawled_websites_path}"
    
    results = []
    for i, doc in enumerate(docs):
        results.append(f"Document {i+1}:\n{doc.page_content}")
    
    return "\n\n".join(results)

tools = [retreiver_tool]

llm = llm.bind_tools(tools)

class StateAgent(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def should_continue(state: StateAgent):
    """Check if the last message contains tool calls."""
    result = state['messages'][-1]
    return hasattr(result, 'tool_calls') and len(result.tool_calls) > 0 # type: ignore

system_prompt = """
You are an AI research assistant. Your role is to accurately and efficiently
answer user questions by retrieving relevant information from a vector database.
Use semantic search to find the most relevant documents or data points,
then synthesize that information into clear, concise, and informative responses.
If necessary, explain your reasoning and cite specific sources or excerpts from the retrieved data.
Prioritize factual accuracy, relevance, and clarity in every response.
"""

tools_dict = {our_tool.name: our_tool for our_tool in tools} # Creating a dictionary of our tools

# LLM Agent
def agent(state:StateAgent) -> StateAgent:
    """Function to call the LLM in the current state"""
    messages = list(state["messages"])
    messages = [SystemMessage(content=system_prompt)] + messages
    message = llm.invoke(messages)
    return {"messages": [message]}

# Retriever Agent
def take_action(state: StateAgent) -> StateAgent:
    """Execute tool calls from the LLM's response."""

    tool_calls = state['messages'][-1].tool_calls # type: ignore
    results = []
    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query', 'No query provided')}")
        
        if not t['name'] in tools_dict: # Checks if a valid tool is present
            print(f"\nTool: {t['name']} does not exist.")
            result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."
        
        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query', ''))
            print(f"Result length: {len(str(result))}")
            

        # Appends the Tool Message
        results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))

    print("Tools Execution Complete. Back to the model!")
    return {'messages': results}

def create_graph():
    graph = StateGraph(StateAgent)
    graph.add_node("agent", agent)
    graph.add_node("retriever_agent", take_action)

    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            True: "retriever_agent",
            False: END
        }
    )

    graph.add_edge("retriever_agent", "agent")
    graph.set_entry_point("agent")

    return graph.compile()

def run_agent():
    create_retriever()
    rag_agent = create_graph()
    print("\n=== RAG AGENT===")
    
    while True:
        user_input = input("\nWhat is your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        messages = [HumanMessage(content=user_input)] # converts back to a HumanMessage type

        result = rag_agent.invoke({"messages": messages})
        
        print("\n=== ANSWER ===")
        print(result['messages'][-1].content)
    

