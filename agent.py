import anthropic
import logging

logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, model: str, system_prompt: str, tools: list[dict]) -> None:
        self.client = anthropic.Anthropic()
        self.model = model
        self.system_prompt = system_prompt
        self.tools = tools
        self.tool_registry: dict[str, callable] = {}
        self.conversation_history: list[dict] = []

    def register_tool(self, name: str, fn: callable) -> None:
        self.tool_registry[name] = fn

    def run(self, user_message: str, max_turns: int = 10) -> str:
        self.conversation_history.append({"role": "user", "content": user_message})
        turns = 0

        while turns < max_turns:
            response = self.client.messages.create(
                model=self.model,
                system=self.system_prompt,
                tools=self.tools,
                messages=self.conversation_history,
                max_tokens=4096,
            )
            logger.debug("Response stop_reason: %s", response.stop_reason)

            if response.stop_reason == "end_turn":
                text = next(b.text for b in response.content if b.type == "text")
                self.conversation_history.append({"role": "assistant", "content": text})
                return text

            # tool_use stop: execute each tool and feed results back
            self.conversation_history.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                fn = self.tool_registry.get(block.name)
                if fn is None:
                    raise ValueError(f"No tool registered for '{block.name}'")
                logger.debug("Calling tool '%s' with input %s", block.name, block.input)
                result = fn(**block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })

            self.conversation_history.append({"role": "user", "content": tool_results})
            turns += 1

        raise RuntimeError(f"Agent exceeded max_turns ({max_turns}) without reaching end_turn.")
