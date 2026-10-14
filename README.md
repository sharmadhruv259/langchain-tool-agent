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



Manual Agent Selecting-: [Screencast from 14-10-26 12:08:53 PM IST.webm](https://github.com/user-attachments/assets/53efea48-4596-4b2a-b56b-a1398ef0ab22)

Auto Agent Selecting-: [Screencast from 14-10-26 12:55:13 PM IST.webm](https://github.com/user-attachments/assets/bf04c8a6-ba3b-4453-ba5c-f28b6fc98cfe)

Final Project-: [Screencast from 14-10-26 01:39:54 PM IST.webm](https://github.com/user-attachments/assets/4ba634ed-82b9-48e5-be1f-a8fdcf65082d)
