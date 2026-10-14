# LangChain Tool Agent

A tool-calling AI agent built using **LangChain and Groq** that can perform mathematical calculations, analyze text, and handle date-related operations using custom Python tools.

## 🚀 Features

This project demonstrates how to build an AI agent that selects and uses tools based on a user's input.

- **Math Calculator** — Performs mathematical calculations using safe AST-based expression evaluation.
- **Text Analyzer** — Analyzes text by calculating statistics such as word and character counts and providing sentiment-related analysis.
- **Date Utility** — Handles date-related operations and queries.
- **Tool Registry** — Organizes custom tools so the agent can access and use them.
- **LLM Integration** — Uses a Groq-hosted language model through LangChain.
- **Interactive Chat** — Accepts user input in the terminal and responds using the available tools.

## 🛠️ Tech Stack

- Python
- LangChain
- LangChain Groq
- Groq API
- Python-dotenv
- Abstract Syntax Trees (AST)

## 📁 Project Structure

```text
langchain-tool-agent/
│
├── agent.py          # Main agent and interactive execution
├── tools.py          # Custom tool definitions and tool registry
├── test_tools.py     # Tests for custom tools
├── .env              # API key configuration (not committed)
├── .gitignore        # Files excluded from Git
└── README.md         # Project documentation
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd langchain-tool-agent
```

Replace the placeholder with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install langchain langchain-groq python-dotenv
```

### 4. Configure your Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get an API key from the [Groq Console](https://console.groq.com/).

**Important:** Never upload your API key or `.env` file to GitHub.

### 5. Run the agent

```bash
python agent.py
```

The agent starts an interactive terminal session where you can enter prompts and observe how it responds using the available tools.

## 💡 Example Prompts

### Math Calculator

```text
Calculate (25 + 15) * 3.
```

```text
What is 144 divided by 12?
```

### Text Analyzer

```text
Analyze this text: LangChain makes it easier to build
applications powered by language models.
```

```text
Count the words and characters in this sentence:
Learning Python is useful.
```

### Date Utility

```text
What is today's date?
```

```text
Calculate the date 30 days from today.
```

### Multiple Tools

```text
Calculate 125 * 8, then analyze the sentence
"Building AI agents is interesting" and tell me today's date.
```

The model determines which available tools are appropriate for each request.

## 🧪 Testing

Run the tool tests with:

```bash
python -m pytest test_tools.py
```

If `pytest` is not installed, install it first:

```bash
pip install pytest
```

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key used to authenticate with Groq |

Keep `.env` excluded from version control using `.gitignore`.

## 🧠 How It Works

1. The user enters a prompt in the terminal.
2. The LangChain agent receives the prompt.
3. The language model determines whether a custom tool is needed.
4. The appropriate tool executes its Python logic.
5. The tool result is returned to the agent.
6. The agent generates a response for the user.

```text
User Prompt
    |
    v
LangChain Agent
    |
    v
Groq Language Model
    |
    v
Tool Selection
    |
    +----> Math Calculator
    |
    +----> Text Analyzer
    |
    +----> Date Utility
    |
    v
Tool Result
    |
    v
Final Response
```

## 🎯 Learning Objectives

This project demonstrates:

- Creating custom tools in LangChain.
- Using tool descriptions and function docstrings.
- Integrating a language model through Groq.
- Configuring API
