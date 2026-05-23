from tavily import TavilyClient

from utils.config import get_secret

tavily = TavilyClient(
    api_key=get_secret(
        "TAVILY_API_KEY"
    )
)


def search_web(query: str):

    response = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=2
    )

    results = []

    for result in response["results"]:

        formatted = f"""
Title:
{result['title']}

Content:
{result['content']}

URL:
{result['url']}
"""

        results.append(formatted)

    return results