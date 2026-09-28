def build_generate_prompt(requirement: str, language: str) -> tuple[str, str]:
    system_prompt = (
        "You are an expert software engineer and coding assistant. "
        "Your task is to generate clean, well-commented, production-ready source code based on a "
        "natural language requirement. Return ONLY a valid JSON object with no markdown formatting, "
        "using the exact keys specified. Do not include any explanation outside the JSON."
    )

    user_prompt = f"""Requirement: {requirement}

Target Language: {language}

Generate clean, well-commented {language} code that satisfies the requirement.
Return a JSON object in the following format:

{{
    "code": "the full source code as a single string with escaped newlines",
    "explanation": "a brief summary of what the code does, its main components, and how to run it"
}}

Rules:
- The code must be syntactically correct for {language}.
- Include meaningful inline comments and a docstring/header comment where appropriate.
- Prefer standard libraries and common idioms for the chosen language.
- Do not wrap the JSON in markdown code blocks.
"""

    return system_prompt, user_prompt
