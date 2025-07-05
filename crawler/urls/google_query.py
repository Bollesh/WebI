from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

num_of_queries = 10

model = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)

system_prompt = SystemMessage(
    """
        You are a simple assistant that understands what the user wants and converts their request into a concise, effective Google search query. 
        Your goal is to strip away unnecessary words and generate a short, relevant phrase that would return the most useful results on Google.

        Examples:

        User: What are the best smartphones in 2025?
        AI: best smartphones 2025

        User: Can you show me vegan restaurants near Central Park?
        AI: vegan restaurants near Central Park

        User: I need reviews for the Dyson V15 vacuum
        AI: Dyson V15 vacuum reviews

        User: What's the weather like in Tokyo tomorrow?
        AI: Tokyo weather tomorrow

        User: How to fix a leaky kitchen faucet?
        AI: fix leaky kitchen faucet

        User: Find me cheap flights from LA to New York next weekend
        AI: cheap flights LA to New York next weekend

        User: Who won the NBA game last night?
        AI: NBA game results last night

        User: Tell me the symptoms of flu vs covid
        AI: flu vs covid symptoms

        User: Where can I buy a Nintendo Switch in stock?
        AI: buy Nintendo Switch in stock

        User: I want to learn how to start a podcast
        AI: how to start a podcast
    """
)



def get_google_query(user_request: str):
    user_message = HumanMessage(user_request)
    prompt = [system_prompt] + [user_message]
    res = model.invoke(prompt)
    return f"https://google.com/search?q={res.content}&num={num_of_queries}"
    
