import base64
import json
import os
import socket
from urllib import error, request

from .errors import MissingConfigurationError, ModelTimeoutError, ModelUnavailableError

DEFAULT_TIMEOUT_SEC = 10


class VisionModelClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("VISION_API_KEY")
        self.model_name = os.getenv("VISION_MODEL_NAME")
        self.timeout_sec = int(os.getenv("VISION_TIMEOUT_SEC", str(DEFAULT_TIMEOUT_SEC)))

        if not self.api_key:
            raise MissingConfigurationError("VISION_API_KEY が設定されていません。")
        if not self.model_name:
            raise MissingConfigurationError("VISION_MODEL_NAME が設定されていません。")

    def generate_description(self, image_bytes: bytes, mime_type: str, prompt: str) -> str:
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "model": self.model_name,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:{mime_type};base64,{image_b64}",
                        },
                    ],
                }
            ],
        }

        req = request.Request(
            url="https://api.openai.com/v1/responses",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout_sec) as response:
                body = response.read().decode("utf-8")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise ModelUnavailableError(f"モデルAPIエラー: status={exc.code}, detail={detail}") from exc
        except (error.URLError, TimeoutError, socket.timeout) as exc:
            raise ModelTimeoutError("モデルAPI呼び出しがタイムアウトしました。") from exc

        parsed = json.loads(body)
        output_text = parsed.get("output_text")
        if output_text:
            return output_text.strip()

        output = parsed.get("output", [])
        for item in output:
            for content in item.get("content", []):
                if content.get("type") == "output_text" and content.get("text"):
                    return str(content["text"]).strip()

        raise ModelUnavailableError("モデルAPIのレスポンスに説明文が含まれていません。")
