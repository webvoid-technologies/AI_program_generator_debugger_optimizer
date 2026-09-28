def build_explain_prompt(code: str, language: str) -> tuple[str, str]:
    system_prompt = (
        "You are an expert computer science educator and software engineer. "
        "Your task is to explain source code in a clear, structured way. "
        "Return ONLY a valid JSON object with no markdown formatting, using the exact keys specified."
    )

    user_prompt = f"""Analyze and explain the following {language} code. Return a JSON object with exactly these keys:

{{
    "summary": "overall functionality of the program in 3-5 sentences",
    "functions": "description of each function, class, or major block, including parameters and return values",
    "line_by_line": "a concise line-by-line explanation of the most important logic",
    "io_complexity": "expected input/output formats and the time/space complexity if applicable"
}}

Code:
```{language}
{code}
```

Rules:
- Use plain text inside the JSON string values.
- Escape double quotes properly so the JSON is valid.
- Do not wrap the response in markdown code blocks.
"""

    return system_prompt, user_prompt
