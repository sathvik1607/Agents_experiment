import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment.")

print(
    f"Loaded key: starts {api_key[:8]}... "
    f"ends ...{api_key[-4:]} "
    f"(length {len(api_key)})"
)

# -----------------------------
# Shared LLM
# -----------------------------
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
)

# -----------------------------
# Tools
# -----------------------------
def get_weather(city: str) -> str:
    """
    Get weather for a given city.
    """
    return f"It's always sunny in {city}!"


def get_post(post_id: int) -> dict[str, Any]:
    """
    Fetch a post from JSONPlaceholder by ID.
    """

    try:
        response = requests.get(
            f"https://jsonplaceholder.typicode.com/posts/{post_id}",
            timeout=10,
        )

        response.raise_for_status()

        data: dict[str, Any] = response.json()
        return data

    except requests.RequestException as e:
        return {"error": str(e)}


def create_daily_thought() -> str:
    """
    Generate a short inspirational thought.
    """

    response: BaseMessage = llm.invoke(
        "Generate a short inspirational thought in one sentence."
    )

    return str(response.content)


# -----------------------------
# Agent
# -----------------------------
agent = create_agent(
    model=llm,
    tools=[
        get_weather,
        get_post,
        create_daily_thought,
    ],
    system_prompt=(
        "You are a helpful assistant. "
        "Use tools whenever they are relevant."
    ),
)

# -----------------------------
# Main
# -----------------------------
def main() -> None:

    if len(sys.argv) < 2:
        print(
            'Usage: python dynamic_agent_input.py "your question"'
        )
        sys.exit(1)

    user_input = " ".join(sys.argv[1:])

    try:
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ]
            }
        )

        print("\n=== RESPONSE ===\n")

        messages = result["messages"]
        last_message: BaseMessage = messages[-1]

        print(str(last_message.content))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()