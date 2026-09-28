<p align="center">
  <img src="https://www.webvoidtechnologies.com/webvoid_logo_tm.png" alt="Webvoid Technologies" width="220">
</p>

<h1 align="center">AI Program Generator, Debugger & Optimizer</h1>

<p align="center">
  FastAPI-powered AI coding assistant — generate, explain, debug, and optimize code using Groq AI.
</p>

---

## Prerequisites

- Python 3.9+
- Groq API key — get one at [console.groq.com/keys](https://console.groq.com/keys)

## Setup

```bash
# 1. Navigate to the project directory
cd AI_CODE_GENERATOR

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and set GROQ_API_KEY=your_actual_key

# 5. Run the server
uvicorn app.main:app --reload
```

## Run

Open your browser at:

```
http://localhost:8000
```

## Support

For questions or issues, contact:

**Email:** [studentprogram@webvoidtechnologies.com](mailto:studentprogram@webvoidtechnologies.com)

---

<p align="center">
  <sub>Developed by <b>Webvoid Technologies</b></sub>
</p>
