from typing import List

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    error: str
    code: str


class Environment(BaseModel):
    working_directory: str
    platform: str


class AgentCompletionRequest(BaseModel):
    model: str = Field(
        default="claude-3-7-sonnet-latest", description="The Claude model to use"
    )
    persona: str = Field(default="coder", description="The persona to use")
    environment: Environment = Field(..., description="The environment")
    messages: List[dict] = Field(..., description="The messages to send to the agent")


class AgentCompletionResponse(BaseModel):
    messages: List[BaseMessage]
