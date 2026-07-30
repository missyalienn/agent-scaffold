# Replace these stubs and schemas with real implementations for your use case.
#
# Note: sentiment-based escalation (e.g. angry customers) should be handled upstream
# of the agent loop via a dedicated classifier — not as a tool call. Tools are appropriate
# for issue-based routing where the agent reasons that a request is beyond its capabilities.


def escalate_to_human(reason: str) -> dict:
    """Signal that this request requires human intervention."""
    return {"escalated": True, "reason": reason}


def lookup_order(order_id: str) -> dict:
    return {
        "order_id": order_id,
        "status": "shipped",
        "item": "Wireless Headphones",
        "estimated_delivery": "2026-06-10",
    }


def search_knowledge_base(query: str) -> str:
    return (
        "Our return policy allows returns within 30 days of purchase with a valid receipt. "
        "Items must be in original condition. Refunds are processed within 5-7 business days."
    )


TOOL_SCHEMAS = [
    {
        "name": "escalate_to_human",
        "description": (
            "Escalate the conversation to a human agent when the request is beyond the agent's "
            "capabilities, requires authoritative judgment, or cannot be resolved with available tools."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "description": "A brief explanation of why escalation is needed.",
                },
            },
            "required": ["reason"],
        },
    },
    {
        "name": "lookup_order",
        "description": "Look up the status and details of a customer order by order ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The unique order identifier.",
                },
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "search_knowledge_base",
        "description": "Search the internal knowledge base for policy or product information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query or question.",
                },
            },
            "required": ["query"],
        },
    },
]
