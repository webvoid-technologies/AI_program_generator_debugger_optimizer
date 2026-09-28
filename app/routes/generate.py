from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.prompts.generate_prompt import build_generate_prompt
from app.services.groq_service import call_groq

router = APIRouter()


class GenerateRequest(BaseModel):
    requirement: str = Field(..., description="Natural language programming requirement")
    language: str = Field(default="Python", description="Target programming language")


class GenerateResponse(BaseModel):
    code: str
    explanation: str


@router.post("/", response_model=GenerateResponse)
async def generate_code(request: GenerateRequest):
    if not request.requirement.strip():
        raise HTTPException(status_code=400, detail="Requirement cannot be empty")

    system_prompt, user_prompt = build_generate_prompt(request.requirement, request.language)
    response = await call_groq(system_prompt, user_prompt)
    return response
