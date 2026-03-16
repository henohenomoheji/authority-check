import os
import time
from pathlib import Path

from .errors import (
    EmptyImageError,
    ImageTooLargeError,
    InvalidImageFormatError,
    InvalidPromptError,
)
from .logging_utils import log_event, new_request_id
from .model_client import VisionModelClient
from .schemas import InterpretationRequest, InterpretationResult

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
DEFAULT_MAX_IMAGE_SIZE_MB = 10
MAX_PROMPT_LENGTH = 2000
DEFAULT_PROMPT = "この画像の内容を日本語で簡潔に説明してください。"


def get_max_image_size_bytes() -> int:
    max_size_mb = int(os.getenv("MAX_IMAGE_SIZE_MB", str(DEFAULT_MAX_IMAGE_SIZE_MB)))
    return max_size_mb * 1024 * 1024


def validate_image(filename: str, size_bytes: int) -> None:
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise InvalidImageFormatError("対応外の画像形式です。")

    if size_bytes <= 0:
        raise EmptyImageError("画像が空です。")

    if size_bytes > get_max_image_size_bytes():
        raise ImageTooLargeError("画像サイズが上限を超えています。")


def build_prompt(user_prompt: str | None) -> str:
    if user_prompt is None or not user_prompt.strip():
        return DEFAULT_PROMPT
    if len(user_prompt) > MAX_PROMPT_LENGTH:
        raise InvalidPromptError(f"プロンプトは{MAX_PROMPT_LENGTH}文字以内で入力してください。")
    return user_prompt.strip()


def interpret_image(req: InterpretationRequest) -> InterpretationResult:
    validate_image(req.filename, len(req.image_bytes))
    prompt = build_prompt(req.instruction_prompt)

    request_id = new_request_id()
    start = time.perf_counter()
    model_client = VisionModelClient()

    log_event(
        request_id=request_id,
        event="image_interpretation.start",
        status="started",
        model_name=model_client.model_name,
    )

    try:
        description = model_client.generate_description(
            image_bytes=req.image_bytes,
            mime_type=req.mime_type,
            prompt=prompt,
        )
        latency_ms = int((time.perf_counter() - start) * 1000)
        log_event(
            request_id=request_id,
            event="image_interpretation.success",
            status="success",
            latency_ms=latency_ms,
            model_name=model_client.model_name,
        )
        return InterpretationResult(
            description_text=description,
            model_name=model_client.model_name,
            latency_ms=latency_ms,
            request_id=request_id,
        )
    except Exception as exc:
        latency_ms = int((time.perf_counter() - start) * 1000)
        log_event(
            request_id=request_id,
            event="image_interpretation.failure",
            status="failure",
            latency_ms=latency_ms,
            model_name=model_client.model_name,
            error_type=type(exc).__name__,
        )
        raise
