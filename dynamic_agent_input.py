import os
import sys
import requests

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print(
        f"Loaded key: starts {api_key[:8]}... "
        f"ends ...{api_key[-4:]} "
        f"(length {len(api_key)})"
    )
else:
    raise ValueError("OPENAI_API_KEY not found in environment.")

# -----------------------------
# Shared LLM
# -----------------------------
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

# -----------------------------
# Tools
# -----------------------------
def get_weather(city: str) -> str:
    """
    Get weather for a given city.
    """
    return f"It's always sunny in {city}!"


def get_post(id: int) -> dict:
    """
    Fetch a post from JSONPlaceholder by ID.
    Example: get_post(2)
    """

    try:
        response = requests.get(
            f"https://jsonplaceholder.typicode.com/posts/{id}",
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:
        return {
            "error": str(e)
        }


def create_daily_thought() -> str:
    """
    Generate a short inspirational thought.
    """

    response = llm.invoke(
        "Generate a short inspirational thought in one sentence."
    )

    return response.content


# -----------------------------
# Agent
# -----------------------------
agent = create_agent(
    model="openai:gpt-3.5-turbo",
    tools=[
        get_weather,
        get_post,
        create_daily_thought
    ],
    system_prompt=(
        "You are a helpful assistant. "
        "Use tools whenever they are relevant."
    ),
)

# -----------------------------
# CLI Input
# -----------------------------
if len(sys.argv) < 2:
    print(
        'Usage: python dynamic_agent_input.py "your question"'
    )
    sys.exit(1)

user_input = " ".join(sys.argv[1:])

# -----------------------------
# Execute Agent
# -----------------------------
try:
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }
    )

    print("\n=== RESPONSE ===\n")
    print(result["messages"][-1].content)

except Exception as e:
    print(f"Error: {e}")