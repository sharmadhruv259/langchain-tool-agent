
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from tools import (
    math_tool,
    text_analyzer_tool,
    date_tool,
    weather_tool,
)


def main() -> None:
    """Run the Groq-powered multi-tool agent.

    Args:
        None.

    Returns:
        None: Runs an interactive command-line agent.
    """
    load_dotenv()

    if not os.getenv("GROQ_API_KEY"):
        print("Error: Missing GROQ_API_KEY.")
        return

    model = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
    )

    tools = [
        math_tool,
        text_analyzer_tool,
        date_tool,
        weather_tool,
    ]

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=(
            "You are a helpful assistant that can use multiple tools "
            "in sequence to complete a request. "
            "Use math_tool for calculations, date_tool for date calculations, "
            "text_analyzer_tool for text analysis, and weather_tool for "
            "current weather information and clothing suggestions. "
            "When weather information is requested, call weather_tool "
            "for the requested city and base your answer on its actual result. "
            "Use the actual tool results in your final answer."
        ),
        debug=False,
    )

    print("Groq Multi-Tool Agent is ready!")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ").strip()

        # Stop before calling the agent.
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            print("\n--- Agent Execution Log ---")
            final_answer = ""

            for chunk in agent.stream(
                {
                    "messages": [
                        {"role": "user", "content": user_input}
                    ]
                },
                stream_mode="updates",
            ):
                for node, update in chunk.items():
                    for message in update.get("messages", []):
                        tool_calls = getattr(message, "tool_calls", [])

                        if tool_calls:
                            for call in tool_calls:
                                print(f"\nTool selected: {call['name']}")
                                print(f"Tool input: {call['args']}")

                        elif message.__class__.__name__ == "ToolMessage":
                            print(f"Tool result: {message.content}")

                        elif (
                            message.__class__.__name__ == "AIMessage"
                            and message.content
                        ):
                            final_answer = message.content

            print("\n--- Final Answer ---")
            print(final_answer)

        except Exception as exc:
            print(f"\nError: {exc}")


if __name__ == "__main__":
    main()
