import datetime
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
from pydantic import BaseModel, Field
from load_api_key import Settings
from typing import Any, List
from dataclasses import dataclass
from tavily import AsyncTavilyClient
import nest_asyncio
import asyncio
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Dataclass for search parameters
@dataclass
class SearchDataclass:
    max_results: int
    todays_date: str

# Dataclass for research dependencies
@dataclass
class ResearchDependencies:
    todays_date: str
    search_deps: SearchDataclass

# Pydantic model for research results
class ResearchResult(BaseModel):
    research_title: str = Field(description='Markdown heading describing the article topic')
    research_main: str = Field(description='A main section that provides a detailed article based on search results')
    research_bullets: List[str] = Field(description='A list of bullet points that summarize the article')

# Class to encapsulate the search agent and its functionality
class SearchAgentWrapper:
    def __init__(self, groq_api_key: str, tavily_api_key: str, model_name: str = "llama-3.3-70b-versatile"):
        # Initialize the Groq model with tool definition
        self.model = GroqModel(
            model_name=model_name,
            api_key=groq_api_key,
            # Try forcing tool_choice to auto to make the model use the tools 
        )

        # Initialize Tavily client
        self.tavily_client = AsyncTavilyClient(api_key=tavily_api_key)

        # Initialize the search agent
        self.search_agent = Agent(
            self.model,
            result_type=ResearchResult,
            deps_type=ResearchDependencies,
            system_prompt=(
                "You are a researcher that MUST use search tools to find information. "
                "You are not allowed to make up information or rely on your training data.\n\n"
                "When given a query, you MUST use the get_search tool at least 3 times with different search queries "
                "to gather information before providing an answer.\n\n"
                "TOOL USE INSTRUCTIONS:\n"
                "1. You MUST call the get_search tool using exactly this format: get_search(query=\"your search query\", query_number=N)\n"
                "2. Make 3-5 different search queries to gather comprehensive information\n"
                "3. Only after collecting search results should you formulate your final answer\n"
                "4. Your final answer MUST be based solely on the search results, not prior knowledge\n\n"
                "Example correct tool usage:\n"
                "get_search(query=\"iPhone 16 price rumors\", query_number=1)\n"
                "get_search(query=\"Apple iPhone 16e announcement date\", query_number=2)\n"
                "get_search(query=\"iPhone 16e vs iPhone SE price comparison\", query_number=3)\n\n"
                "DO NOT proceed without using the search tool."
            ),
        )

        # System prompt with today's date
        @self.search_agent.system_prompt
        async def add_current_date(ctx: RunContext[ResearchDependencies]) -> str:
            todays_date = ctx.deps.todays_date
            system_prompt = (
                f"You are a researcher that MUST use search tools to find information. "
                f"You are not allowed to make up information or rely on your training data.\n\n"
                f"When given a query, you MUST use the get_search tool at least 3 times with different search queries "
                f"to gather information before providing an answer.\n\n"
                f"Today's date is {todays_date}.\n\n"
                f"TOOL USE INSTRUCTIONS:\n"
                f"1. You MUST call the get_search tool using exactly this format: get_search(query=\"your search query\", query_number=N)\n"
                f"2. Make 3-5 different search queries to gather comprehensive information\n"
                f"3. Only after collecting search results should you formulate your final answer\n"
                f"4. Your final answer MUST be based solely on the search results, not prior knowledge\n\n"
                f"Example correct tool usage:\n"
                f"get_search(query=\"iPhone 16 price rumors\", query_number=1)\n"
                f"get_search(query=\"Apple iPhone 16e announcement date\", query_number=2)\n"
                f"get_search(query=\"iPhone 16e vs iPhone SE price comparison\", query_number=3)\n\n"
                f"DO NOT proceed without using the search tool."
            )
            return system_prompt

        # Search tool for Tavily with enhanced logging
        @self.search_agent.tool
        async def get_search(search_data: RunContext[ResearchDependencies], query: str, query_number: int) -> dict[str, Any]:
            max_results = search_data.deps.search_deps.max_results
            try:
                logger.info(f"EXECUTING SEARCH QUERY #{query_number}: '{query}'")
                results = await self.tavily_client.get_search_context(query=query, max_results=max_results)
                logger.info(f"Received {len(results)} search results for query '{query}'")
                
                # Add more detailed logging about what was found
                if results:
                    logger.info(f"First result snippet: {results[0][:100] if len(results[0]) > 100 else results[0]}...")
                
                return results
            except Exception as e:
                logger.error(f"Error in get_search: {e}")
                raise

    async def do_search(self, query: str, max_results: int):
        current_date = datetime.date.today()
        data_string = current_date.strftime("%Y-%m-%d")
        search_deps = SearchDataclass(max_results=max_results, todays_date=data_string)
        deps = ResearchDependencies(todays_date=data_string, search_deps=search_deps)
        try:
            logger.info(f"Starting search for query: '{query}'")
            result = await self.search_agent.run(query, deps=deps)
            logger.info(f"Search completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in do_search: {e}")
            raise