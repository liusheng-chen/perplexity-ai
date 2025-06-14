"""
Pydantic models for OpenAI Compatible API
"""
from typing import List, Dict, Any, Optional, Union, Literal
from pydantic import BaseModel, Field, field_validator
import time

class TextContent(BaseModel):
    """Text content part for multimodal messages"""
    type: Literal["text"] = Field(..., description="Content type")
    text: str = Field(..., description="Text content")

class ChatMessage(BaseModel):
    """Chat message model - supports both string and multimodal content"""
    role: Literal["system", "user", "assistant"] = Field(..., description="Role of the message sender")
    content: Union[str, List[TextContent]] = Field(..., description="Content of the message")

    @field_validator('content', mode='before')
    @classmethod
    def normalize_content(cls, v):
        """Convert multimodal content to simple string if needed"""
        if isinstance(v, list):
            # Extract text from multimodal content
            text_parts = []
            for item in v:
                if isinstance(item, dict) and item.get('type') == 'text':
                    text_parts.append(item.get('text', ''))
                elif isinstance(item, TextContent):
                    text_parts.append(item.text)
            return '\n'.join(text_parts)
        return v

class ChatCompletionRequest(BaseModel):
    """OpenAI Chat Completion Request model"""
    model: str = Field(..., description="Model to use for completion")
    messages: List[ChatMessage] = Field(..., description="List of messages in the conversation")
    max_tokens: Optional[int] = Field(None, description="Maximum number of tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    top_p: Optional[float] = Field(1.0, description="Nucleus sampling parameter")
    n: Optional[int] = Field(1, description="Number of completions to generate")
    stream: Optional[bool] = Field(False, description="Whether to stream the response")
    stop: Optional[Union[str, List[str]]] = Field(None, description="Stop sequences")
    presence_penalty: Optional[float] = Field(0.0, description="Presence penalty")
    frequency_penalty: Optional[float] = Field(0.0, description="Frequency penalty")
    user: Optional[str] = Field(None, description="User identifier")

class ChatCompletionChoice(BaseModel):
    """Chat completion choice model"""
    index: int = Field(..., description="Index of the choice")
    message: ChatMessage = Field(..., description="The generated message")
    finish_reason: Optional[str] = Field(None, description="Reason for finishing")

class ChatCompletionUsage(BaseModel):
    """Token usage information"""
    prompt_tokens: int = Field(..., description="Number of tokens in the prompt")
    completion_tokens: int = Field(..., description="Number of tokens in the completion")
    total_tokens: int = Field(..., description="Total number of tokens")

class ChatCompletionResponse(BaseModel):
    """OpenAI Chat Completion Response model"""
    id: str = Field(..., description="Unique identifier for the completion")
    object: str = Field("chat.completion", description="Object type")
    created: int = Field(default_factory=lambda: int(time.time()), description="Unix timestamp")
    model: str = Field(..., description="Model used for completion")
    choices: List[ChatCompletionChoice] = Field(..., description="List of completion choices")
    usage: Optional[ChatCompletionUsage] = Field(None, description="Token usage information")

class ChatCompletionStreamChoice(BaseModel):
    """Streaming chat completion choice model"""
    index: int = Field(..., description="Index of the choice")
    delta: Dict[str, Any] = Field(..., description="Delta containing new content")
    finish_reason: Optional[str] = Field(None, description="Reason for finishing")

class ChatCompletionStreamResponse(BaseModel):
    """Streaming chat completion response model"""
    id: str = Field(..., description="Unique identifier for the completion")
    object: str = Field("chat.completion.chunk", description="Object type")
    created: int = Field(default_factory=lambda: int(time.time()), description="Unix timestamp")
    model: str = Field(..., description="Model used for completion")
    choices: List[ChatCompletionStreamChoice] = Field(..., description="List of streaming choices")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: Dict[str, Any] = Field(..., description="Error information")

class ModelInfo(BaseModel):
    """Model information"""
    id: str = Field(..., description="Model identifier")
    object: str = Field("model", description="Object type")
    created: int = Field(default_factory=lambda: int(time.time()), description="Unix timestamp")
    owned_by: str = Field("perplexity", description="Organization that owns the model")

class ModelsResponse(BaseModel):
    """Models list response"""
    object: str = Field("list", description="Object type")
    data: List[ModelInfo] = Field(..., description="List of available models")
