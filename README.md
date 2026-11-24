# TraceBack

> **An Intelligent Coding, Execution and AI-Powered Debugging Platform.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.162.0-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-74%20Passed-brightgreen.svg)](#9-automated-testing)
[![Code Editor](https://img.shields.io/badge/Editor-Monaco-blue.svg)](https://microsoft.github.io/monaco-editor/)
[![AI Engine](https://img.shields.io/badge/AI-Google%20Gemini-8E75B2.svg?logo=google&logoColor=white)](https://aistudio.google.com/)
[![Remote Judge](https://img.shields.io/badge/Execution-OnlineCompiler.io-0284C7.svg)](#5-execution-engine--providers)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20SQLAlchemy%202.x-lightgrey.svg)](#6-database-architecture)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 1. Project Overview

**TraceBack** is an intelligent coding platform designed to bridge the gap between running automated test cases and understanding why code fails. Traditional online judges inform students **what** happened (`Wrong Answer`, `Runtime Error`, `Time Limit Exceeded`), but leave them stranded when deciphering **why** their algorithmic logic broke or which boundary condition failed.

TraceBack couples a responsive, split-screen coding workspace with an automated test runner and an **AI Debug Mentor** powered by Google Gemini. Rather than simply revealing solutions, TraceBack provides Socratic guidance, algorithm walk-throughs, bug isolation, and code fixes tailored to the student's exact source code.

---

## 2. Key Features

### 💻 Interactive Monaco Code Editor
- In-browser VS Code Monaco editor running in an **uncontrolled client-side model**.
- **Blank by Default**: Every problem opens with a completely empty editor so students write solutions from scratch.
- **Zero-Rerun Stability**: Custom event-driven synchronization (`Ctrl+S`, action buttons) prevents cursor jumping and intermediate Streamlit re-renders while typing.
- Persistent drafts cached per problem across navigation and normal page refreshes.

### 🐍 Complete Program Mode Execution
- Formatted for competitive programming standards (Codeforces / CodeChef / HackerRank style):
  - Standard input read via `sys.stdin` or `input()`.
  - Standard output produced via `print()`.
- Eliminates brittle boilerplate wrapper classes.

### ⚡ Dual Execution Provider System
- **OnlineCompiler Provider**: Real remote sandboxed execution in the cloud via the official OnlineCompiler.io REST API.
- **Mock Provider (Offline Development)**: Safe, deterministic simulation engine that never executes untrusted code locally (`is_simulated=True`), guaranteeing host security during development and testing.

### 📚 Problem Library (23 Programming Problems)
- **23 curated problems** covering essential data structures and algorithms across **Easy** and **Medium** tiers:
  - **Array & Strings**: Two Sum, Reverse String, Valid Parentheses, Palindrome String, Second Largest Distinct Element, Missing Number in an Array, Count Vowels and Consonants.
  - **Math & Number Theory**: Fibonacci Series, Armstrong Number, Palindrome Number, Prime Number, Factorial, Reverse a Number, Sum of Digits, Count Digits, GCD, LCM, Even or Odd, Leap Year, Multiplication Table, Perfect Number, Strong Number, Decimal to Binary.
- Dynamic filtering by difficulty, topic tags (`Array`, `Math`, `String`, `Basic Programming`), and real-time title search.

### ⚖️ Automated Submission & Test Judging
- Evaluates code against multiple hidden and public test cases stored in SQLite.
- Computes execution time, memory usage, exit code, stdout, and stderr.
- Delivers clear verdicts: `ACCEPTED`, `WRONG_ANSWER`, or `RUNTIME_ERROR`, complete with per-testcase input/expected/actual comparisons.

### 🔬 Custom Test Lab
- Interactive multi-testcase sandbox enabling developers to supply multiple custom input/expected-output pairs simultaneously.

### 🤖 Gemini-Powered AI Debug Mentor
- Integrated with the **Google Gemini API** (`POST /ai/debug`), featuring **five specialized assistance modes**:
  1. **Explain Error (`explain_error`)**: Translates complex runtime tracebacks (e.g. `IndexError`, `ZeroDivisionError`) into plain English explanations.
  2. **Find the Bug (`find_bug`)**: Pinpoints the exact faulty statement, explains why it fails, and identifies the underlying misconception.
  3. **Explain Algorithm (`explain_algorithm`)**: Explains optimal algorithmic intuition, step-by-step approach, time complexity ($O$), and space complexity ($O$).
  4. **Give Me a Hint (`hint`)**: Socratic tutor mode providing incremental conceptual clues without spoiling the solution.
  5. **Show Corrected Code (`corrected_code`)**: Delivers a clean, verified replacement Python 3 program with an explanation of surgical corrections.
- **Resilient Fallback**: Gracefully detects missing or unconfigured `GEMINI_API_KEY` credentials and provides actionable instructions without crashing the application.

---

## 3. Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Language** | Python | `3.14+` | Core backend runtime and analysis engine |
| **Backend API** | FastAPI | `0.162.0` | Asynchronous REST API framework |
| **ASGI Server** | Uvicorn | Standard | High-performance ASGI server |
| **Frontend UI** | Streamlit | `1.42+` | Dark-themed, reactive web interface |
| **Code Editor** | Monaco Editor | Custom Build | VS Code Monaco editor with event sync |
| **Database** | SQLite 3 | Embedded | Lightweight relational database |
| **ORM** | SQLAlchemy | `2.x` | Declarative models, connections & migrations |
| **Data Validation** | Pydantic | `v2` | Strict payload schema validation and size bounds |
| **HTTP Client** | HTTPX | Latest | Asynchronous client for external REST APIs |
| **AI Integration** | Google Gemini API | REST / v1beta | Diagnostic reasoning and Socratic hints |
| **Remote Judge** | OnlineCompiler.io | REST API | Cloud sandboxed Python code runner |
| **Testing** | Pytest | `9.2+` | Deterministic automated unit and integration tests |

---

## 4. Project Architecture

TraceBack maintains strict separation of concerns across a clean three-tier architecture:

```text
                      +-----------------------------+
                      |     Streamlit Frontend      |
                      |   (Port 8501 - app.py)      |
                      +--------------+--------------+
                                     |
                                HTTP | (BackendAPIClient via HTTPX)
                                     v
                      +-----------------------------+
                      |       FastAPI Backend       |
                      |  (Port 8000 - backend/main) |
                      +--------------+--------------+
                                     |
        +----------------------------+----------------------------+
        |                            |                            |
        v                            v                            v
+---------------+            +---------------+            +---------------+
| /problems     |            | /execute      |            | /ai/debug     |
| ProblemService|            |ExecutionServic|            |AIDebugService |
+-------+-------+            +-------+-------+            +-------+-------+
        |                            |                            |
        v                            v                            v
+---------------+            +---------------+            +---------------+
|  SQLite DB    |            |ProviderFactory|            | Google Gemini |
|  traceback.db |            +-------+-------+            | REST API      |
+---------------+                    |                    +---------------+
                           +---------+---------+
                           |                   |
                           v                   v
                    +--------------+   +---------------+
                    | MockProvider |   |OnlineCompiler |
                    | (Simulation) |   | (Cloud Judge) |
                    +--------------+   +---------------+
```

### Component Responsibilities
- **`frontend/`**: Streamlit presentation layer. Injects custom dark CSS, handles navigation state, embeds Monaco, and communicates with the backend via `BackendAPIClient`.
- **`backend/routes/`**: FastAPI route controllers validating inputs and returning canonical response schemas (`/execute`, `/problems`, `/ai`).
- **`backend/services/`**: Core business domain logic, orchestrating problem queries, remote execution dispatch, and AI prompt engineering.
- **`backend/services/providers/`**: Pluggable code execution system implementing `BaseExecutionProvider`.
- **`database/`**: SQLAlchemy SQLite connection pooling, declarative models (`Problem`, `ProblemExample`), and idempotent database seeding.

---

## 5. Directory Structure

```text
TraceBack/
├── .env.example                # Environment configuration template
├── .gitignore                  # Git exclusion rules (ignores secrets & databases)
├── LICENSE                     # MIT License
├── PROJECT_NOTES.md            # Technical engineering decisions & history
├── README.md                   # Comprehensive project documentation
├── requirements.txt            # Python dependencies
│
├── backend/                    # Core FastAPI backend application
│   ├── main.py                 # FastAPI application instance, lifespan & router mounting
│   ├── core/                   # Central configuration & domain exceptions
│   │   ├── config.py           # Pydantic/dotenv settings & bounds
│   │   └── exceptions.py       # Domain exceptions (Configuration, NotFound, Duplicate)
│   ├── integrations/           # External service clients
│   │   └── onlinecompiler_client.py # HTTPX client for OnlineCompiler.io
│   ├── models/                 # SQLAlchemy 2.x declarative ORM models
│   │   ├── __init__.py         # Model exports
│   │   └── problem.py          # Problem & ProblemExample table definitions
│   ├── routes/                 # REST API endpoints
│   │   ├── ai_debug.py         # POST /ai/debug endpoint
│   │   ├── execution.py        # POST /execute/run and /execute/submit
│   │   └── problems.py         # GET/POST /problems endpoints
│   ├── schemas/                # Pydantic request & response contracts
│   │   ├── ai_debug.py         # AIDebugRequest & AIDebugResponse
│   │   ├── execution.py        # Execution & submission schemas
│   │   ├── problem.py          # Problem create, detail, and summary schemas
│   │   └── system.py           # Health and root response schemas
│   └── services/               # Domain business logic
│       ├── ai_debug_service.py # Gemini prompt orchestration & fallbacks
│       ├── execution_service.py# Submission evaluation & runner orchestration
│       ├── problem_service.py  # Problem querying, pagination & search
│       └── providers/          # Pluggable execution providers
│           ├── base_provider.py# Abstract execution provider interface
│           ├── mock_provider.py# Safe offline simulation provider
│           ├── onlinecompiler_provider.py # Remote execution provider
│           └── provider_factory.py        # Provider resolution factory
│
├── database/                   # SQLite database engine & seed scripts
│   ├── base.py                 # DeclarativeBase foundation
│   ├── connection.py           # SessionLocal, engine, and init_db
│   └── seed.py                 # Idempotent 23-problem seed generator
│
├── frontend/                   # Streamlit user interface
│   ├── app.py                  # Streamlit entrypoint and page router
│   ├── api_client.py           # HTTPX backend API client
│   ├── config.py               # Theme constants & API URLs
│   ├── starter_templates.py    # Blank editor configuration & template migration
│   ├── styles.py               # Dark design system CSS injection
│   ├── components/             # Reusable UI components
│   │   ├── cards.py            # Dashboard metric cards & alert banners
│   │   ├── header.py           # Top navigation bar & live health dot
│   │   ├── monaco_editor.py    # Monaco custom component wrapper
│   │   ├── problem_card.py     # Problem row pills & difficulty badges
│   │   ├── sidebar.py          # Brand logo & navigation menu
│   │   └── monaco_build/       # Bundled Monaco React/JS artifacts
│   └── pages/                  # Main platform views
│       ├── coming_soon.py      # Placeholder for future roadmap features
│       ├── dashboard.py        # Analytics, KPI metrics & problem suggestions
│       ├── problem_detail.py   # Problem specifications & examples view
│       ├── problems.py         # Problem Library table with search & filters
│       └── workspace.py        # Split-screen coding workspace & AI drawer
│
└── tests/                      # Automated test suite (74 tests)
    ├── test_ai_debug_api.py    # AI assistant endpoint & schema validation tests
    ├── test_execution_api.py   # Run Code & Submit endpoint integration tests
    ├── test_frontend_api_client.py # Frontend HTTP client unit tests
    ├── test_frontend_workspace.py  # Workspace state, blank editor & draft tests
    ├── test_main.py            # API health & system route tests
    ├── test_mock_provider.py   # Mock execution provider safety tests
    ├── test_onlinecompiler_provider.py # OnlineCompiler integration tests
    └── test_problems_api.py    # Problem management, filtering & seeding tests
```

---

## 6. Installation & Setup

### Prerequisites
- Python 3.10 or higher (Python 3.14 recommended)
- Git

### Step 1: Clone the Repository
On **Windows (PowerShell)**:
```powershell
git clone https://github.com/Ashish-Ku-Rath/TraceBack.git
cd TraceBack
```

### Step 2: Create and Activate Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 7. Environment Configuration

TraceBack reads its configuration from a root `.env` file. A template `.env.example` is included in the repository.

### Create Your `.env` File
```powershell
Copy-Item .env.example .env
```

### Environment Variables Reference

| Variable | Default Value | Description |
|---|---|---|
| `EXECUTION_PROVIDER` | `mock` | `mock` for safe local simulation; `onlinecompiler` for real remote cloud execution. |
| `DATABASE_URL` | `sqlite:///./database/traceback.db` | SQLite database connection string. |
| `ONLINECOMPILER_API_URL` | `https://api.onlinecompiler.io` | REST endpoint for OnlineCompiler API. |
| `ONLINECOMPILER_API_KEY` | *(empty)* | API key for OnlineCompiler.io (required only if provider is `onlinecompiler`). |
| `ONLINECOMPILER_PYTHON_COMPILER` | `python-3.14` | Target Python compiler version for remote execution. |
| `ONLINECOMPILER_MAX_TESTS_PER_REQUEST` | `8` | Maximum custom tests evaluated per request. |
| `ONLINECOMPILER_DEFAULT_TIME_LIMIT` | `5` | Remote execution timeout in seconds. |
| `GEMINI_API_KEY` | *(empty)* | Google Gemini API key for AI Debug Assistant. |
| `GEMINI_MODEL` | `gemini-3.8-flash` | Gemini model name (`gemini-3.8-flash`, `gemini-2.5-flash`, etc.). |
| `GEMINI_TIMEOUT_SECONDS` | `30` | Network timeout for Gemini AI requests. |

---

## 8. Running the Application

### Step 1: Seed the Problem Database
Populate the SQLite database with all 23 initial programming problems:
```powershell
.\.venv\Scripts\Activate.ps1
python -m database.seed
```

### Step 2: Start the FastAPI Backend Server
In your first terminal window:
```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn backend.main:app --port 8000
```
- **API Documentation (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **API Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### Step 3: Start the Streamlit Frontend Web App
In a second terminal window:
```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run frontend/app.py --server.port 8501
```
- **Application URL**: [http://localhost:8501](http://localhost:8501)

---

## 9. Automated Testing

TraceBack includes a comprehensive, deterministic test suite containing **74 automated unit and integration tests**. All tests run offline using `httpx.MockTransport` and in-memory SQLite fixtures (`sqlite:///:memory:`).

To execute the test suite:
```powershell
.\.venv\Scripts\Activate.ps1
$env:EXECUTION_PROVIDER="mock"
python -m pytest -q tests
```

### Test Coverage Highlights
- **Backend Execution API**: Validation limits, byte bounds, execution responses, and submission judging.
- **Provider Architecture**: Confirms `MockProvider` never invokes `exec()`, `eval()`, or local subprocesses.
- **Problem API**: CRUD operations, difficulty filters, tag search, title search, pagination, and seed idempotency.
- **AI Debug API**: Request validation, schema parsing, unconfigured state handling, and fallback simulation.
- **Frontend Workspace**: Monaco editor configuration, blank-by-default initial state, session state caching, and template migrations.

---

## 10. AI Assistant Configuration (Google Gemini)

TraceBack integrates with Google's state-of-the-art Gemini generative models to act as an on-demand Socratic programming mentor.

### How to Obtain a Free Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google account.
3. Click **Get API key** and create a new key.
4. Copy your API key into your local `.env` file:
   ```ini
   GEMINI_API_KEY=AIzaSyYourActualKeyHere
   GEMINI_MODEL=gemini-3.8-flash
   ```

### Security & Privacy Mandates
- **Zero Secret Exposure**: The frontend never communicates directly with Google Gemini. All calls route through the authenticated FastAPI backend.
- **Never Committed**: `.env` is permanently excluded via `.gitignore`.
- **Offline & Unconfigured Grace**: If no key is set, the AI tab provides clear configuration guidance without throwing exceptions or disabling the coding editor.

---

## 11. REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API status and root greeting. |
| `GET` | `/health` | Healthcheck returning database and system status. |
| `GET` | `/problems` | List paginated problems with `difficulty`, `tag`, and `search` filters. |
| `GET` | `/problems/{id}` | Retrieve individual problem details with examples and constraints. |
| `GET` | `/problems/slug/{slug}` | Retrieve problem details by unique slug identifier. |
| `POST` | `/execute/run` | Execute Python code with custom stdin; returns stdout, stderr, execution time. |
| `POST` | `/execute/submit` | Evaluate code against all problem test cases; returns judge verdicts. |
| `POST` | `/execute/check-custom-tests` | Run code against custom test pairs in Custom Test Lab. |
| `POST` | `/ai/debug` | Request AI failure analysis and debugging guidance across 5 modes. |

---

## 12. License

This project is released under the MIT License.

---

## 13. Author

**Ashish Kumar Rath**  
- GitHub: [@Ashish-Ku-Rath](https://github.com/Ashish-Ku-Rath)
