# agent-scaffold
Minimal reusable Python agent scaffold using the Anthropic SDK directly.
No frameworks. No LangChain. Python 3.11+. Venv already active.

## Stack
- anthropic SDK
- python-dotenv

## Structure
- agent.py — core agentic loop
- tools.py — tool definitions and registry
- prompts.py — system prompt config
- main.py — CLI entrypoint
