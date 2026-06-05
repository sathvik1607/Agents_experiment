# Dynamic Agent — Setup & Run Guide

A LangGraph-powered AI agent with two tools: **get_weather** and **create_daily_thought**,
driven by OpenAI's GPT-4o model.

---

## Prerequisites

- Python **3.10 or higher** installed
- An **OpenAI API key** (get one at https://platform.openai.com/api-keys)
- Basic familiarity with the terminal / command prompt

---

## Step-by-Step Setup

### Step 1 — Clone or Download the Project

Place both files in the same folder on your machine:
```
my_agent/
├── dynamic_agent_input.py
├── .env
└── requirements.txt
```

---

### Step 2 — Create a Virtual Environment

It is best practice to isolate dependencies in a virtual environment.

```bash
# Navigate into your project folder
cd my_agent

# Create a virtual environment named 'venv'
python -m venv venv
```

Activate it:

| OS | Command |
|---|---|
| macOS / Linux | `source venv/bin/activate` |
| Windows (CMD) | `venv\Scripts\activate` |
| Windows (PowerShell) | `venv\Scripts\Activate.ps1` |

You should see `(venv)` at the start of your terminal prompt.

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
| Package | Purpose |
|---|---|
| `langchain` | Core LangChain framework |
| `langchain-openai` | OpenAI integration for LangChain |
| `langgraph` | Provides `create_agent` (used in the script) |
| `python-dotenv` | Loads API keys from the `.env` file |

---

### Step 4 — Set Up Your `.env` File

Create a file named `.env` in the project folder (no other extension):

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
```

Replace the value with **your own OpenAI API key**.

> ⚠️ **Never share or commit your `.env` file.** Add it to `.gitignore` if using Git.

---

### Step 5 — Run the Agent

Pass your message as a command-line argument:

```bash
python dynamic_agent_input.py "What is the weather in Hyderabad?"
```

```bash
python dynamic_agent_input.py "Give me today's daily thought"
```

```bash
python dynamic_agent_input.py "What is the weather in Mumbai and also give me a daily thought"
```

---

## How It Works

```
User Input (CLI)
      │
      ▼
  Agent (GPT-4o)
      │
      ├──► get_weather(city)         → Returns a weather string for the city
      │
      └──► create_daily_thought()    → Calls GPT-4o-mini internally to generate
                                        an inspirational thought
      │
      ▼
  Final response printed to terminal
```

The agent decides **which tool(s) to call** based on the user's message. It uses
the **ReAct** (Reason + Act) pattern internally via LangGraph.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: langchain.agents` has no `create_agent` | Apply the import fix in Step 5 |
| `No OPENAI_API_KEY found` | Check your `.env` file exists and has no typos |
| `AuthenticationError` from OpenAI | Your API key is invalid or has been revoked — regenerate it |
| `Usage: python dynamic_agent_input.py ...` printed | You forgot to pass a message argument — see Step 6 |

---

## Project Structure (Final)

```
my_agent/
├── dynamic_agent_input.py   # Main agent script
├── .env                     # Your secret API key (DO NOT SHARE)
├── requirements.txt         # Python dependencies
└── venv/                    # Virtual environment (auto-created, DO NOT SHARE)
```
