import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def perform_web_search(query):
    """
    Searches the live web for evidence using Tavily.
    """
    try:
        # Search for the claim. We search for 'news' and 'science' 
        # to get high-quality factual results.
        response = tavily.search(query=query, search_depth="advanced", max_results=3)
        
        context = ""
        sources = []
        
        for result in response['results']:
            context += f"- {result['content']}\n"
            sources.append(result['url'])
            
        return context, sources
    except Exception as e:
        return f"Search failed: {str(e)}", []