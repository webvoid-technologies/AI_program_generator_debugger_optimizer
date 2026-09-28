def build_optimize_prompt(code: str, language: str) -> tuple[str, str]:
    system_prompt = (
        "You are an expert code optimizer and software engineer. "
        "Your task is to improve existing code for readability, structure, and efficiency. "
        "Return ONLY a valid JSON object with no markdown formatting, using the exact keys specified."
    )

    user_prompt = f"""Optimize the following {language} code. Return a JSON object with exactly these keys:

{{
    "optimized_code": "the improved source code as a single string with escaped newlines",
    "improvements": "a detailed list of optimizations made, including readability, structure, algorithmic improvements, and complexity changes"
}}

Code:
```{language}
{code}
```

Rules:
- Preserve the original functionality and public interface where possible.
- Improve naming, reduce redundancy, and choose better algorithms/data structures when applicable.
- Add comments explaining non-trivial optimizations.
- Return valid JSON; escape newlines and double quotes properly.
- Do not wrap the response in markdown code blocks.
"""

    return system_prompt, user_prompt
