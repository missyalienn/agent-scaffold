# Agent Scaffold — Notes & Learnings

## What this is
A minimal customer support agent built on the Anthropic SDK directly. No frameworks.
The scaffold is generic — swap the system prompt and tool functions for any use case.

## How the agentic loop works
1. User message → Anthropic API
2. Claude returns a `tool_use` block if it needs data
3. Your code executes the tool locally and sends the result back
4. Claude uses the result to form a plain-English response
5. Repeat until Claude returns `end_turn` with a text response

Claude decides *when* to call a tool and *what args* to pass. Execution always happens in your Python process. Same pattern applies to OpenAI function calling.

## Testing insights

### Happy path
"What is the status of order 12345?" — Claude correctly called `lookup_order` with the order ID and formatted the stub response. Two API calls total: one to get the tool call, one to get the final response.

### Ambiguous input
"I have a problem with my order" — Claude asked for clarification rather than hallucinating an order ID. The system prompt did the work here: telling Claude to look up order details before answering made it know it needed an ID first. Prompt-driven guardrailing, no extra code.

### No matching tool
"What's the weather in New York?" — Claude answered from training data and was transparent about what tools it actually has. It did not hallucinate a tool call. Default Claude behavior, no fallback code needed.

### Escalation (removed from scaffold)
Claude would not reliably escalate on angry messages — it kept trying to help instead. This is a known LLM behavior: models are trained to be helpful and default to "keep trying."

**Key insight:** Sentiment-based escalation should NOT be a tool call. Handle it upstream with a dedicated sentiment classifier before the message ever reaches the agent. Tools are appropriate for issue-based routing where the agent reasons that a request is beyond its capabilities (e.g. legal question, account compromise).

## Prompt tuning is fragile
Adjusting system prompt wording to change tool invocation behavior is hard to test and iterate on. The real answer is evals: structured input/expected-tool-call pairs you can run repeatedly. Without evals you're just vibes-testing in a REPL.

## Import gotcha
If you forget to import tool functions into `main.py`, you get a `NameError` at runtime — not at import time. It won't fail until the agent actually tries to register the tool. Keep this in mind when wiring up new tools quickly in an interview.

## Running interactively vs. piped input
Run with `python main.py` for interactive use. If you pipe input (`echo "..." | python main.py`) you'll see an `EOFError` and exit code 1 after the response — that's not a bug, just stdin closing. Ignore it.

## What this scaffold covers
- Agentic loop with tool calling (multi-turn, runs until `end_turn`)
- Conversation history maintained across turns within a session
- Tool registry pattern — clean separation between schema definitions and callables
- Max turns guard to prevent infinite loops
- System prompt config isolated in its own file
- API key loaded from `.env` via `python-dotenv`
- Basic logging setup

## Gaps / prod concerns to mention
- **No streaming** — blocks until full response. In prod you'd use `client.messages.stream()` for better UX.
- **No error handling** — no retry logic, no handling of rate limits or API timeouts.
- **No persistence** — conversation history lives in memory, dies when the process exits. No session resumption.
- **No async** — single-user synchronous loop. Multi-user would need `AsyncAnthropic` and `asyncio`.
- **No evals** — no structured tests asserting which tool gets called for a given input. Prompt changes are untestable without them.
- **No observability** — no logging of token usage, tool call decisions, or latency per turn.
- **No token counting** — long sessions will eventually hit context limits with no warning.
- **No cost tracking** — no visibility into how many tokens are being consumed per session.
- **Sentiment routing handled outside the agent** — mention that angry-user escalation belongs in a classifier layer upstream, not as a tool.

## Prompts to use with Claude mid-interview

### Adding a new tool
> "Add a new tool called `check_refund_status(order_id: str)` that returns a hardcoded refund status dict. Add the Anthropic tool schema to `TOOL_SCHEMAS`, import and register it in `main.py`."

### Adding async support
> "Refactor `agent.py` to use `AsyncAnthropic` and make the `run` method async. Update `main.py` to run the REPL loop with `asyncio.run(main())`."
