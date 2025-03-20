from typing import Callable

from pydantic import BaseModel, ConfigDict, Field

from aiteamwork.llm_context import LLMContext
from aiteamwork.llm_message import LLMMessage
from aiteamwork.llm_tool_function import LLMToolFunctionDefinition


class LLMToolsFactoryContext[RuntimeContextType: BaseModel](LLMContext[RuntimeContextType]):
    """Context for the tools factory callback in LLMAgent."""

    messages: list[LLMMessage] = Field()
    """A list of messages that have been sent to the agent."""


class LLMToolsFactoryResult(BaseModel):
    """Result of the tools factory callback in LLMAgent."""

    tools: list[Callable | LLMToolFunctionDefinition] = Field(default_factory=list)
    """A dictionary of tools and their respective versions."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
