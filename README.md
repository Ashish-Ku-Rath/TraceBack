# TraceBack — The Intelligent Coding & Debugging Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-0.162.0-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-51%20Passed-brightgreen.svg)](#12-running-tests)
[![Architecture: Pluggable Providers](https://img.shields.io/badge/Architecture-Pluggable%20Execution-blue.svg)](#4-execution-architecture)
[![Database: SQLite & SQLAlchemy](https://img.shields.io/badge/Database-SQLite%20%7C%20SQLAlchemy%202.x-lightgrey.svg)](#6-problem-management--database-architecture)
[![Frontend: Streamlit](https://img.shields.io/badge/Frontend-Streamlit%201.66%2B-red.svg)](#9-frontend-architecture--design-system)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

TraceBack is a next-generation LeetCode-style competitive programming and learning platform that bridges the gap between running test cases and understanding code failures. Rather than leaving developers staring at generic errors or opaque test outputs, TraceBack pairs an automated code judge with an intelligent AI debugging assistant powered by Google Gemini and Python AST analysis.

---

## 1. The Problem TraceBack Solves

Traditional online judges tell you **what** failed:
- `Wrong Answer` (expected `[0, 1]`, got `[1, 2]`)
- `Runtime Error` (`IndexError: list index out of range`)
- `Time Limit Exceeded`

However, they rarely tell you **why** your logic broke, which edge case was missed, or how your algorithm's invariant failed without giving away the full answer immediately.

**TraceBack solves this by:**
1. Isolating failure modes with precise test harnesses.
2. Providing a sandboxed, provider-independent execution layer.
3. Inspecting runtime call stacks and AST representations.
4. Leveraging LLM-driven diagnostic reasoning (Gemini API in later milestones) to deliver Socratic, actionable debugging guidance.

---

## 2. Planned Features

- **Problem Catalog & DSA Categorization**: Curated collection of DSA problems with difficulty grading and hidden edge test suites.
- **Monaco Code Editor Integration**: Full-featured in-browser code editor with syntax highlighting, auto-complete, and indentation *(Planned)*.
- **Sandboxed Execution Architecture**: Pluggable architecture supporting:
  - **Mock Provider**: Fast, safe, offline development simulation with labeled responses (`is_simulated=True`).
  - **OnlineCompiler Provider**: Real remote sandboxed execution via the official OnlineCompiler.io REST API.
- **Custom Test Lab**: Interactive test case validation where users can supply custom inputs and compare actual vs. expected outputs.
- **AI-Powered Debugging Assistant (Gemini)**: Context-aware explanations detailing why submitted code failed *(Planned)*.
- **AST Static Code Analysis**: Pre-execution syntax validation, anti-pattern detection, and algorithmic complexity hints *(Planned)*.

---

## 3. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.14+ | Primary backend and analysis language |
| **Backend API** | FastAPI | High-performance asynchronous REST API |
| **ASGI Server** | Uvicorn (standard) | Fast ASGI server with uvloop and websockets |
| **Validation** | Pydantic v2 | Robust request/response schema modeling, size limits, and byte checks |
| **Configuration** | python-dotenv | Secure environment variable handling |
| **HTTP Client** | HTTPX | Asynchronous HTTP client for OnlineCompiler REST API |
| **Database** | SQLite 3 | Lightweight, zero-config relational storage for DSA problems |
| **ORM** | SQLAlchemy 2.x | Declarative data modeling, relations, connection pooling, and migrations |
| **Testing** | Pytest & FastAPI TestClient | Automated test suite with MockTransport & in-memory SQLite (51 tests) |
| **Execution** | Pluggable Providers | Abstract interface decoupling API from execution backends |
| **Remote Judge** | OnlineCompiler.io | Remote sandboxed code execution engine |
| **Frontend** | Streamlit 1.66+ | Professional dark-theme interactive UI with custom CSS |
| **AI Debugger** | Google Gemini API *(Planned)* | Diagnostic debugging reasoning engine |

---

## 4. Execution Architecture

TraceBack decouples endpoint routing from code execution through an abstract provider pattern:

```text
                     +----------------------------+
                     |    FastAPI Routes Layer    |
                     |  /execute/run              |
                     |  /execute/check-custom-tests|
                     +--------------+-------------+
                                    |
                                    v
                     +----------------------------+
                     |      ExecutionService      |
                     +--------------+-------------+
                                    |
                                    v
                     +----------------------------+
                     |      ProviderFactory       |
                     +--------------+-------------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
            v                                               v
+------------------------+                     +---------------------------+
|      MockProvider      |                     |  OnlineCompilerProvider   |
| (Offline Development)  |                     |  (Remote Cloud Sandbox)   |
| - Never executes code  |                     | - HTTPX AsyncClient       |
| - is_simulated: True   |                     | - Raw Authorization header|
| - Deterministic mocks  |                     | - Normalized verdicts     |
+------------------------+                     +---------------------------+
```

### Provider Interface
All execution providers inherit from `BaseExecutionProvider` and implement two asynchronous methods:
1. `run_code(request: RunCodeRequest) -> RunCodeResponse`: Executes source code with custom standard input and captures stdout/stderr.
2. `run_tests(request: CustomTestCheckRequest) -> CustomTestCheckResponse`: Evaluates code against multiple test cases and returns verdicts.

### Mock Provider (Default)
> [!IMPORTANT]
> **MockProvider NEVER executes submitted source code locally.** It avoids `exec()`, `eval()`, and local `subprocess` calls completely. It returns deterministic synthetic responses explicitly flagged with `"is_simulated": true` to protect host security and prevent accidental interpretation of simulated results as real execution.

### OnlineCompiler Provider
- Connects directly to the official OnlineCompiler.io REST API (`https://api.onlinecompiler.io`).
- Communicates via `POST /api/run-code-sync/` and `POST /api/run-tests/`.
- Authenticates using the raw API key passed in the `Authorization` header (`Authorization: <api_key>`).
- Normalizes provider responses into canonical TraceBack schemas (`accepted`, `wrong_answer`, `runtime_error`, `compilation_error`, `time_limit_exceeded`, etc.).

---

## 5. Security & Isolation Mandates

1. **Host Isolation**: Zero local execution of user-submitted source code. No `exec()`, `eval()`, or local subprocess calls.
2. **Credential Protection**:
   - `ONLINECOMPILER_API_KEY` is loaded strictly from environment variables.
   - Authorization headers and API keys are never printed in logs or included in exception messages.
   - `.env` is tracked in `.gitignore` and never committed.
3. **Payload & Size Limits**:
   - Source code: Max 100 KB UTF-8 encoded bytes.
   - Standard input: Max 100 KB UTF-8 encoded bytes.
   - Expected output per test: Max 64 KB UTF-8 encoded bytes.
   - Max custom tests per request: 8.
   - Execution time: 1 to 30 seconds (default 5s).
   - Rejection of NUL (`\x00`) characters to prevent memory-level injection vulnerabilities.
4. **Deterministic Testing**: All automated test cases use `httpx.MockTransport`. No real external API calls or quota consumption occur during pytest.

---

## 6. Problem Management & Database Architecture

TraceBack stores and categorizes Data Structures & Algorithms (DSA) problems using SQLite and SQLAlchemy 2.x with synchronous sessions.

```text
+------------------------------------+             +------------------------------------+
|              problems              |             |          problem_examples          |
+------------------------------------+             +------------------------------------+
| id          : INTEGER (PK, auto)   |<----------->| id          : INTEGER (PK, auto)   |
| title       : VARCHAR(255)         |   1     N   | problem_id  : INTEGER (FK, cascade)|
| slug        : VARCHAR(255) (UNIQUE)|             | input       : TEXT                 |
| description : TEXT                 |             | expected_out: TEXT                 |
| difficulty  : VARCHAR(50) (INDEX)  |             | explanation : TEXT (nullable)      |
| constraints : TEXT                 |             +------------------------------------+
| tags        : JSON                 |
| created_at  : DATETIME             |
| updated_at  : DATETIME             |
+------------------------------------+
```

### Problem Entities
1. **Problem (`problems` table)**:
   - `id`: Auto-incrementing primary key.
   - `title`: Problem title (e.g., "Two Sum").
   - `slug`: Unique, URL-safe slug identifier (e.g., "two-sum").
   - `description`: Full markdown-formatted problem statement.
   - `difficulty`: Normalized rating: `Easy`, `Medium`, or `Hard`.
   - `constraints`: Specific runtime bounds and input limitations.
   - `tags`: JSON array of topic categories (e.g. `["Array", "Hash Map"]`).
   - `created_at` / `updated_at`: UTC timestamps.
2. **ProblemExample (`problem_examples` table)**:
   - Public sample test cases displayed in UI descriptions to illustrate problem behavior.
   - *Security Note*: These are sample examples only, distinct from future official hidden evaluation suites.
   - Linked via 1-to-many relationship with cascading delete (`ondelete="CASCADE"`).

---

## 7. Problem Management API Endpoints

| Method | Endpoint | Description | Status Code |
|---|---|---|---|
| `POST` | `/problems` | Create new problem with statement and sample examples | `201 Created` |
| `GET` | `/problems` | Retrieve paginated problem summaries with filtering and search | `200 OK` |
| `GET` | `/problems/{problem_id}` | Retrieve individual problem details and public examples | `200 OK` / `404` |
| `GET` | `/problems/slug/{slug}` | Retrieve individual problem details by unique slug | `200 OK` / `404` |

### Endpoint Filtering & Pagination Parameters (`GET /problems`)
- `skip`: Records to skip (default `0`, minimum `0`).
- `limit`: Records to return (default `10`, range `1-100`).
- `difficulty`: Filter by difficulty (`Easy`, `Medium`, `Hard`).
- `tag`: Filter by topic tag (case-insensitive substring match).
- `search`: Filter by keyword in problem title.
- Response header `X-Total-Count`: Contains the total number of records matching the query before pagination.

---

## 8. Database Initialization & Idempotent Seeding

### Automatic Initialization
When starting the FastAPI backend, the lifespan context manager automatically calls `init_db()` to ensure all required tables exist safely without deleting existing data.

### Manual Seeding via CLI
TraceBack includes an idempotent seeding command that inserts 3 classic DSA problems with original descriptions and multiple public examples:
1. **Two Sum** (Easy — Array, Hash Map)
2. **Reverse String** (Easy — String, Two Pointers)
3. **Valid Parentheses** (Medium — String, Stack)

To run or re-run the seed script:
```powershell
.\.venv\Scripts\Activate.ps1
python -m database.seed
```
*Idempotency Guarantee*: Running the seeding script multiple times will safely detect existing slugs and skip them without duplicating records or wiping the database.

---

## 9. Frontend Architecture & Design System (Day 4)

TraceBack delivers an authentic coding-platform web experience built on Streamlit with a bespoke CSS design system inspired by Linear's dark aesthetics and LeetCode's workflow clarity.

### Brand Identity
- **Logo**: `</TraceBack>`
  - `</` rendered in electric purple (`#8B5CF6`).
  - `Trace` rendered in crisp white (`#F8FAFC`).
  - `Back` rendered in light purple (`#C084FC`).
- **Tagline**: *The Intelligent Coding & Debugging Assistant*

### Design System Color Palette
The UI follows an 80% black/charcoal, 15% dark navy, and 5% accent palette:

| Element | Hex Code | Purpose |
|---|---|---|
| **Main Background** | `#080B12` | Primary page canvas |
| **Sidebar Background** | `#0D111B` | Navigation sidebar background |
| **Card Background** | `#131A27` | Primary card containers |
| **Secondary Card** | `#192235` | Nested example boxes & metrics |
| **Primary Accent** | `#8B5CF6` | Action buttons, active navigation, logo accent |
| **Secondary Accent** | `#3B82F6` | Informational highlights |
| **Main Text** | `#F8FAFC` | Headings, primary labels |
| **Secondary Text** | `#94A3B8` | Subtitles, metadata descriptions |
| **Borders** | `#273449` | Restrained card & separator outlines |
| **Success** | `#22C55E` | Easy difficulty badge, online indicator |
| **Warning** | `#F59E0B` | Medium difficulty badge, constraints header |
| **Error** | `#EF4444` | Hard difficulty badge, offline indicator |

### Key Frontend Views
1. **Dashboard (`frontend/pages/dashboard.py`)**:
   - Welcome Hero banner with direct exploration action.
   - Real-time KPI statistics cards powered directly by the FastAPI backend (Total, Easy, Medium, Hard problems).
   - Recommended problems list with colored difficulty badges, topic tags, and quick-solve buttons.
   - Polished empty state for recent submissions activity.
   - 4-step algorithmic problem-solving walkthrough.
2. **Problem Library (`frontend/pages/problems.py`)**:
   - Interactive search bar querying `GET /problems?search=<term>`.
   - Difficulty dropdown filter (`All`, `Easy`, `Medium`, `Hard`).
   - Category topic tag filter (`Array`, `Hash Map`, `String`, `Stack`, `Two Pointers`).
   - Clean problems table with difficulty badges, tag pills, and "Solve" buttons.
3. **Problem Details (`frontend/pages/problem_detail.py`)**:
   - Full problem statement with formatted markdown and code blocks.
   - Algorithmic bounds and constraints checklist.
   - Structured public sample test cases (Input, Expected Output, Explanation).
   - "Back to Problems" navigation and Day 5 Workspace integration button.
4. **Navigation & Status**:
   - Fixed-looking sidebar with active page highlight.
   - Real-time backend status pill (live pulsing green dot when FastAPI is running; red when offline with actionable troubleshooting instructions).

---

## 10. Project Directory Structure

```text
TraceBack/
├── frontend/                   # Frontend presentation layer (Streamlit 1.66+)
│   ├── app.py                  # Streamlit application entrypoint & routing
│   ├── api_client.py           # Reusable BackendAPIClient (HTTPX)
│   ├── config.py               # Theme constants, brand logo, and URLs
│   ├── styles.py               # Custom CSS design system injection
│   ├── components/             # Reusable UI widgets
│   │   ├── __init__.py         # Component exports
│   │   ├── sidebar.py          # Brand logo & navigation sidebar
│   │   ├── header.py           # Top navigation bar & live health indicator
│   │   ├── cards.py            # Stat cards, hero banner, getting-started
│   │   └── problem_card.py     # Difficulty badges, tags, and problem items
│   └── pages/                  # Route view controllers
│       ├── __init__.py         # Page exports
│       ├── dashboard.py        # Main platform dashboard
│       ├── problems.py         # Problem Library with search & filters
│       ├── problem_detail.py   # Full problem statement & sample examples
│       └── coming_soon.py      # Polished preview for future milestones
│
├── backend/                    # Core application backend (FastAPI)
│   ├── core/                   # Application settings, exceptions, and configuration
│   │   ├── config.py           # Centralized settings, DB URL & bounds
│   │   └── exceptions.py       # Domain exceptions (Configuration, DuplicateSlug, NotFound)
│   ├── integrations/           # External service clients
│   │   └── onlinecompiler_client.py # Async HTTP client for OnlineCompiler.io
│   ├── models/                 # SQLAlchemy 2.x declarative ORM models
│   │   ├── __init__.py         # Re-export Problem and ProblemExample
│   │   └── problem.py          # Problem and ProblemExample table definitions
│   ├── routes/                 # API route handlers & endpoints
│   │   ├── execution.py        # /execute/run and /execute/check-custom-tests
│   │   └── problems.py         # /problems endpoints (CRUD, filters, pagination)
│   ├── schemas/                # Pydantic request/response schemas
│   │   ├── execution.py        # Execution payload schemas & validators
│   │   ├── problem.py          # Problem create, detail, and summary schemas
│   │   └── system.py           # System & health schemas
│   ├── services/               # Business logic orchestration
│   │   ├── execution_service.py # Decoupled execution orchestrator
│   │   ├── problem_service.py   # Problem query, pagination, and creation logic
│   │   └── providers/          # Pluggable execution providers
│   │       ├── base_provider.py           # Abstract execution provider ABC
│   │       ├── mock_provider.py           # Safe simulated execution provider
│   │       ├── onlinecompiler_provider.py # Real remote execution provider
│   │       └── provider_factory.py        # Provider resolution factory
│   └── main.py                 # FastAPI application instance, lifespan & routing
│
├── database/                   # Database engine, connection, base, and seeding
│   ├── base.py                 # DeclarativeBase base class
│   ├── connection.py           # Engine, sessionmaker, get_db dependency, init_db
│   └── seed.py                 # Idempotent problem seeding script
│
├── tests/                      # Automated test suite (Pytest & TestClient - 51 tests)
│   ├── test_execution_api.py   # FastAPI endpoint integration & boundary tests
│   ├── test_frontend_api_client.py # Frontend HTTPX API client unit tests
│   ├── test_main.py            # Core health & system tests
│   ├── test_mock_provider.py   # Mock provider simulation & safety tests
│   ├── test_onlinecompiler_provider.py # OnlineCompiler client & normalization tests
│   └── test_problems_api.py    # Problem management, filtering, and seeding tests
│
├── .env.example                # Template for required environment variables
├── .gitignore                  # Git exclusion rules (ignores *.db and .env)
├── requirements.txt            # Python package dependencies
├── README.md                   # Comprehensive project documentation
└── PROJECT_NOTES.md            # Architectural decisions and technical notes
```

---

## 11. Installation & Running Instructions

### Prerequisites
- Python 3.10+ (Python 3.14 recommended)
- Git

### Step 1: Clone Repository & Create Virtual Environment
On **Windows (PowerShell)**:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Configure Environment
Create `.env` from template:
```powershell
Copy-Item .env.example .env
```

### Step 4: Seed Database
```powershell
python -m database.seed
```

### Step 5: Start the Backend and Frontend

Run the backend and frontend in separate terminals:

**Terminal 1 — Backend (FastAPI)**:
```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
- Interactive Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Interactive ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

**Terminal 2 — Frontend (Streamlit)**:
```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501
```
- Open in browser: [http://127.0.0.1:8501](http://127.0.0.1:8501)

---

## 11. Example API Requests & Responses

### 1. Create a Problem (`POST /problems`)
```bash
curl -X POST "http://127.0.0.1:8000/problems" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Two Sum",
    "slug": "two-sum",
    "description": "Given an integer array nums and an integer target, return indices of two numbers that add up to target.",
    "difficulty": "Easy",
    "constraints": "2 <= nums.length <= 10^4",
    "tags": ["Array", "Hash Map"],
    "examples": [
      {
        "input": "nums = [2, 7, 11, 15], target = 9",
        "expected_output": "[0, 1]",
        "explanation": "2 + 7 == 9"
      }
    ]
  }'
```

### 2. List Problems (`GET /problems?difficulty=Easy&tag=array`)
```bash
curl -X GET "http://127.0.0.1:8000/problems?difficulty=Easy&tag=array"
```
**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "title": "Two Sum",
    "slug": "two-sum",
    "difficulty": "Easy",
    "tags": ["Array", "Hash Map"],
    "created_at": "2026-11-05T14:33:55.123456Z",
    "updated_at": "2026-11-05T14:33:55.123456Z"
  }
]
```

### 3. Retrieve Individual Problem (`GET /problems/1`)
```bash
curl -X GET "http://127.0.0.1:8000/problems/1"
```
**Response (200 OK)**:
```json
{
  "id": 1,
  "title": "Two Sum",
  "slug": "two-sum",
  "description": "Given an integer array nums and an integer target...",
  "difficulty": "Easy",
  "constraints": "2 <= nums.length <= 10^4...",
  "tags": ["Array", "Hash Map"],
  "created_at": "2026-11-05T14:33:55.123456Z",
  "updated_at": "2026-11-05T14:33:55.123456Z",
  "examples": [
    {
      "id": 1,
      "problem_id": 1,
      "input": "nums = [2, 7, 11, 15], target = 9",
      "expected_output": "[0, 1]",
      "explanation": "Because nums[0] + nums[1] == 2 + 7 == 9, return [0, 1]."
    }
  ]
}
```

---

## 12. Running Tests

Run the complete test suite with pytest:

```powershell
pytest -v
```

All 51 tests run deterministically offline:
- 26 execution and core tests using `httpx.MockTransport`.
- 16 problem management tests using isolated in-memory SQLite (`sqlite:///:memory:`) with `StaticPool`.
- 9 frontend API client tests verifying query construction, error handling, and stats calculation.

---

## 13. Current Development Status

- **Milestone 1 — Project Foundation**: Completed.
- **Milestone 2 — Execution Architecture**: Completed.
  - Pluggable provider architecture with `BaseExecutionProvider` and `ProviderFactory`.
  - Non-executing `MockProvider` with deterministic simulation flags (`is_simulated=True`).
  - `OnlineCompilerProvider` integration with official REST API endpoints.
  - Endpoints `POST /execute/run` and `POST /execute/check-custom-tests` active and verified.
  - Strict payload validation (UTF-8 byte length, NUL-character rejection, test count limits).
- **Milestone 3 — Problem Management System**: Completed.
  - SQLite database integration with SQLAlchemy 2.x declarative models.
  - `Problem` and `ProblemExample` entities with 1-to-many relationship.
  - Endpoints `POST /problems`, `GET /problems`, `GET /problems/{id}`, `GET /problems/slug/{slug}`.
  - Pagination (`skip`, `limit`), filtering by difficulty, filtering by tag, title search.
  - Idempotent seeding mechanism with 3 initial DSA problems (Two Sum, Reverse String, Valid Parentheses).
- **Milestone 4 — Frontend Foundation & UI Development**: Completed.
  - Built full Streamlit frontend with bespoke dark coding-platform theme (`#080B12`, `#0D111B`, `#131A27`, `#8B5CF6`).
  - Brand identity with modern `</TraceBack>` typography and tagline.
  - Dashboard with live backend statistics, problem recommendations, and recent activity empty state.
  - Problem Library with live title search, difficulty filters, and topic tag filters.
  - Problem Detail view with formatted description, constraints checklist, and sample test cases.
  - Robust `BackendAPIClient` with error resilience, live health indicator, and retry messaging.
  - 51/51 automated unit and integration tests passing.
