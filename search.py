import os
import requests

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def search_web(query):
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "basic",
                "max_results": 5
            },
            timeout=30
        )

        data = response.json()

        if "results" not in data:
            return None

        text = ""

        for item in data["results"]:
            text += f"{item['title']}\n"
            text += f"{item['content']}\n\n"

        return text

    except Exception:
        return None