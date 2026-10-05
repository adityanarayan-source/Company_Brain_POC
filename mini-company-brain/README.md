# Mini Company Brain POC

A small learning project that demonstrates persistent user memory, preference learning, a simple AI-agent flow, tool execution, correction capture, and observable activity.

## Architecture

React/Vite sends `POST /chat` to FastAPI. The agent retrieves user memory, chooses a registered tool when useful, creates a response, saves preferences, and logs activity in SQLite. The frontend renders both the answer and the trace.

## Folder structure

```text
mini-company-brain/
  src/                 React dashboard
  backend/             FastAPI, agent, memory, tools, database
  data/app.db          Local SQLite data (created at runtime)
```

## Prerequisites

- Node.js 18+
- Python 3.10+
- Optional: OpenAI and Supermemory API keys

## Run the backend

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
```

The API runs at http://localhost:8000 and Swagger is at http://localhost:8000/docs.

## Run the frontend

```powershell
cd ..
npm install
npm run dev
```

The dashboard runs at http://localhost:5173. If the backend is not running, the frontend uses a small local demo response so the interface can still be explored.

## Demo steps

1. Ask: `Create content announcing our new AI product.`
2. Say: `From now on keep my content short, professional, no emojis and always give me 3 options.`
3. Click **New conversation**. Visible messages clear, but the memory is not deleted.
4. Ask for content again and inspect **Memory retrieved**.
5. Ask: `Analyze this content: ...` to run `content_analyzer`.
6. Try content longer than 200 characters to see a captured tool error.
7. Correct it with: `Keep my content below 200 characters.` The correction is stored for later requests.

## Memory and tools

The local POC stores useful preferences and corrections in SQLite, scoped by `user_id`; it does not permanently save every chat message. `memory.py` is the single integration point where Supermemory can be enabled when its API details are available.

Tools are registered in one dictionary in `tools.py`: `calculator`, `company_search`, and `content_analyzer`. Adding a tool means writing one function and registering it.

## What this proves about Company Brain

This POC demonstrates the foundational loop of user interaction → agent → memory/tools → response → correction → future personalization. It is useful for exploring IRMA-like concepts such as persistent memory, personalization, company knowledge, tool use, and observable agent activity.

It is **not** the complete IRMA self-learning architecture. It does not implement Sentinel, Decision Episodes, Outcome Attribution, Neutral Engine, simulation or benchmark engines, SafetyBench, Gatekeeper, Proof Ledger, shadow/canary deployments, rollback, or model retraining. Preference capture is memory-based adaptation, not LLM retraining.
