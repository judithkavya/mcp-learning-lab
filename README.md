# MCP Learning Lab

A personal project to learn Model Context Protocol (MCP) from scratch — built phase by phase, starting from a hello world server all the way to connecting real vendor-hosted services like Atlassian and Google Calendar.

---

## What is MCP?

MCP (Model Context Protocol) is an open standard that lets AI applications connect to external tools and data sources in a consistent way. Instead of hardcoding integrations, you define a server that exposes capabilities, and any MCP-compatible client can discover and use them.

Think of it like USB-C — one standard protocol, works with any compatible device.

---

## Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Package manager | uv |
| MCP framework | FastMCP |
| LLM | Ollama — llama3.2 (local, free) |
| Vendor MCP | Atlassian (Jira/Confluence) |
| Transport | stdio (phases 1–7), HTTP (phases 8–10) |

---

## Project Structure

```
mcp-learning-lab/
├── phase1_hello_world/       # Hello world server + host via stdio
├── phase2_tools/             # Multiple tools with mock data
├── phase3_resources/         # Resources (knowledge) vs tools (actions)
├── phase4_prompts/           # Reusable prompt templates
├── phase5_gateway/           # One host, two servers
├── phase6_multi_server/      # Three servers, full workflow
├── phase7_auth/              # Bearer token auth
├── phase8_remote_mcp/        # Remote MCP over HTTP/SSE
├── phase9_rovo/              # Vendor-hosted Atlassian MCP (real Jira)
├── phase10_google_calendar/  # Custom Google Calendar MCP server
├── docs/
└── pyproject.toml
```

---

## Phases

### Phase 1 — Hello World
First MCP server and host. One tool: `hello_world(name)`. Teaches the basic host → client → server flow over stdio.

### Phase 2 — Multiple Tools
Three tools with mock data: `get_customer`, `create_ticket`, `get_weather`. Teaches how to add tools and how the client discovers them at startup.

### Phase 3 — Resources
Introduces `@mcp.resource` — readable knowledge (documents, files) vs callable tools (actions). Includes a `company_policy.md` resource.

### Phase 4 — Prompts
Introduces `@mcp.prompt` — reusable prompt templates the server exposes centrally. Any host can fetch and use them without hardcoding.

### Phase 5 — Gateway Pattern
One host connecting to two servers simultaneously. Teaches how the host routes tool calls to the right server.

### Phase 6 — Multi-Server Workflow
Three servers (customer, weather, ticket) with in-memory state. Full workflow: get customer → check weather → create ticket → list tickets → close ticket.

### Phase 7 — Auth
Bearer token pattern. Server checks token before returning protected data. Token stored in `.env` and shared between host and server.

### Phase 8 — Remote MCP over HTTP
Server runs independently on `localhost:8000` with `transport="streamable-http"`. Host connects via URL instead of subprocess. Requires two terminals.

### Phase 9 — Vendor-hosted Atlassian MCP
Connects to Atlassian's real MCP server at `https://mcp.atlassian.com/v1/mcp`. Auth via Basic auth (email + API token). Uses Ollama as the local LLM. Full flow: terminal input → LLM → MCP tool call → Atlassian → response back.

### Phase 10 — Google Calendar MCP Server
Custom MCP server wrapping Google Calendar API v3. OAuth 2.0 auth. Four tools: list, create, update, delete events. See [phase10_google_calendar/README.md](./phase10_google_calendar/README.md) for full setup.

---

## Key Concepts

**Host** — the app you build. Owns the conversation loop, makes LLM calls, manages server connections.

**MCP Client** — a library inside the host (`mcp` SDK). Handles the wire protocol. You just call `list_tools()` and `call_tool()`.

**MCP Server** — the integration wrapper. Exposes tools, resources, and prompts in MCP format.

**Self-hosted** — you run the server (phases 1–8, phase 10). Transport: stdio or HTTP.

**Vendor-hosted** — vendor runs the server, you connect via URL and auth (phase 9).

---

## Self-hosted vs Vendor-hosted

| | Self-hosted | Vendor-hosted |
|---|---|---|
| Who runs it | You | The vendor (Atlassian, GitHub etc.) |
| Transport | stdio or HTTP | HTTP/SSE |
| Auth | You control it | OAuth / API key |
| Examples | Phases 1–8, Phase 10 | Phase 9 (Atlassian) |

---

## Setup

### Install dependencies

```bash
uv add mcp python-dotenv httpx ollama google-api-python-client google-auth-oauthlib google-auth-httplib2
```

### Start Ollama

```bash
ollama serve
```

```bash
ollama pull llama3.2
```

---

## Running each phase

Each phase is self-contained and runnable independently.

```bash
# stdio phases (1–7)
uv run python phase1_hello_world/host.py

# HTTP phases (8, 10) — need two terminals
# Terminal 1:
uv run python phase8_remote_mcp/server.py
# Terminal 2:
uv run python phase8_remote_mcp/host.py

# Vendor-hosted (9)
uv run python phase9_rovo/host.py
```

---

## Notes

- `credentials.json`, `token.json`, and all `.env` files are excluded from version control
- Ollama is used as the LLM throughout to avoid API costs
- This is a POC/learning project, not production-ready
- Learnings will be applied to the PPM Agent Marketplace project
