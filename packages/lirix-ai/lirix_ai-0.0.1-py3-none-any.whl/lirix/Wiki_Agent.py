from pydantic_ai import Agent, RunContext, models
from pydantic_ai.messages import ModelMessage, ModelResponse, ModelRequest, UserPromptPart
from pydantic_ai.models.groq import GroqModel
from pydantic import BaseModel
from dataclasses import dataclass
from typing import List, Optional
import asyncio
import aiohttp
import json
import os
import re

CACHE_FILE = "wiki_cache.json"

@dataclass
class SearchResult:
    title: str
    snippet: str

@dataclass
class WikiResults:
    results: List[SearchResult]

class WikiAgent:
    def __init__(self, model: BaseModel, wiki_api_key: str, system_prompt: str = (
    "You are a helpful assistant. You can have a conversation with the user and answer general questions. "
    "Only use the Wikipedia search tool when the user **explicitly asks** for it by saying 'search the wiki for ...'. "
    "Otherwise, respond as a normal chatbot."
    )
):
        self.model = model
        self.wiki_api_key = wiki_api_key
        self.cache = self.load_cache()
        
        @dataclass
        class Deps:
            pass
        
        self.deps = Deps()
        self.agent = Agent(model=self.model, system_prompt=system_prompt, deps_type=Deps, retries=2)
        self.messages: List[ModelMessage] = []
        self._register_tools()

    def _register_tools(self):
        @self.agent.tool_plain(retries=1)
        async def search_wikipedia(query: str) -> str:
            '''Searches the given query on Wikipedia'''
            return await self.instance_search_wikipedia(query)

    def load_cache(self):
        """Loads cache from the JSON file."""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def save_cache(self):
        """Saves updated cache to JSON file."""
        with open(CACHE_FILE, 'w') as file:
            json.dump(self.cache, file, indent=4)

    async def instance_search_wikipedia(self, query: str) -> str:
        '''Instance method to search Wikipedia.'''
        if not isinstance(self.cache, dict):
            self.cache = {}

        if query.lower() in (cached_query.lower() for cached_query in self.cache):
            return f"🔍 Cached Wikipedia Search: {self.cache[query]}"
        
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "utf8": 1,
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                search_results = data.get("query", {}).get("search", [])
                
                if not search_results:
                    return "No results found."
                
                top_result = search_results[0]
                title = top_result['title']
                snippet = top_result['snippet']
                result_text = f"**{title}**: {snippet}..."
                
                self.cache[query] = result_text
                self.save_cache()
            return f"🔍 Wikipedia Search: {result_text}"

    async def process_user_input(self, user_input: str):
        """Processes user input and calls Wikipedia search if needed."""
        if user_input.lower() == "clear":
            self.messages.clear()
            return "Conversation cleared."
        
        if "search the wiki" in user_input.lower():
            query = user_input.replace("search the wiki", "").strip()
            return await self.instance_search_wikipedia(query=query)
        
        self.messages.append(ModelRequest(parts=[UserPromptPart(content=user_input)]))
        self.messages[:] = self.messages[-5:]
        response = await self.agent.run(user_prompt=user_input, message_history=self.messages, deps=self.deps)
        if isinstance(response.data, str):
    # Ignore tool calls if they don't match a proper wiki search request
            if 'search_wikipedia' in response.data and 'query' in response.data:
                match = re.search(r'search_wikipedia\s*,\s*\{"query":\s*"(.*?)"\}', response.data)
                if match:
                    query = match.group(1)
                    search_result = await self.instance_search_wikipedia(query)
                    return f"🔍 Wikipedia Search: {search_result}"
            
            return f"Bot: {response.data}"

# Usage Example
if __name__ == "__main__":
    def get_model(model_type: str, model_name: str, api_key: str) -> BaseModel:
        if model_type.lower() == "groq":
            return GroqModel(model_name=model_name, api_key=api_key)
        raise ValueError(f"Unsupported model type: {model_type}")
    
    async def main():
        model_type = "groq"
        llm = "llama-3.3-70b-versatile"
        api_key = "GROQ_API_KEY"
        wikimedia_api_key = "WIKIMEDIA_API_KEY"

        model = get_model(model_type, llm, api_key)
        wiki_agent = WikiAgent(model, wikimedia_api_key)

        while True:
            user_message = input("You: ")
            response = await wiki_agent.process_user_input(user_message)
            
            if response.lower() == "exiting...":
                break
            
            print(response)
    
    asyncio.run(main())