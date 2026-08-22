from pydantic import BaseModel, Field, field_validator


SUPPORTED_MODELS = {
    "openai/gpt-oss-20b",
}


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    system_prompt: str | None = None
    model: str = "openai/gpt-oss-20b"
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=300, gt=0)
    history: list[ChatMessage] = Field(default_factory=list)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty.")

        return value

    @field_validator("model")
    @classmethod
    def validate_model(cls, value: str) -> str:
        if value not in SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model: {value}")

        return value


class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_used: int
    latency_ms: float