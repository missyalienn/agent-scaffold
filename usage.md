# Usage — Interview Quickstart

## Before the interview (do this once)
- [ ] Python 3.11+ installed
- [ ] Anthropic API key in `.env`
- [ ] Venv created, deps installed, `python main.py` runs clean

```bash
cd agent-scaffold
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# paste your ANTHROPIC_API_KEY into .env
python main.py  # confirm it runs
```

## In the interview
You are NOT cloning anything. This repo is already on your machine. When they give you the use case:

**1. `prompts.py`** — replace `DEFAULT_SYSTEM_PROMPT` with a persona and instructions that fit the problem. There is an example customer support prompt commented out at the bottom.

**2. `tools.py`** — rename/replace the stub functions with tools that make sense for the use case. Update `TOOL_SCHEMAS` to match. The `name` field in each schema must exactly match the function name.

**3. `main.py`** — update the imports and `register_tool` calls to match your new tools.

Then run it and demo a happy path:
```bash
python main.py
```

`agent.py` stays untouched for most problems.

## Model
Set in `main.py` via the `MODEL` constant. Default is `claude-sonnet-4-6`. Swap to `claude-haiku-4-5-20251001` if you need faster/cheaper during a demo.

## Things to keep in mind
- Tool `name` in `TOOL_SCHEMAS` must exactly match what you pass to `register_tool()` — mismatch only surfaces at runtime on a tool call, not at startup.
- `conversation_history` persists across `agent.run()` calls in the same session — the agent remembers prior turns.
- Sentiment-based escalation should not be a tool. If the problem requires routing angry users to a human, say you'd handle that upstream with a classifier, not inside the agent loop.
