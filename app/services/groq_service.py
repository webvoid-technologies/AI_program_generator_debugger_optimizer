import json
import os
from typing import Any, Dict, Tuple

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-oss-120b"


async def call_groq(system_prompt: str, user_prompt: str) -> Dict[str, Any]:
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is not configured")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": os.getenv("GROQ_MODEL", DEFAULT_MODEL),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 4096,
        "response_format": {"type": "json_object"},
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(GROQ_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Groq API error: {exc.response.text}",
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Groq API request failed: {str(exc)}")

    try:
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return parsed
    except (KeyError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=502, detail=f"Invalid response from Groq API: {str(exc)}")
