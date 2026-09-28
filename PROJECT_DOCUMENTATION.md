<p align="center">
  <img src="https://www.webvoidtechnologies.com/webvoid_logo_tm.png" alt="Webvoid Technologies" width="220">
</p>

<h1 align="center">AI Program Generator, Debugger & Optimizer</h1>

<p align="center">
  <b>Project Documentation</b><br>
  Final Year CSE Project — FastAPI Proof of Concept
</p>

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Problem Statement](#3-problem-statement)
4. [Objectives](#4-objectives)
5. [Scope of the Project](#5-scope-of-the-project)
6. [System Requirements](#6-system-requirements)
7. [Technology Stack](#7-technology-stack)
8. [System Architecture](#8-system-architecture)
9. [Project Structure](#9-project-structure)
10. [Module Descriptions](#10-module-descriptions)
11. [Backend Design](#11-backend-design)
12. [Frontend Design](#12-frontend-design)
13. [API Documentation](#13-api-documentation)
14. [Prompt Engineering](#14-prompt-engineering)
15. [Data Flow](#15-data-flow)
16. [Setup & Installation](#16-setup--installation)
17. [Usage Guide](#17-usage-guide)
18. [Testing & Verification](#18-testing--verification)
19. [Limitations](#19-limitations)
20. [Future Enhancements](#20-future-enhancements)
21. [Conclusion](#21-conclusion)
22. [References](#22-references)

---

## 1. Abstract

Software development demands significant time, expertise, and iterative effort — from translating requirements into code, to understanding unfamiliar codebases, to debugging errors, to optimizing for performance. This project presents the **AI Program Generator, Debugger & Optimizer**, an intelligent coding assistant that automates all four tasks through a single web dashboard.

Users describe what they want in plain English — or paste existing source code — and the system leverages a Large Language Model (LLM) served through the Groq inference API to generate clean code, produce multi-level explanations, identify and repair bugs, and refactor for efficiency.

The entire application is built on a minimal, stateless FastAPI stack: Python backend, Jinja2 server-side rendering, Tailwind CSS, Vanilla JavaScript, and the Monaco Editor (the editor engine behind VS Code). No database, no authentication, and no frontend framework — demonstrating that a production-quality AI tool can be delivered with remarkably few moving parts.

## 2. Introduction

Large Language Models have demonstrated strong capabilities in code understanding and code generation. However, most AI coding tools are either heavyweight IDE plugins or complex cloud services. This project explores a third path: a lightweight, self-hosted web application that exposes four distinct AI capabilities through a clean, professional interface.

The system is designed as a **Proof of Concept (POC)** suitable for academic demonstration. It showcases:

- **Full-stack engineering** — backend API design, prompt engineering, async HTTP, and frontend state management.
- **LLM integration patterns** — structured JSON output contracts, per-task system personas, and error handling.
- **Real-world utility** — every module addresses a genuine developer workflow.

## 3. Problem Statement

Students and developers frequently face the following challenges:

1. Translating a requirement described in natural language into working code requires domain knowledge and time.
2. Understanding unfamiliar code (e.g., during code review or learning) is cognitively demanding.
3. Debugging requires locating the defect, understanding why it occurs, and producing a correct fix.
4. Optimizing working code for readability and efficiency requires experience with idioms and algorithms.

Existing solutions either require paid subscriptions, complex setup, or heavyweight IDEs. **This project provides a free, lightweight, browser-based alternative powered by fast LLM inference.**

## 4. Objectives

- Accept natural language programming requirements and generate syntactically correct, well-commented source code.
- Support six target languages: **Python, Java, C, C++, JavaScript, SQL**.
- Explain source code at three levels: overall summary, per-function/class, and line-by-line.
- Detect and repair syntax, logical, and runtime errors with human-readable explanations.
- Optimize code for readability, structure, and algorithmic efficiency.
- Return all results in a consistent structured JSON format.
- Deliver a professional single-page dashboard with a modern code editor.
- Keep the architecture stateless — no database, no authentication, minimal dependencies.

## 5. Scope of the Project

### In Scope

- Web-based dashboard accessible at `localhost` after setup.
- Four AI modules: Generate, Explain, Debug, Optimize.
- Groq API integration with structured JSON responses.
- Monaco Editor for code input and output display.
- Multi-language support (6 languages).

### Out of Scope (Deliberately Excluded)

- No database — the application is fully stateless.
- No authentication or user accounts.
- No code execution/sandboxing (e.g., Judge0) — code is generated but not run.
- No React or other frontend frameworks — Vanilla JS only.
- No persistent history between sessions.

## 6. System Requirements

### Software

| Component | Requirement |
| --------- | ----------- |
| Operating System | Windows / macOS / Linux |
| Python | 3.9 or higher |
| Browser | Any modern browser (Chrome, Edge, Firefox, Safari) |
| Internet | Required (Groq API + CDN assets) |

### Python Dependencies

| Package | Version | Purpose |
| ------- | ------- | ------- |
| `fastapi` | 0.115.0 | Web framework |
| `uvicorn[standard]` | 0.30.0 | ASGI server with hot reload |
| `pydantic` | 2.9.0 | Request/response validation |
| `httpx` | 0.27.2 | Async HTTP client for Groq API |
| `python-dotenv` | 1.0.1 | `.env` file loading |
| `jinja2` | 3.1.4 | Server-side HTML templating |

### External Services

| Service | Usage |
| ------- | ----- |
| Groq API | LLM inference (`openai/gpt-oss-120b` default) |
| Tailwind CSS CDN | UI styling |
| Monaco Editor CDN | Code editor component |

### API Key

A Groq API key is required. Create one free at [console.groq.com/keys](https://console.groq.com/keys).

## 7. Technology Stack

| Layer | Technology | Rationale |
| ----- | ---------- | --------- |
| Backend | **FastAPI** | Async-native, automatic validation via Pydantic, OpenAPI docs at `/docs` |
| Server | **Uvicorn** | Lightweight ASGI server; `--reload` for development |
| HTTP client | **httpx** | Async non-blocking calls to Groq |
| Templating | **Jinja2** | Server-rendered HTML, keeps frontend decoupled |
| Styling | **Tailwind CSS** | Utility-first, responsive, zero build step via CDN |
| Scripting | **Vanilla JavaScript** | No framework overhead; direct Fetch API calls |
| Editor | **Monaco Editor** | VS Code-grade editor with syntax highlighting for all 6 languages |
| AI | **Groq API** | OpenAI-compatible chat completions with very low latency |
| Config | **python-dotenv** | Secrets kept out of source code |

## 8. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                             │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │  Sidebar   │  │ Monaco Editor│  │ Output Panel + Toasts│  │
│  └────────────┘  └──────────────┘  └─────────────────────┘  │
│         └────── Vanilla JS (app.js) + Fetch API ──────┘      │
└───────────────────────────┬─────────────────────────────────┘
                            │  JSON over HTTP
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                      │
│                                                             │
│   main.py ── mounts static/, templates/, registers routers  │
│                                                             │
│   routes/         services/           prompts/              │
│   ├─ generate.py  ├─ groq_service.py  ├─ generate_prompt.py │
│   ├─ explain.py   └─ async httpx ───► ├─ explain_prompt.py  │
│   ├─ debug.py        Groq API         ├─ debug_prompt.py    │
│   └─ optimize.py                      └─ optimize_prompt.py │
└───────────────────────────┬─────────────────────────────────┘
                            │  POST /openai/v1/chat/completions
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 Groq Inference API (LLM)                    │
└─────────────────────────────────────────────────────────────┘
```

**Design principles:**

- **Thin routes** — each route validates input (Pydantic), builds a prompt, calls the service, returns the response. No business logic in routes.
- **Single AI gateway** — `groq_service.py` is the only file that talks to Groq. One place to change models, temperature, retries.
- **Prompt isolation** — prompt text lives in `prompts/`, separate from HTTP logic. Prompts can be tuned without touching routes.
- **Structured contract** — every AI response is forced into a documented JSON shape via `response_format: {"type": "json_object"}`.

## 9. Project Structure

```
AI_CODE_GENERATOR/
├── app/
│   ├── __init__.py
│   ├── main.py                  # App factory, static mount, route registration, GET /
│   │
│   ├── routes/                  # HTTP layer — one file per module
│   │   ├── __init__.py
│   │   ├── generate.py          # POST /generate/
│   │   ├── explain.py           # POST /explain/
│   │   ├── debug.py             # POST /debug/
│   │   └── optimize.py          # POST /optimize/
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── groq_service.py      # Async Groq client; loads .env; parses JSON output
│   │
│   ├── prompts/                 # Prompt builders — one file per module
│   │   ├── __init__.py
│   │   ├── generate_prompt.py
│   │   ├── explain_prompt.py
│   │   ├── debug_prompt.py
│   │   └── optimize_prompt.py
│   │
│   ├── templates/
│   │   └── index.html           # Single-page dashboard (Jinja2 + Tailwind + Monaco CDN)
│   │
│   └── static/
│       ├── css/
│       │   └── style.css        # Scrollbars, toast animations, output formatting
│       └── js/
│           └── app.js           # Monaco init, module switching, Fetch calls, toasts
│
├── .env                         # Secrets (GROQ_API_KEY) — never commit
├── .env.example                 # Environment variable template
├── requirements.txt             # Pinned Python dependencies
├── README.md                    # Quick-start setup guide
└── PROJECT_DOCUMENTATION.md     # This document
```

## 10. Module Descriptions

### 10.1 AI Program Generator

**Purpose:** Convert a natural language requirement into complete, runnable source code.

**Input:** Requirement text + target language.
**Output:** `code` (full source, commented) + `explanation` (component summary, run instructions).

**Example:**

> Requirement: *"a function to check if a number is prime"*, Language: *Python*
> Output: a complete `is_prime()` implementation with input validation, edge-case handling (`n < 2`, `n == 2`), a √n trial-division loop, and a `__main__` demo block.

### 10.2 AI Code Explainer

**Purpose:** Help users understand unfamiliar code at multiple levels of detail.

**Input:** Source code + language.
**Output fields:**

| Field | Content |
| ----- | ------- |
| `summary` | Overall functionality in 3–5 sentences |
| `functions` | Each function/class with parameters and return values |
| `line_by_line` | Walkthrough of the important logic |
| `io_complexity` | Input/output formats + time & space complexity |

### 10.3 AI Debugger

**Purpose:** Find and fix defects; explain *why* each fix works.

**Input:** Buggy code + language + optional error message.
**Output fields:**

| Field | Content |
| ----- | ------- |
| `issues` | Every identified syntax/logical/runtime problem, explained |
| `corrected_code` | Full fixed source, loaded back into the editor |
| `suggestions` | Debugging tips and best practices to avoid recurrence |

**Graceful fallback:** if no bugs exist, the prompt instructs the model to improve clarity and explain its changes — the endpoint always returns useful output.

### 10.4 AI Code Optimizer

**Purpose:** Improve readability, structure, and efficiency while preserving behavior.

**Input:** Source code + language.
**Output fields:**

| Field | Content |
| ----- | ------- |
| `optimized_code` | Refactored source with comments explaining non-trivial changes |
| `improvements` | List of optimizations: naming, redundancy removal, better algorithms/data structures, complexity changes |

**Example:**

> `def f(l): r=[]; for i in l: r.append(i*2); return r` → `return [i * 2 for i in l]` — documented as a comprehension refactor (O(n) preserved, readability improved).

## 11. Backend Design

### 11.1 Application Entry Point — `app/main.py`

- Loads `.env` via `python-dotenv`.
- Creates the `FastAPI` app with title/description metadata (visible at `/docs`).
- Mounts `app/static` at `/static` for CSS/JS.
- Configures `Jinja2Templates` pointing at `app/templates`.
- Registers four routers under `/generate`, `/explain`, `/debug`, `/optimize`.
- `GET /` renders `index.html`.

### 11.2 Route Layer — `app/routes/*.py`

Each route module follows an identical pattern:

```python
class XRequest(BaseModel):    # input validation schema
class XResponse(BaseModel):   # output contract

@router.post("/")
async def handler(request: XRequest):
    # 1. reject empty input → HTTP 400
    # 2. build (system_prompt, user_prompt) via app/prompts/
    # 3. await call_groq(system, user)
    # 4. return parsed JSON dict → validated against XResponse
```

### 11.3 Service Layer — `app/services/groq_service.py`

- `load_dotenv()` called at module level; API key read **lazily inside the function** (avoids import-order pitfalls where env vars load after module constants are bound).
- Posts to `https://api.groq.com/openai/v1/chat/completions` via `httpx.AsyncClient` with a 60 s timeout.
- Payload: `model` (env-overridable `GROQ_MODEL`, default `openai/gpt-oss-120b`), `temperature: 0.2`, `max_tokens: 4096`, `response_format: {"type": "json_object"}`.
- Error mapping:

| Condition | HTTP status |
| --------- | ----------- |
| Missing `GROQ_API_KEY` | 500 |
| Groq HTTP error | Groq's status, message forwarded |
| Network failure | 503 |
| Malformed JSON from model | 502 |

## 12. Frontend Design

### 12.1 Layout

```
┌──────────┬──────────────────────────────────────────────┐
│          │  Header: module title + language dropdown     │
│ Sidebar  ├──────────────────────────────────────────────┤
│          │  Input area (requirement / error message)     │
│ - Title  ├──────────────────────────────────────────────┤
│ - Gen    │                                              │
│ - Expl   │           Monaco Code Editor                 │
│ - Debug  │                                              │
│ - Optim  ├──────────────────────────────────────────────┤
│          │  Output Panel (explanations/issues/results)  │
└──────────┴──────────────────────────────────────────────┘
```

- **Sidebar** (`bg-slate-900`): project title, four module buttons, footer credit.
- **Header** (`bg-white`): dynamic module title/description + language `<select>`.
- **Input area**: `<textarea>` whose label/placeholder change per module.
- **Editor**: Monaco initialized via CDN loader (`vs-light` theme, auto-layout, minimap disabled).
- **Output panel**: fixed-height scrollable region rendering the response's prose fields as labeled sections.

### 12.2 State & Behavior — `app.js`

- A `modules` config object defines each module's title, description, endpoint, editor-target key (`code` / `corrected_code` / `optimized_code`), and which response fields render in the output panel.
- **Module switching** updates heading text, placeholder, button label/icon, and sidebar highlight.
- **Language changes** call `monaco.editor.setModelLanguage()` so highlighting stays in sync.
- **Actions:** `POST` JSON via `fetch()`. Loading state disables the button and shows a spinner. On success, the code field loads into Monaco and prose fields render below.
- **Toasts:** transient bottom-right notifications (green = success, red = error) animated via CSS keyframes.
- **Copy/Clear:** clipboard API + full reset of input, editor, and output.

## 13. API Documentation

All endpoints accept and return `application/json`. Errors return `{"detail": "..."}` with an appropriate HTTP status. Interactive docs are auto-generated at `http://localhost:8000/docs` (Swagger UI).

### `GET /`

Renders the dashboard HTML.

### `POST /generate/`

**Request**

```json
{
  "requirement": "a function to check if a number is prime",
  "language": "python"
}
```

**Response** `200 OK`

```json
{
  "code": "def is_prime(n):\n    ...",
  "explanation": "The module defines is_prime(n)..."
}
```

### `POST /explain/`

**Request**

```json
{
  "code": "def add(a, b):\n    return a + b",
  "language": "python"
}
```

**Response** `200 OK`

```json
{
  "summary": "...",
  "functions": "...",
  "line_by_line": "...",
  "io_complexity": "..."
}
```

### `POST /debug/`

**Request**

```json
{
  "code": "def divide(a, b)\n    return a/b",
  "language": "python",
  "error_message": "SyntaxError: invalid syntax"
}
```

(`error_message` is optional — omit or pass `""`.)

**Response** `200 OK`

```json
{
  "issues": "Line 1: missing colon after function signature...",
  "corrected_code": "def divide(a, b):\n    ...",
  "suggestions": "..."
}
```

### `POST /optimize/`

**Request**

```json
{
  "code": "def f(l):\n    r=[]\n    for i in l:\n        r.append(i*2)\n    return r",
  "language": "python"
}
```

**Response** `200 OK`

```json
{
  "optimized_code": "def f(l):\n    return [i * 2 for i in l]",
  "improvements": "Replaced manual append-loop with a list comprehension..."
}
```

### Error Codes

| Status | Cause |
| ------ | ----- |
| 400 | Empty `requirement` or `code` field |
| 422 | Malformed request body (Pydantic validation) |
| 500 | `GROQ_API_KEY` not configured |
| 502 | Groq returned unparseable JSON |
| 503 | Network error reaching Groq |
| 4xx/5xx | Groq API error forwarded verbatim |

### Supported `language` Values

`python` · `java` · `c` · `cpp` · `javascript` · `sql`

## 14. Prompt Engineering

Each module has a dedicated prompt builder producing a `(system_prompt, user_prompt)` tuple.

| Module | System Persona | JSON Contract |
| ------ | -------------- | ------------- |
| Generate | Expert software engineer / coding assistant | `{code, explanation}` |
| Explain | CS educator + software engineer | `{summary, functions, line_by_line, io_complexity}` |
| Debug | Expert debugger | `{issues, corrected_code, suggestions}` |
| Optimize | Code optimizer | `{optimized_code, improvements}` |

**Techniques applied:**

- **Strict output contracts** — system prompts explicitly forbid markdown fences and any text outside the JSON object; Groq's `json_object` response format enforces machine-readable output.
- **Few-shot-free determinism** — `temperature: 0.2` keeps code outputs focused and consistent.
- **Context injection** — target language interpolated into the instruction text and the fenced code block.
- **Edge-case handling** — debug prompt handles the "no bugs found" case; generate prompt rules require syntactic validity for the chosen language.
- **Token budget** — `max_tokens: 4096` comfortably fits a full source file plus explanations.

## 15. Data Flow

**Generate flow example:**

```
User types requirement → clicks "Generate"
  → app.js builds {requirement, language}
  → POST /generate/
  → Pydantic validates → build_generate_prompt()
  → call_groq() → Groq API
  → JSON parsed → {code, explanation}
  → app.js: editor.setValue(code); output panel renders explanation
  → success toast
```

**Error path:**

```
Groq/network failure
  → HTTPException with status + detail
  → app.js catches, shows red toast + error text in output panel
```

## 16. Setup & Installation

See [README.md](README.md) for the quick-start. Summary:

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # set GROQ_API_KEY
uvicorn app.main:app --reload
```

Then open `http://localhost:8000`.

**Environment variables:**

| Variable | Required | Default | Description |
| -------- | -------- | ------- | ----------- |
| `GROQ_API_KEY` | Yes | — | Groq API key |
| `GROQ_MODEL` | No | `openai/gpt-oss-120b` | LLM model ID override |

## 17. Usage Guide

1. **Select a module** in the left sidebar — Generate, Explain, Debug, or Optimize.
2. **Choose a language** in the header dropdown — editor highlighting updates automatically.
3. **Provide input:**
   - *Generate:* type the requirement in the top textarea.
   - *Explain / Optimize:* paste code into the Monaco editor.
   - *Debug:* paste buggy code into the editor; optionally paste the error message in the top textarea.
4. **Click the action button** — a spinner appears in the output header while the AI works.
5. **Review results:** code lands in the editor; explanations/issues/improvements render in the Output panel.
6. **Copy Code** copies editor contents to the clipboard. **Clear** resets everything.
7. Toast notifications confirm success or describe failures.

## 18. Testing & Verification

Verification performed during development:

| Check | Result |
| ----- | ------ |
| `python3 -m py_compile` on all backend modules | All compile cleanly |
| `GET /` | Returns rendered dashboard HTML; static assets resolve |
| `POST /generate/` (prime checker, Python) | Returns valid `code` + `explanation` JSON |
| `POST /explain/` (sample function) | Returns all four documented keys |
| Missing API key | `500 {"detail":"GROQ_API_KEY is not configured"}` |
| Invalid model | `404 model_not_found` forwarded from Groq |

**Manual test script:**

```bash
curl -s -X POST http://127.0.0.1:8000/generate/ \
  -H "Content-Type: application/json" \
  -d '{"requirement":"print hello world","language":"python"}'
```

## 19. Limitations

- **No execution** — generated code is not compiled or run; correctness is not verified. Review before production use.
- **Stateless** — no persistence, history, or saved projects.
- **Model availability** — this deployment uses `openai/gpt-oss-120b`; other Groq models may return `model_not_found` depending on account access.
- **Single file context** — the assistant sees only what is pasted; it cannot reason across multiple project files.
- **Rate limits** — subject to Groq account quota.
- **Security** — `.env` must never be committed; the key is visible in plain text there by design of the POC.

## 20. Future Enhancements

- **Code execution sandbox** — run generated code in-browser via Judge0 or a containerized runner.
- **Streaming responses** — Server-Sent Events for token-by-token output.
- **Diff view** — side-by-side original vs. corrected/optimized code.
- **Session history** — localStorage or optional SQLite persistence.
- **Multi-file generation** — produce entire project scaffolds.
- **Unit-test generation** — a fifth AI module.
- **Static analysis** — integrate `pylint`/`bandit` for pre-AI linting.
- **Model selector** — expose `GROQ_MODEL` choice in the UI.
- **Download/Export** — save editor content as `.py`, `.java`, etc.

## 21. Conclusion

The AI Program Generator, Debugger & Optimizer demonstrates that a genuinely useful AI coding tool requires surprisingly little infrastructure. A single FastAPI application — thin routes, an isolated service layer, and dedicated prompt builders — combined with a CDN-loaded Monaco editor delivers a professional, four-module assistant with zero frontend build tooling.

Key takeaways:

- **Modularity pays off** — each capability is independently extensible because prompts, routes, and service calls are cleanly separated.
- **Structured output matters** — enforcing JSON contracts makes the LLM integration predictable and the UI simple.
- **LLMs are a powerful accelerator** — with the right prompt design, a single model can serve four distinct developer workflows convincingly.

## 22. References

- FastAPI documentation — https://fastapi.tiangolo.com
- Groq API documentation — https://console.groq.com/docs
- Monaco Editor — https://microsoft.github.io/monaco-editor
- Tailwind CSS — https://tailwindcss.com
- Jinja2 templates — https://jinja.palletsprojects.com
- httpx async client — https://www.python-httpx.org
- Uvicorn ASGI server — https://www.uvicorn.org

---

## Support

For questions or issues, contact:

**Email:** [studentprogram@webvoidtechnologies.com](mailto:studentprogram@webvoidtechnologies.com)

---

<p align="center">
  <sub>Developed by <b>Webvoid Technologies</b></sub>
</p>
