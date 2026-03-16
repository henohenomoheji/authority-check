from dataclasses import dataclass


@dataclass(slots=True)
class InterpretationRequest:
    image_bytes: bytes
    filename: str
    mime_type: str
    instruction_prompt: str | None


@dataclass(slots=True)
class InterpretationResult:
    description_text: str
    model_name: str
    latency_ms: int
    request_id: str
