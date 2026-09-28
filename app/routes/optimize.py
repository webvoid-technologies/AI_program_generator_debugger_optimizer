from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.prompts.optimize_prompt import build_optimize_prompt
from app.services.groq_service import call_groq

router = APIRouter()


class OptimizeRequest(BaseModel):
    code: str = Field(..., description="Source code to optimize")
    language: str = Field(default="Python", description="Programming language of the code")


class OptimizeResponse(BaseModel):
    optimized_code: str
    improvements: str


@router.post("/", response_model=OptimizeResponse)
async def optimize_code(request: OptimizeRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    system_prompt, user_prompt = build_optimize_prompt(request.code, request.language)
    response = await call_groq(system_prompt, user_prompt)
    return response
