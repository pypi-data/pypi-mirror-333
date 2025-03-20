from logging import Logger
from typing import Callable, Coroutine, final

from aiteamwork.callbacks.streaming import LLMStreamingContext
from aiteamwork.llm_message import LLMMessage


@final
class LLMToolFlowControl:
    _new_messages: list[LLMMessage]
    _state_changes: dict
    _requires_reprompt: bool
    _streaming_callback: Callable[[LLMStreamingContext], Coroutine[None, None, None]] | None
    _logger: Logger

    def __init__(
        self, streaming_callback: Callable[[LLMStreamingContext], Coroutine[None, None, None]] | None, logger: Logger
    ) -> None:
        self._new_messages = []
        self._state_changes = {}
        self._requires_reprompt = True
        self._streaming_callback = streaming_callback
        self._logger = logger

    @property
    def new_messages(self) -> list[LLMMessage]:
        return self._new_messages.copy()

    @property
    def should_reprompt(self) -> bool:
        return self._requires_reprompt

    def append_message(self, message: LLMMessage) -> "LLMToolFlowControl":
        self._new_messages.append(message)
        return self

    def skip_reprompt(self) -> "LLMToolFlowControl":
        self._requires_reprompt = False
        return self

    def request_reprompt(self) -> "LLMToolFlowControl":
        self._requires_reprompt = True
        return self

    def update_state(self, state_changes: dict) -> "LLMToolFlowControl":
        self._state_changes.update(state_changes)
        return self

    @property
    def state_changes(self) -> dict:
        return self._state_changes.copy()

    @property
    def has_state_changes(self) -> bool:
        return len(self._state_changes) > 0

    async def stream_back(
        self, piece: str, message_so_far: str = "", stream_type: str = "llm_tool", done: bool = False
    ) -> None:
        if self._streaming_callback is not None:
            try:
                await self._streaming_callback(
                    LLMStreamingContext(piece=piece, message_so_far=message_so_far, done=done, stream_type=stream_type)
                )
            except Exception as e:
                self._logger.error(f"Error in streaming tool data back: {e}")
                self._logger.exception(e)
