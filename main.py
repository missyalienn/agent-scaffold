import logging

from dotenv import load_dotenv

from agent import Agent
from prompts import DEFAULT_SYSTEM_PROMPT
from tools import TOOL_SCHEMAS, lookup_order, search_knowledge_base

load_dotenv()
logging.basicConfig(level=logging.WARNING)

MODEL = "claude-sonnet-4-6"


def main() -> None:
    agent = Agent(model=MODEL, system_prompt=DEFAULT_SYSTEM_PROMPT, tools=TOOL_SCHEMAS)

    agent.register_tool("lookup_order", lookup_order)
    agent.register_tool("search_knowledge_base", search_knowledge_base)

    print("Agent ready. Type 'quit' or leave blank to exit.\n")
    while True:
        user_input = input("You: ").strip()
        if not user_input or user_input.lower() == "quit":
            break
        response = agent.run(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()
