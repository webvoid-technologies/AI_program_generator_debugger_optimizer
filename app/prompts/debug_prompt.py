def build_debug_prompt(code: str, language: str, error_message: str = "") -> tuple[str, str]:
    system_prompt = (
        "You are an expert debugger and software engineer. "
        "Your task is to find syntax, logical, and runtime errors in source code and provide a corrected version. "
        "Return ONLY a valid JSON object with no markdown formatting, using the exact keys specified."
    )

    error_context = f"\nReported Error/Message:\n{error_message}\n" if error_message.strip() else ""

    user_prompt = f"""Debug the following {language} code and return a JSON object with exactly these keys:

{{
    "issues": "list each identified issue with a clear explanation",
    "corrected_code": "the full corrected source code as a single string with escaped newlines",
    "suggestions": "practical debugging tips and best practices to avoid similar issues"
}}

Code:
```{language}
{code}
```{error_context}

Rules:
- If no obvious errors exist, improve clarity and robustness and explain what you changed.
- Include meaningful comments in the corrected code.
- Return valid JSON; escape newlines and double quotes properly.
- Do not wrap the response in markdown code blocks.
"""

    return system_prompt, user_prompt
