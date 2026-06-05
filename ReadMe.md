# 🤖 LangChain Agent with Gmail Integration

An AI-powered agent built using **LangChain**, **OpenAI**, and **Gmail API** that can dynamically invoke tools based on user requests.

---

## 🚀 Features

### 🌤️ Weather Tool

Retrieve weather information for a specified city.

**Example**

```bash
What is the weather in Hyderabad?
```

---

### 📰 Post Retrieval Tool

Fetch post details from JSONPlaceholder using a Post ID.

**Example**

```bash
Get post 20
```

API:

```text
https://jsonplaceholder.typicode.com/posts/{id}
```

---

### 💡 Daily Motivational Thought generator

Uses OpenAI to generate a short motivational thought.

**Example**

```bash
Generate today's thought
```

---

### 📧 Gmail Subject Retrieval Tool

Connects securely to Gmail using OAuth 2.0 and retrieves the latest email subjects from the user's Primary Inbox.

**Example**

```bash
Show my latest 2 email subjects
```

---

## 🏗️ Architecture

```text
                 ┌─────────────┐
                 │    User     │
                 └──────┬──────┘
                        │
                        ▼
              ┌──────────────────┐
              │ LangChain Agent  │
              └────────┬─────────┘
                       │
                       ▼
               ┌─────────────┐
               │ OpenAI LLM  │
               └──────┬──────┘
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼

🌤️ Weather     📰 Posts      📧 Gmail Tool

      │               │                │
      ▼               ▼                ▼

 External API   JSONPlaceholder   Gmail API

                      │
                      ▼

              Final AI Response
```

---

## 🛠️ Tech Stack

| Technology       | Purpose                   |
| ---------------- | ------------------------- |
| 🐍 Python        | Core Programming Language |
| 🦜 LangChain     | Agent Framework           |
| 🕸️ LangGraph    | Agent Execution Engine    |
| 🤖 OpenAI API    | LLM Integration           |
| 📧 Gmail API     | Email Retrieval           |
| 🔐 OAuth 2.0     | Authentication            |
| 🌐 Requests      | HTTP Requests             |
| ⚙️ Python Dotenv | Environment Variables     |

---

## 📦 Installation

Install required packages:

```bash
pip install langchain
pip install langchain-openai
pip install langgraph
pip install python-dotenv
pip install requests
pip install google-api-python-client
pip install google-auth-oauthlib
pip install google-auth-httplib2
```

---

## 🔑 Environment Setup

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## 📧 Gmail API Setup

### Step 1

Create a Google Cloud Project.

### Step 2

Enable Gmail API.

### Step 3

Configure OAuth Consent Screen.

### Step 4

Create OAuth Client ID.

Select:

```text
Desktop Application
```

### Step 5

Download credentials file.

Rename to:

```text
credentials.json
```

Project Structure:

```text
project/
│
├── dynamic_agent_input.py
├── credentials.json
├── .env
├── token.json
└── README.md
```

---

## 🔐 Authentication Flow

```text
User
 ↓
Google Login
 ↓
OAuth Consent
 ↓
Access Granted
 ↓
token.json Generated
 ↓
Gmail API Access
```

First run requires login.

Subsequent runs use the stored token.

---

## ▶️ Running the Agent

### Fetch Post

```bash
python dynamic_agent_input.py "Get post 20"
```

### Generate Thought

```bash
python dynamic_agent_input.py "Generate a daily thought"
```

### Gmail Subjects

```bash
python dynamic_agent_input.py "Show my latest email subjects"
```

---

## 📊 Agent Execution Flow

```text
User Query
     ↓
LangChain Agent
     ↓
OpenAI Model
     ↓
Tool Selection
     ↓
Tool Execution
     ↓
External API
     ↓
Tool Result
     ↓
LLM Formatting
     ↓
Final Response
```

---

## ⚠️ Security Best Practices

Never commit:

```text
credentials.json
token.json
.env
```

Add to `.gitignore`:

```gitignore
credentials.json
token.json
.env
__pycache__/
venv/
```

---

## 📚 Concepts Demonstrated

✅ Tool Calling

✅ Agent Architecture

✅ OAuth 2.0 Authentication

✅ Gmail API Integration

✅ OpenAI Integration

✅ External API Consumption

✅ Dynamic Workflow Execution

✅ LangChain Agent Development

---

## 🎯 Future Enhancements

* 📩 Email Summarization
* ✉️ Email Draft Generation
* 📅 Calendar Integration
* 🌦️ Real Weather API Integration
* 🗄️ Database Connectivity
* 🔎 Multi-Tool Agent Workflows

---

## 👨‍💻 Author

**Sathvik Chekkali**

Built for learning Agentic AI, LangChain, Tool Calling, and External API Integration.
