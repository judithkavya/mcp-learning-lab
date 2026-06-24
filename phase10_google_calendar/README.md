# Phase 10 — Google Calendar MCP Server

Part of the MCP Learning Lab — a personal project to learn Model Context Protocol patterns.

This phase builds a custom Google Calendar MCP server from scratch using FastMCP and the Google Calendar API, connected to a local LLM (Ollama / llama3.2) via a Python host.

---

## What it does

Takes natural language input and performs real actions on Google Calendar:

- **List events** — fetch events in a date range
- **Create events** — with title, time, description, location, and optional attendees
- **Update events** — patch any field on an existing event
- **Delete events** — remove an event by ID

---

## Stack

| Layer | Technology |
|---|---|
| MCP server | FastMCP (Python) |
| Calendar API | Google Calendar API v3 |
| Auth | OAuth 2.0 (Desktop app flow) |
| LLM | Ollama — llama3.2 (local) |
| Transport | stdio |
| Package manager | uv |

---

## Setup

### 1. Google Cloud
- Create a project in [Google Cloud Console](https://console.cloud.google.com)
- Enable the **Google Calendar API**
- Create **OAuth 2.0 credentials** (Desktop app type)
- Download `credentials.json` and place it in this folder
- Add your Google account as a test user under **Audience → Test users**

### 2. Install dependencies
```bash
uv add mcp anthropic python-dotenv google-api-python-client google-auth-oauthlib google-auth-httplib2 ollama
```

### 3. Configure `.env`
```dotenv
GOOGLE_CREDENTIALS_PATH=./credentials.json
GOOGLE_TOKEN_PATH=./token.json
```

### 4. Start Ollama
```bash
ollama serve
```
Make sure `llama3.2` is pulled:
```bash
ollama pull llama3.2
```

---

## Running

Open two terminals:

**Terminal 1 — Start the MCP server:**
```bash
uv run python server.py
```

**Terminal 2 — Start the host:**
```bash
uv run python host.py
```

On first run, a browser window opens for Google OAuth consent. After approving, `token.json` is created automatically and reused on subsequent runs.

---

## Example prompts

```
What events do I have this week?
Create a meeting called "Sprint Review" on 2026-07-01 from 10am to 11am
Update the Sprint Review to start at 2pm instead
Delete the Sprint Review event
```

---

## File structure

```
mcp-learning-lab/
└── phase10_google_calendar/
    ├── server.py          # FastMCP server with 4 Calendar tools
    ├── host.py            # Ollama host connecting to the MCP server
    ├── credentials.json   # Google OAuth credentials (not committed)
    ├── token.json         # Auto-generated after first OAuth flow (not committed)
    ├── .env               # Credential paths
    └── README.md
```

---

## Notes

- `credentials.json` and `token.json` are excluded from version control
- Timezone is set to `Asia/Kolkata` (IST) in the server — update to your local timezone if needed
- This is a POC/learning project, not production-ready
