<div align="center">

# ✈️ Voyager AI — Multi-Agent Travel Planner

**An enterprise-grade, AI-powered travel planning system built with LangGraph, Groq LLaMA 3, and Model Context Protocol (MCP)**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2%2B-00b4d8?logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-f97316?logo=groq&logoColor=white)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Memory-336791?logo=postgresql&logoColor=white)](https://postgresql.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> *Seven specialised AI agents collaborate to research flights, hotels, weather, and budgets — then ask for your approval before delivering a polished travel itinerary.*

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Architecture](#-architecture)
- [Agent Pipeline](#-agent-pipeline)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Environment Variables](#-environment-variables)
- [Running the Application](#-running-the-application)
- [How It Works](#-how-it-works)
- [MCP Servers](#-mcp-servers)
- [Database & Memory](#-database--memory)
- [UI Overview](#-ui-overview)
- [API Keys Guide](#-api-keys-guide)
- [Known Limitations](#-known-limitations)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌐 Overview

**Voyager AI** is a production-grade, multi-agent travel planning system that combines the power of:

- **LangGraph** — stateful, graph-based orchestration of multiple AI agents
- **Groq + LLaMA 3.3 70B** — ultra-fast LLM inference
- **Model Context Protocol (MCP)** — standardised real-time tool integration with live aviation, weather, and web-search data
- **PostgreSQL** — persistent conversation memory across sessions (like ChatGPT threads)
- **Streamlit** — a Trava-AI-inspired professional chat dashboard

A user describes their trip in natural language. A **Supervisor Agent** analyses the request, activates the right specialist agents, those agents gather real-world data via MCP servers, and finally the system pauses for **your explicit approval** before generating a polished, downloadable travel plan.

---

## 🎬 Live Demo

```
APP LINK - https://graph-orchestrated-multi-agent-retrieval-telemetry-pipeline-qm.streamlit.app/ 
```

Open `http://localhost:8501` in your browser.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Streamlit UI                           │
│          (Trava-AI-inspired 3-column dashboard)             │
└───────────────────────────┬─────────────────────────────────┘
                            │  HumanMessage + thread_id (UUID)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   LangGraph StateGraph                      │
│                  (graph.py — compiled app)                  │
│                                                             │
│   START ──► [Supervisor] ──► conditional routing            │
│                   │                                         │
│          ┌────────┼────────┬──────────┐                     │
│          ▼        ▼        ▼          ▼                     │
│      [Flight]  [Hotel]  [Weather]  [Budget]                 │
│          │        │        │          │                     │
│          └────────┴────────┴──────────┘                     │
│                        │                                    │
│                        ▼                                    │
│                  [Itinerary Agent]                          │
│                        │                                    │
│                        ▼                                    │
│              [Human Approval — interrupt()]  ◄── YOU        │
│                        │                                    │
│                        ▼                                    │
│               [Final Response Agent]                        │
│                        │                                    │
│                       END                                   │
└─────────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┴──────────────┐
              │        MCP Servers         │
              │  ┌─────────────────────┐   │
              │  │  Tavily (HTTP MCP)  │   │  ← Hotel / web search
              │  ├─────────────────────┤   │
              │  │ AviationStack (MCP) │   │  ← Airports & airlines
              │  ├─────────────────────┤   │
              │  │  OpenWeatherMap MCP │   │  ← Current weather & forecast
              │  └─────────────────────┘   │
              └────────────────────────────┘
                            │
              ┌─────────────┴──────────────┐
              │  PostgreSQL Checkpointer   │  ← Persistent thread memory
              └────────────────────────────┘
```

---

## 🤖 Agent Pipeline

| # | Agent | Role | Data Source |
|---|-------|------|-------------|
| 1 | 🧭 **Supervisor Agent** | Validates the request (input guardrail), decides which specialist agents to activate, extracts trip constraints | Groq LLM |
| 2 | ✈️ **Flight Agent** | Fetches live airport and airline data, synthesises flight guidance (routes, duration, fare ranges, booking advice) | AviationStack MCP |
| 3 | 🏨 **Hotel Agent** | Searches the web for the best hotels and neighbourhoods for the destination | Tavily MCP |
| 4 | 🌤️ **Weather Agent** | Retrieves current weather conditions and a 5-step forecast for the destination city | OpenWeatherMap MCP |
| 5 | 💰 **Budget Agent** | Analyses cost categories, identifies risk areas, and provides money-saving suggestions | Groq LLM (all prior context) |
| 6 | 🗓️ **Itinerary Agent** | Synthesises all gathered data into a structured, day-by-day draft travel plan | Groq LLM |
| 7 | 👤 **Human Approval** | Pauses the graph via `interrupt()` — you review the draft and either approve or request revisions | LangGraph interrupt |
| 8 | 🎯 **Final Response Agent** | Polishes the approved (or revised) plan into a production-ready itinerary | Groq LLM |

> **Supervisor routing is dynamic** — if your query mentions no flights, the Flight Agent is skipped. The supervisor decides which agents are needed based on your request.

---

## ✨ Features

### 🧠 AI & Agent Capabilities
- **Input Guardrail** — The Supervisor rejects non-travel requests before any agent runs
- **Dynamic routing** — Only the agents relevant to your query are activated
- **Human-in-the-loop** — Graph pauses at `interrupt()` for your review and approval
- **Auto-approve mode** — Toggle in sidebar to skip the review step for fast iterations
- **Context-aware revision** — Reject the draft with feedback; the Final Agent incorporates your notes

### 🔧 Technical
- **Persistent memory** — PostgreSQL checkpointer stores every thread; resume conversations across browser sessions
- **UUID thread management** — Every trip is a unique thread (like ChatGPT conversations), named with a human-readable label
- **MCP tool integration** — Live, real-world data from aviation, weather, and web APIs via standardised MCP servers
- **Streaming output** — Agent results stream to the UI in real time as each node completes
- **LangGraph interrupt/resume** — Proper `Command(resume=...)` pattern for human-in-the-loop

### 🎨 UI / UX
- **Trava-AI-inspired design** — 3-column layout (sidebar · chat centre · right panel)
- **Conversation naming** — Trips are named from your query (e.g. "Japan Trip India ₹2 Lakhs")
- **Tabbed agent outputs** — Flights, Hotels, Weather, Budget, Itinerary in separate tabs
- **Quick destination chips** — One-click popular trip starters
- **Smart picks & inspiration** — Right-panel destination cards
- **Auto-save & download** — Plans saved to `travel_plans/` and downloadable as Markdown
- **Continue Planning** — Right panel shows your most recent trip for quick resumption

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Groq API — LLaMA 3.3 70B (openai/gpt-oss-120b routing) |
| **Orchestration** | LangGraph 0.2+ (StateGraph, interrupt, Command) |
| **LLM Framework** | LangChain Core, LangChain Groq |
| **Tool Protocol** | Model Context Protocol (MCP) via `langchain-mcp-adapters` |
| **Weather API** | OpenWeatherMap REST API (custom FastMCP server) |
| **Aviation API** | AviationStack REST API (official MCP server) |
| **Web Search** | Tavily Search API (streamable HTTP MCP) |
| **Database** | PostgreSQL + `langgraph-checkpoint-postgres` |
| **Frontend** | Streamlit 1.x |
| **HTTP Client** | `requests`, `httpx` |
| **Environment** | `python-dotenv` |
| **Data Models** | `pydantic` |

---

## 📁 Project Structure

```
AI Travel Planner RAG Systen/
│
├── frontend.py                  # ✅ Main Streamlit UI (Trava-AI design)
├── graph.py                     # LangGraph StateGraph — compiles the full pipeline
├── agents.py                    # All 8 agent node functions
├── state.py                     # TravelState TypedDict (shared graph state)
├── config.py                    # API key loading + get_llm() factory
├── mcp_client.py                # MCP client hub (connects all 3 MCP servers)
│
├── custom_weather_mcp_server.py # FastMCP server wrapping OpenWeatherMap
│
├── tools/
│   ├── tavily_search.py         # Legacy direct Tavily SDK wrapper
│   └── search_flight.py         # Legacy direct AviationStack REST wrapper
│
├── aviationstack-mcp/           # Third-party AviationStack MCP server
│   ├── src/aviationstack_mcp/
│   │   ├── server.py            # FastMCP server with 15+ aviation tools
│   │   ├── __init__.py
│   │   └── __main__.py
│   ├── .venv/                   # Isolated Python 3.13 venv for this server
│   ├── pyproject.toml
│   └── requirements.txt
│
├── travel_plans/                # Auto-saved Markdown travel plans
│   └── travel_plan_*.md
│
├── requirements.txt             # Main project dependencies
├── .env                         # API keys (never commit to git!)
└── README.md
```

---

## 📋 Prerequisites

Before you begin, ensure you have:

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.10+ | Main project uses Python 3.10 |
| PostgreSQL | 14+ | For conversation memory/checkpointing |
| Git | Any | To clone the repository |

**API Keys required** (all free tiers available):
- [Groq API Key](https://console.groq.com) — Free, very fast LLM inference
- [Tavily API Key](https://tavily.com) — Free tier: 1000 searches/month
- [AviationStack API Key](https://aviationstack.com) — Free tier: 500 requests/month
- [OpenWeatherMap API Key](https://openweathermap.org/api) — Free tier: 60 calls/minute

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/voyager-ai-travel-planner.git
cd voyager-ai-travel-planner
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Main Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `langchain-mcp-adapters` and `mcp` are also required but not in `requirements.txt`. Install them manually:

```bash
pip install langchain-mcp-adapters mcp
```

### 4. Set Up the AviationStack MCP Server

This server has its own isolated environment:

```bash
cd aviationstack-mcp
pip install uv          # if not already installed
uv sync                 # installs into aviationstack-mcp/.venv
cd ..
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root (copy from the template below):

```env
# ── LLM ─────────────────────────────────────────────
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile    # optional override

# ── Travel APIs ──────────────────────────────────────
TAVILY_API_KEY=your_tavily_api_key_here
AVIATIONSTACK_API_KEY=your_aviationstack_api_key_here
OPENWEATHER_API_KEY=your_openweathermap_api_key_here

# ── Database (PostgreSQL) ────────────────────────────
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/langgraph_memory
```

> ⚠️ **Never commit your `.env` file to Git.** Add it to `.gitignore`.

---

## 🗄️ Database Setup

Voyager AI uses **PostgreSQL** to persist conversation memory across sessions (identical to how ChatGPT remembers your threads).

### 1. Create the database

```sql
-- Connect to PostgreSQL and run:
CREATE DATABASE langgraph_memory;
```

### 2. The checkpointer sets itself up automatically

When `graph.py` is imported (on app start), `PostgresSaver.setup()` creates all required tables automatically. No manual migrations needed.

### 3. Verify your connection string

```env
DATABASE_URL=postgresql://username:password@localhost:5432/langgraph_memory
```

> If you don't have PostgreSQL, the app still works — it falls back to in-memory checkpointing (no cross-session persistence).

---

## ▶️ Running the Application

### Start the Streamlit Frontend

```bash
streamlit run frontend.py
```

Then open **http://localhost:8501** in your browser.

The app automatically:
- Connects to PostgreSQL on startup
- Launches the AviationStack MCP server as a subprocess on first query
- Launches the custom Weather MCP server as a subprocess on first query
- Connects to Tavily via its hosted HTTP MCP endpoint

### (Optional) Test MCP Servers Individually

**Test Weather MCP:**
```bash
python testing_weather_mcp_server.py
```

**Test AviationStack MCP:**
```bash
python test_aviationstack_mcp_server.py
```

**Run Weather MCP server directly:**
```bash
python custom_weather_mcp_server.py
```

---

## 🔍 How It Works

### Step-by-Step Flow

```
1. User enters query  →  "7-day Japan trip from Delhi under ₹2 Lakhs"
                                        │
2. New UUID thread created              │  (each trip = unique thread ID)
                                        │
3. Supervisor Agent runs                │
   ├─ Input guardrail: Is this travel?  │  (rejects off-topic requests)
   ├─ Extracts: destination=Japan,      │
   │            origin=Delhi,           │
   │            budget=₹2 Lakhs,        │
   │            duration=7 days         │
   └─ Selects agents: [flight, hotel,  │
                       weather, budget, │
                       itinerary]       │
                                        │
4. Flight Agent                         │
   ├─ Calls AviationStack MCP          │  → list_airports
   ├─ Calls AviationStack MCP          │  → list_airlines
   └─ LLM synthesises flight guidance  │
                                        │
5. Hotel Agent                          │
   └─ Calls Tavily MCP search          │  → "Best hotels Japan from India"
                                        │
6. Weather Agent                        │
   ├─ Calls Weather MCP                │  → get_current_weather(Tokyo)
   └─ Calls Weather MCP                │  → get_forecast(Tokyo)
                                        │
7. Budget Agent                         │
   └─ LLM analyses all prior results   │  → cost breakdown + savings tips
                                        │
8. Itinerary Agent                      │
   └─ LLM synthesises day-by-day plan  │
                                        │
9. ⏸️  PAUSE — Human Approval           │  ← Graph interrupt()
   User reviews draft in UI            │
   User clicks ✅ Approve OR 🔄 Revise │
                                        │
10. Final Response Agent                │
    └─ Polishes plan based on feedback │
                                        │
11. Result displayed + auto-saved      │  → travel_plans/travel_plan_*.md
```

### State Management

All agents share a single `TravelState` TypedDict that flows through the graph:

```python
class TravelState(TypedDict, total=False):
    messages:             list[AnyMessage]   # accumulated chat history
    user_id:              str                # UUID thread identifier
    user_query:           str                # original user request
    trip_constraints:     dict               # destination, origin, budget, etc.
    selected_agents:      list[str]          # supervisor's routing decision
    supervisor_reasoning: str                # why these agents were chosen
    flight_results:       str                # flight agent output
    hotel_results:        str                # hotel agent output
    weather_results:      str                # weather agent output
    budget_results:       str                # budget agent output
    itinerary:            str                # draft itinerary
    approval_request:     str                # message shown to human
    human_feedback:       str                # user's approval/revision notes
    approved:             bool               # True = approved, False = revise
    final_response:       str                # polished final travel plan
    llm_calls:            int                # running LLM call counter
```

---

## 🔌 MCP Servers

### 1. Custom Weather MCP Server (`custom_weather_mcp_server.py`)

A lightweight **FastMCP** server that wraps the OpenWeatherMap API.

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_current_weather` | Current temperature, humidity, condition, wind | `city: str` |
| `get_forecast` | Next 5 × 3-hour forecast intervals | `city: str` |

**Transport:** `stdio` (spawned as subprocess)
**Launch command:**
```bash
python custom_weather_mcp_server.py
```

---

### 2. AviationStack MCP Server (`aviationstack-mcp/`)

An official third-party MCP server for the AviationStack API with **15+ tools**.

Key tools used by Voyager AI:

| Tool | Description |
|------|-------------|
| `list_airports` | Search airports by name/code |
| `list_airlines` | Search airlines by name/code |
| `get_flight_status` | Real-time flight status by IATA number |
| `flights_with_airline` | Active flights for a given airline |
| `flight_arrival_departure_schedule` | Airport timetable (arrivals/departures) |
| `historical_flights_by_date` | Past flight data (Basic plan+) |

**Transport:** `stdio` (spawned as subprocess via its own `.venv`)
**Launch command:**
```bash
# Uses the isolated venv inside aviationstack-mcp/
aviationstack-mcp\.venv\Scripts\python.exe -m aviationstack_mcp mcp run
```

---

### 3. Tavily Web Search MCP

Hosted MCP endpoint provided directly by Tavily — no local server needed.

| Tool | Description |
|------|-------------|
| `tavily_search` | Searches the web and returns structured results |

**Transport:** `streamable_http`
**Endpoint:** `https://mcp.tavily.com/mcp/?tavilyApiKey=<YOUR_KEY>`

---

## 🗃️ Database & Memory

Voyager AI uses **LangGraph's PostgreSQL checkpointer** to store the full state of every conversation thread.

### What's persisted
- Every message in the conversation (`messages` field)
- All agent outputs (flight, hotel, weather, budget, itinerary, final)
- Trip constraints extracted by the supervisor
- Approval decisions and human feedback
- LLM call counts

### Thread Model
Every trip is a **unique UUID thread** — identical to how ChatGPT organises conversations. The thread ID is:
- Generated fresh when you click **＋ New Chat**
- Stored in Streamlit session state
- Displayed (truncated) in the UI metrics
- Used as `config["configurable"]["thread_id"]` for all graph calls

This means you can close the browser, reopen it, and resume an in-progress trip using the same thread ID.

---

## 🖥️ UI Overview

The frontend is built in Streamlit with a **Trava AI-inspired 3-column layout**:

### Left Sidebar
| Element | Description |
|---------|-------------|
| ✈️ Voyager AI logo | Brand identity |
| Navigation (Chats, Trips, Explore…) | App sections |
| **＋ New Chat** button | Starts a fresh UUID thread |
| Conversation history | Named trips (ChatGPT-style) |
| Trending card | Highlighted destination |
| ⚙️ Settings | Auto-approve toggle |

### Centre Panel
| State | Display |
|-------|---------|
| **Empty (home)** | "Where to next?" hero + quick chips + chat input |
| **Running** | Live agent status widgets streaming results |
| **Awaiting approval** | Draft itinerary + ✅ Approve / 🔄 Revise buttons |
| **Complete** | Tabbed results (Flights/Hotels/Weather/Budget/Itinerary) + Final Plan card + Download |

### Right Panel
| Section | Description |
|---------|-------------|
| Smart picks | Curated destination image grid |
| Continue Planning | Last trip card for quick resumption |
| Get Inspired | Adventure/experience images |
| ⚡ Agent Status | Live 🟢/⚪ indicators for all 8 pipeline steps |
| 🌟 Chase the Experiences | Motivational CTA card |

---

## 🔑 API Keys Guide

### Groq
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up → API Keys → Create API Key
3. Free tier: extremely fast inference with LLaMA 3.3 70B

### Tavily
1. Visit [app.tavily.com](https://app.tavily.com)
2. Sign up → Dashboard → API Keys → Copy your key
3. Free tier: 1,000 searches/month

### AviationStack
1. Visit [aviationstack.com](https://aviationstack.com)
2. Sign up → Dashboard → Copy your Access Key
3. Free tier: 500 API calls/month (real-time flights require Basic plan+)

### OpenWeatherMap
1. Visit [openweathermap.org](https://openweathermap.org/api)
2. Sign up → My API Keys → Copy your key
3. Free tier: 60 calls/minute, 1,000,000 calls/month

---

## ⚠️ Known Limitations

| Limitation | Detail |
|------------|--------|
| **AviationStack free tier** | Real-time flight status and timetable endpoints require a paid plan. The free tier supports reference data (airports, airlines) only. |
| **Weather forecast granularity** | The free OpenWeatherMap API returns 3-hour interval forecasts, not daily summaries. |
| **Tavily MCP URL** | The Tavily MCP URL in `mcp_client.py` contains a literal `<TAVILY_API_KEY>` placeholder — replace it with your actual key. |
| **asyncio in sync agents** | Agent functions use `asyncio.run()` to call async MCP helpers. If your environment has a running event loop (e.g., Jupyter), this will raise an error. |
| **PostgreSQL required for persistence** | Without PostgreSQL, the app falls back to in-memory checkpointing and conversation history is lost on restart. |
| **MCP subprocess startup time** | The AviationStack and Weather MCP servers are spawned as subprocesses on first use — expect a 2–5 second cold start delay. |

---

## 🗺️ Roadmap

- [ ] Google Flights / Skyscanner integration for real fare prices
- [ ] Booking.com / Hotels.com MCP for live hotel prices
- [ ] Multi-city trip planning support
- [ ] Trip comparison (compare 3 destinations side-by-side)
- [ ] PDF export with custom branding
- [ ] User accounts with trip sharing
- [ ] Voice input ("Tell me about a Japan trip…")
- [ ] Mobile-optimised layout

---

## 🤝 Contributing

Contributions are warmly welcome! Here's how to get started:

1. **Fork** the repository
2. **Create a branch** — `git checkout -b feature/amazing-feature`
3. **Commit your changes** — `git commit -m 'Add amazing feature'`
4. **Push to the branch** — `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Keep each agent function in `agents.py` self-contained and pure (inputs from state, outputs to state)
- New external API integrations should be added as MCP servers, not direct API calls in agents
- All new state fields must be declared in `state.py`'s `TravelState`
- The supervisor prompt in `agents.py` must be updated when new agents are added

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ using LangGraph, Groq, and MCP**

*If this project helped you, please consider giving it a ⭐ on GitHub!*

</div>

