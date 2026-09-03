from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    application: str
    version: str


class CalculatorRequest(BaseModel):
    operation: str = Field(
        ...,
        description="add, subtract, multiply or divide",
    )

    num1: float
    num2: float


class CalculatorResponse(BaseModel):
    operation: str
    num1: float
    num2: float
    result: float


class RAGRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
    )

    provider: str = "Gemini"

    retrieval_method: str = "similarity"

    top_k: int = Field(
        default=4,
        ge=1,
        le=10,
    )


class RAGResponse(BaseModel):
    question: str
    answer: str
    sources: List[Dict[str, Any]] = []


class AgentRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
    )


class AgentResponse(BaseModel):
    question: str
    answer: str
    status: str
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None