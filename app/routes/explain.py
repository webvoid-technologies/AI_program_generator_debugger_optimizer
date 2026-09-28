from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.prompts.explain_prompt import build_explain_prompt
from app.services.groq_service import call_groq

router = APIRouter()


class ExplainRequest(BaseModel):
    code: str = Field(..., description="Source code to explain")
    language: str = Field(default="Python", description="Programming language of the code")


class ExplainResponse(BaseModel):
    summary: str
    functions: str
    line_by_line: str
    io_complexity: str


@router.post("/", response_model=ExplainResponse)
async def explain_code(request: ExplainRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    system_prompt, user_prompt = build_explain_prompt(request.code, request.language)
    response = await call_groq(system_prompt, user_prompt)
    return response
