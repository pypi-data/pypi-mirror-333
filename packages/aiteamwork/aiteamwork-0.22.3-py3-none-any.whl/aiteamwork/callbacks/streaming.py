from pydantic import BaseModel, Field


class LLMStreamingContext(BaseModel):
    piece: str = Field(description=("The piece of data received. This is the piece of data that was received."))
    """The piece of data received. This is the piece of data that was received."""

    message_so_far: str = Field(
        description=("The message so far. Should be a combination of all the pieces received so far.")
    )
    """The message so far. Should be a combination of all the pieces received so far."""

    done: bool = Field(
        description=(
            "Whether the stream is done or not. "
            "This is used to determine if the stream is done "
            "or if there is more data to come."
        )
    )
    """Whether the stream is done or not.
    This is used to determine if the stream is done or if there is more data to come."""

    stream_type: str = Field(
        description=(
            "The type of the stream. "
            "This is used to determine the type of the stream. "
            "i.e: llm_response for response streams, or custom strings for data coming from tools."
        )
    )
    """The type of the stream. This is used to determine the type of the stream.
    i.e: llm_response for response streams, or custom strings for data coming from tools."""

    @property
    def is_from_llm(self) -> bool:
        return self.stream_type == "llm_response"
