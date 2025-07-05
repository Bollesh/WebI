import asyncio

from rag_agent.rag_agent import run_agent
from crawler.crawler import parallel_crawler

user_query = input("Ask anything: ")

async def main():
    await parallel_crawler(user_query)
    run_agent()

if __name__ == "__main__":
    asyncio.run(main())