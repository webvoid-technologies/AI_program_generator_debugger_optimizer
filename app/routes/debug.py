from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.prompts.debug_prompt import build_debug_prompt
from app.services.groq_service import call_groq

router = APIRouter()


class DebugRequest(BaseModel):
    code: str = Field(..., description="Buggy source code")
    language: str = Field(default="Python", description="Programming language of the code")
    error_message: str = Field(default="", description="Optional runtime or compile error message")


class DebugResponse(BaseModel):
    issues: str
    corrected_code: str
    suggestions: str


@router.post("/", response_model=DebugResponse)
async def debug_code(request: DebugRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    system_prompt, user_prompt = build_debug_prompt(request.code, request.language, request.error_message)
    response = await call_groq(system_prompt, user_prompt)
    return response
