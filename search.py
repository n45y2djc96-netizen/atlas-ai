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
                "max_results": 3
            },
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        if "results" not in data:
            return None

        parts = []

        for item in data["results"]:
            title = item.get("title", "")
            content = item.get("content", "")[:1000]

            if title or content:
                parts.append(
                    f"{title}\n{content}"
                )

        if not parts:
            return None

        return "\n\n".join(parts)[:3000]

    except Exception as e:
        print("SEARCH ERROR:", e)
        return None