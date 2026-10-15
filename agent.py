"""Groq-powered multi-tool agent.

Terminal chat:  python agent.py
The API (api.py) imports build_agent() and run_agent() from this file.
"""

import os
import time
from typing import Iterator

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

from prompt import SYSTEM_PROMPT
from tools import ALL_TOOLS

load_dotenv()

MAX_TURNS = 10


def build_agent():
    """Create the Groq-powered agent with every registered tool.

    Raises:
        RuntimeError: If GROQ_API_KEY is missing.
    """
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("Missing GROQ_API_KEY.")

    model = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
    )

    return create_agent(
        model=model,
        tools=ALL_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        debug=False,
    )


def _text(content) -> str:
    """Message content can be a string or a list of content blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "".join(parts)
    return str(content)


def _trim(history: list) -> None:
    """Keep only the last MAX_TURNS user turns, cutting on a turn boundary."""
    human_idx = [i for i, m in enumerate(history) if m.type == "human"]
    if len(human_idx) > MAX_TURNS:
        del history[: human_idx[-MAX_TURNS]]


def run_agent(agent, message: str, history: list) -> Iterator[dict]:
    """Run one user message and yield simple event dicts as work happens.

    Events: tool_start, tool_result, answer. `history` is updated in place
    when the run finishes, so pass the same list to keep multi-turn memory.
    """
    new_messages = [HumanMessage(content=message)]
    started_at: dict[str, float] = {}

    for chunk in agent.stream(
        {"messages": history + new_messages}, stream_mode="updates"
    ):
        for update in chunk.values():
            for msg in (update or {}).get("messages", []):
                new_messages.append(msg)

                if msg.type == "ai":
                    for call in msg.tool_calls or []:
                        started_at[call["id"]] = time.perf_counter()
                        yield {
                            "type": "tool_start",
                            "id": call["id"],
                            "tool": call["name"],
                            "input": call["args"],
                        }
                    if not msg.tool_calls:
                        text = _text(msg.content)
                        if text:
                            yield {"type": "answer", "text": text}

                elif msg.type == "tool":
                    began = started_at.pop(msg.tool_call_id, time.perf_counter())
                    yield {
                        "type": "tool_result",
                        "id": msg.tool_call_id,
                        "tool": msg.name,
                        "result": _text(msg.content),
                        "duration_ms": int((time.perf_counter() - began) * 1000),
                    }

    history.extend(new_messages)
    _trim(history)


def main() -> None:
    """Run the interactive command-line agent.

    Args:
        None.

    Returns:
        None: Runs an interactive command-line agent.
    """
    try:
        agent = build_agent()
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return

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

            for event in run_agent(agent, user_input, []):
                if event["type"] == "tool_start":
                    print(f"\nTool selected: {event['tool']}")
                    print(f"Tool input: {event['input']}")
                elif event["type"] == "tool_result":
                    print(f"Tool result: {event['result']}")
                elif event["type"] == "answer":
                    final_answer = event["text"]

            print("\n--- Final Answer ---")
            print(final_answer)

        except Exception as exc:
            print(f"\nError: {exc}")


if __name__ == "__main__":
    main()