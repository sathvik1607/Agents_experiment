import os
import sys
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

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


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

def get_gmail_service():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build(
        "gmail",
        "v1",
        credentials=creds
    )
# -----------------------------
# Tools
# -----------------------------

def get_weather(city: str) -> str:
    """
    Get weather for a given city.
    """
    return f"{city}!"


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
    Generate a short motivational thought.
    """

    response = llm.invoke(
        "Generate a short motivational thought in one sentence."
    )

    return response.content

def get_recent_email_subjects() -> list:
    """
    Fetch latest 2 email subjects.
    """

    try:

        service = get_gmail_service()

        results = service.users().messages().list(
            userId="me",
            maxResults=4
        ).execute()

        messages = results.get(
            "messages",
            []
        )

        if not messages:
            return ["No emails found"]

        subjects = []

        for msg in messages:

            message = service.users().messages().get(
                userId="me",
                id=msg["id"]
            ).execute()

            headers = message["payload"]["headers"]

            for header in headers:

                if header["name"] == "Subject":

                    subjects.append(
                        header["value"]
                    )

                    break

        return subjects

    except Exception as e:

        return [f"Error: {str(e)}"]
    
# -----------------------------
# Agent
# -----------------------------
agent = create_agent(
    model="openai:gpt-3.5-turbo",
    tools=[
        get_weather,
        get_post,
        create_daily_thought,
        get_recent_email_subjects
    ],
    system_prompt=(
        "You are a helpful assistant and an agent. "
        "Use tools whenever they are relevant and make no mistake."
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
