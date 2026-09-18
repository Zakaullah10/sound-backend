from contextvars import ContextVar

refreshed_tokens_ctx: ContextVar[dict | None] = ContextVar(
    "refreshed_tokens",
    default=None,
)
