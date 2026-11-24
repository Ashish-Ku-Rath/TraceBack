# TraceBack — Architectural Project Notes & Engineering Blueprint

This document details the architectural decisions, component responsibilities, dependency roles, communication protocols, and execution workflows designed for **TraceBack — The Intelligent Coding & Debugging Assistant**.

---

## 1. Directory Responsibilities & Boundary Separation

```text
TraceBack/
├── frontend/                   # Frontend presentation layer (Streamlit 1.66+)
│   ├── app.py                  # Entrypoint & router
│   ├── api_client.py           # BackendAPIClient
│   ├── config.py               # Theme constants & brand logo
│   ├── styles.py               # Custom CSS design system
│   ├── components/             # Sidebar, Header, Cards, ProblemCard
│   └── pages/                  # Dashboard, Problems, ProblemDetail, ComingSoon
├── backend/                    # Core application backend (FastAPI)
│   ├── core/                   # Settings, bounds, and domain exceptions
│   ├── integrations/           # External service clients (OnlineCompiler REST API)
│   ├── models/                 # SQLAlchemy 2.x ORM models (Problem, ProblemExample)
│   ├── routes/                 # API controllers (/execute, /problems, /system)
│   ├── schemas/                # Pydantic validation contracts (Execution, Problem, System)
│   ├── services/               # Orchestrators and pluggable providers (ProblemService, ExecutionService)
│   │   └── providers/          # BaseExecutionProvider, MockProvider, OnlineCompilerProvider
│   └── main.py                 # FastAPI application instance, lifespan & routing
├── database/                   # SQLite database engine, Base, connection, and seeding
├── tests/                      # Automated test suite (Pytest & TestClient - 51 tests)
├── .env.example                # Template for required environment variables
├── .gitignore                  # Git exclusion rules
├── requirements.txt            # Python package dependencies
├── README.md                   # Comprehensive project documentation
└── PROJECT_NOTES.md            # Architectural decisions and technical notes
```

---

## 2. Pluggable Execution Architecture

To support offline local development, automated testing without external dependencies, and real remote execution, TraceBack implements a provider-independent execution architecture:

```text
                           +------------------------+
                           |   FastAPI Controller   |
                           |  POST /execute/run     |
                           |  POST /execute/check   |
                           +-----------+------------+
                                       |
                                       v
                           +------------------------+
                           |    ExecutionService    |
                           +-----------+------------+
                                       |
                                       v
                           +------------------------+
                           |    ProviderFactory     |
                           +-----------+------------+
                                       |
                     +-----------------+-----------------+
                     |                                   |
                     v                                   v
        +-------------------------+         +-------------------------+
        |      MockProvider       |         | OnlineCompilerProvider  |
        | - Simulated responses   |         | - Remote HTTP client    |
        | - Never executes code   |         | - Real sandboxed cloud  |
        | - is_simulated: True    |         | - Normalized schemas    |
        +-------------------------+         +-------------------------+
```

### A. Execution Provider Interface (`BaseExecutionProvider`)
Both providers inherit from `BaseExecutionProvider` which mandates:
- `run_code(request: RunCodeRequest) -> RunCodeResponse`: Executes source code with custom standard input.
- `run_tests(request: CustomTestCheckRequest) -> CustomTestCheckResponse`: Evaluates code against multiple test cases and returns verdicts.

### B. Mock Provider (`MockProvider`)
- **Safety Guarantee**: `MockProvider` **NEVER** executes user-submitted code locally. Calls to `exec()`, `eval()`, or local subprocesses are strictly forbidden.
- **Purpose**: Provides immediate, deterministic synthetic responses for frontend and API integration during development.
- **Simulation Control**: Inspects code comments for explicit directives:
  - `# mock:wrong_answer` / `# mock:wa` $\rightarrow$ Simulates `wrong_answer` verdict.
  - `# mock:runtime_error` / `# mock:re` $\rightarrow$ Simulates `runtime_error` with synthetic traceback.
  - `# mock:time_limit_exceeded` / `# mock:tle` $\rightarrow$ Simulates `time_limit_exceeded`.
  - `# mock:compilation_error` / `# mock:ce` $\rightarrow$ Simulates `compilation_error`.
  - Default $\rightarrow$ Simulates successful execution (`status="success"` or `verdict="accepted"`).
- **Transparency**: Every mock response returns `"is_simulated": true` and `"provider": "mock"`.
- **Limitation**: Synthetic responses do not evaluate actual algorithm correctness or measure physical compute performance. Real validation requires the remote OnlineCompiler provider.

### C. OnlineCompiler Provider (`OnlineCompilerProvider`)
- **Endpoint 1 (Run Code)**: `POST https://api.onlinecompiler.io/api/run-code-sync/`
  - Sends: `{"compiler": "python-3.14", "code": "...", "input": "...", "time_limit": 5}`
  - Receives: `output`, `error`, `status`, `exit_code`, `signal`, `time`, `memory`, `truncated`.
- **Endpoint 2 (Custom Tests)**: `POST https://api.onlinecompiler.io/api/run-tests/`
  - Sends: `{"compiler": "python-3.14", "code": "...", "tests": [...], "checker": "trim", "time_limit": 5, "scoring": "all_or_nothing"}`
  - Receives: `verdict`, `score`, `passed`, `total`, `time_limit`, `compile_error`, `tests`.
- **Authentication**: Pass raw API key directly in HTTP `Authorization` header (`Authorization: <api_key>`).
- **Hidden Test Cases**: Safely preserves hidden test status without fabricating missing output or error strings.

---

## 3. Provider Factory & Switching

The execution provider is selected via the environment variable `EXECUTION_PROVIDER`:
- `EXECUTION_PROVIDER=mock` (default): Resolves to `MockProvider`.
- `EXECUTION_PROVIDER=onlinecompiler`: Resolves to `OnlineCompilerProvider`.

### Strict Factory Rules:
1. If `EXECUTION_PROVIDER=onlinecompiler` is configured but `ONLINECOMPILER_API_KEY` is missing or empty, `ProviderFactory` raises `ConfigurationError`.
2. The system **never silently switches** from OnlineCompiler to MockProvider if a remote execution fails, ensuring that execution failures are transparently diagnosed rather than masked by simulated data.
3. The frontend is agnostic to provider selection; switching providers requires zero frontend code modifications.

---

## 4. Run Code vs. Custom Test Lab Workflows

### Run Code Workflow (`POST /execute/run`)
- Purpose: Free-form code execution with arbitrary `stdin`.
- Architectural Principle: A successful execution (`exit_code == 0`) represents process success, **not** an accepted algorithm solution. Correctness evaluation occurs exclusively in test evaluation.

### Custom Test Lab Workflow (`POST /execute/check-custom-tests`)
- Purpose: Multi-test evaluation where users define inputs and expected outputs.
- Supported Checkers:
  - `trim` (default): Trims trailing whitespace and newlines before comparing.
  - `exact`: Exact character-by-character comparison.
  - `tokens`: Whitespace-separated token comparison.
  - `float`: Numerical comparison with floating-point tolerance.
  - `rows`: Line-by-line comparison ignoring trailing line breaks.
- Returns detailed per-test results (`actual_output`, `error`, `verdict`, `execution_time`, `memory_kb`).

---

## 5. Security & Boundary Enforcement

1. **Zero Host Execution**: The server host machine is completely isolated from user code. All code is either simulated safely in `MockProvider` or delegated remotely to OnlineCompiler's isolated sandbox.
2. **Payload Bounds & Validation**:
   - `source_code`: Max 100 KB UTF-8 bytes.
   - `stdin`: Max 100 KB UTF-8 bytes.
   - `expected_output` per test: Max 64 KB UTF-8 bytes.
   - Combined test payload size: Max 512 KB UTF-8 bytes.
   - Tests per request: Max 8 (configurable).
   - Execution time: 1 to 30 seconds.
   - Rejection of NUL characters (`\x00`).
3. **Credential Protection**:
   - API keys are never logged, never exposed in JSON responses, and never printed in exception messages.
   - `.env` is strictly ignored by Git.

---

## 6. Problem Management & Relational Database Architecture (Day 3)

In Milestone 3 (Day 3), TraceBack introduces a relational problem management subsystem using SQLite and SQLAlchemy 2.x declarative models.

```text
                            +--------------------------+
                            |       HTTP Request       |
                            +------------+-------------+
                                         |
                                         v
                            +--------------------------+
                            |  FastAPI Router Layer    |
                            |  backend/routes/         |
                            |  - problems.py           |
                            +------------+-------------+
                                         |  Validates Pydantic Schemas
                                         v  Injects get_db Session
                            +--------------------------+
                            |      Service Layer       |
                            |  backend/services/       |
                            |  - problem_service.py    |
                            +------------+-------------+
                                         |  Translates queries & filters
                                         v  Handles slug uniqueness
                            +--------------------------+
                            |   SQLAlchemy 2.x ORM     |
                            |  backend/models/         |
                            |  - Problem               |
                            |  - ProblemExample        |
                            +------------+-------------+
                                         |  Executes parameterized SQL
                                         v
                            +--------------------------+
                            |     SQLite Database      |
                            |  database/traceback.db   |
                            +--------------------------+
```

### A. Database Entity Models (`backend/models/problem.py`)

#### 1. `Problem` Entity (`problems` table)
- `id`: Integer primary key, autoincrementing.
- `title`: String(255), required.
- `slug`: String(255), unique, indexed, required. URL-friendly identifier.
- `description`: Text, required problem statement.
- `difficulty`: String(50), indexed, required. Normalized to `Easy`, `Medium`, or `Hard`.
- `constraints`: Text, algorithmic input and execution bounds.
- `tags`: JSON array of categories (e.g. `["Array", "Hash Map"]`).
- `created_at`: DateTime (UTC), auto-populated with `func.now()`.
- `updated_at`: DateTime (UTC), auto-updated on change.
- `examples`: 1-to-many relationship with `ProblemExample` (cascading delete).

#### 2. `ProblemExample` Entity (`problem_examples` table)
- `id`: Integer primary key, autoincrementing.
- `problem_id`: Integer foreign key referencing `problems.id` with `ondelete="CASCADE"`, indexed.
- `input`: Text, required sample input string.
- `expected_output`: Text, required sample expected output.
- `explanation`: Text, optional conceptual rationale for the sample case.
- `problem`: Many-to-1 relationship back to `Problem`.

*Crucial Boundary Rule*: Public sample examples are intended exclusively for UI problem description rendering. They are **never** treated as official hidden judging test suites.

### B. Problem Service Layer (`backend/services/problem_service.py`)
- Decouples database interaction from API routing controllers.
- `create_problem`: Ensures slug uniqueness and inserts problem + examples in a single transaction.
- `get_problems`: Supports multi-criteria filtering:
  - Difficulty filter (`func.lower(Problem.difficulty) == difficulty.lower()`).
  - Category tag search (cast JSON to string with case-insensitive `like`).
  - Title keyword search (`func.lower(Problem.title).like("%search%")`).
  - Pagination offset and limit (`offset(skip).limit(limit)`).
- `count_problems`: Computes total matching records for the `X-Total-Count` HTTP response header.
- `get_problem_by_id`: Retrieves problem with eager-loaded examples.
- `get_problem_by_slug`: Retrieves problem by unique slug.

### C. Idempotent Database Seeding (`database/seed.py`)
- Provides 3 initial classic DSA problems:
  1. **Two Sum** (Easy) — Array, Hash Map (3 public examples)
  2. **Reverse String** (Easy) — String, Two Pointers (2 public examples)
  3. **Valid Parentheses** (Medium) — String, Stack (3 public examples)
- *Idempotency Guarantee*: The seed mechanism queries each problem by slug before insertion. Existing records are skipped, preventing duplication across repeated server boots or test setups.

---

## 7. Frontend Architecture & UI Design System (Day 4)

In Milestone 4 (Day 4), TraceBack implements a complete frontend client using Streamlit 1.66+ and a bespoke dark CSS design system.

```text
+-----------------------------------------------------------------------------------------+
|                                Streamlit Frontend Application                            |
|                                     frontend/app.py                                     |
+-----------------------------------------------------------------------------------------+
       |                                           |                                  |
       v                                           v                                  v
+------------------+                    +--------------------+             +--------------------+
| Sidebar & Brand  |                    | Header & Indicator |             | View Controllers   |
| components/      |                    | components/        |             | pages/             |
| - sidebar.py     |                    | - header.py        |             | - dashboard.py     |
|   `</TraceBack>` |                    |   (Live /health    |             | - problems.py      |
|   Nav Menu       |                    |    Pulsing Dot)    |             | - problem_detail.py|
+------------------+                    +--------------------+             | - coming_soon.py   |
                                                                           +--------------------+
                                                                                      |
                                                                                      v
                                                                           +--------------------+
                                                                           | Backend API Client |
                                                                           | frontend/          |
                                                                           | - api_client.py    |
                                                                           |   (HTTPX Sync)     |
                                                                           +--------------------+
                                                                                      |
                                                                                      v
                                                                           +--------------------+
                                                                           | FastAPI REST API   |
                                                                           | http://127.0.0.1   |
                                                                           | :8000              |
                                                                           +--------------------+
```

### A. Design System Tokens & Coded Theme (`frontend/styles.py` & `frontend/config.py`)
- **Proportions**: ~80% black/charcoal (`#080B12`, `#0D111B`), ~15% dark navy (`#131A27`, `#192235`), ~5% accent (`#8B5CF6`, `#3B82F6`).
- **Typography**: Inter / system monospace fallback, strict contrast standards (`#F8FAFC` primary, `#94A3B8` secondary).
- **Difficulty Badges**:
  - Easy: `#22C55E` text with `rgba(34, 197, 94, 0.15)` background.
  - Medium: `#F59E0B` text with `rgba(245, 158, 11, 0.15)` background.
  - Hard: `#EF4444` text with `rgba(239, 68, 68, 0.15)` background.
- **Card Containers**: Subtly rounded (10px–16px), restrained borders (`#273449`), no overwhelming neon glow.

### B. Client Layer & Resilience (`frontend/api_client.py`)
- `BackendAPIClient` encapsulates all HTTP communication via `httpx.Client(timeout=5.0)`.
- Reusable methods:
  - `check_health()`: Probes `GET /health` to drive the top-bar live status pill.
  - `get_problems(skip, limit, difficulty, tag, search)`: Queries `GET /problems` with sanitized filters.
  - `get_problem_by_id(id)` / `get_problem_by_slug(slug)`: Queries detailed problem schemas.
  - `get_statistics()`: Computes real database KPI metrics (never hardcodes or invents user data).
- Graceful offline fallback: If FastAPI is not running or network fails, an informative offline banner with the exact command to start FastAPI is displayed without crashing the Streamlit UI.

---

## 8. MVP Architectural Components (Days 5 & 6)

### A. Monaco Editor Zero-Rerun Architecture
- **Root Cause of Prior Instability**: The standard `streamlit-monaco` package hardcoded continuous debounced `setComponentValue(e)` calls on every keystroke (`onChange`). Because Streamlit reruns the Python script upon receiving component value updates, typing triggered continuous full app reruns, black screen flickering, and cursor reset to the end of the text.
- **TraceBack Solution**:
  1. Replaced with uncontrolled editor model (`defaultValue: o.value`), so Streamlit parent rerenders do not alter the client model or move the cursor.
  2. Removed automatic keystroke and blur event dispatches to Python.
  3. Installed event-driven synchronization: capture-phase click listeners on the parent window for `▶ Run Code`, `Submit`, and `💾 Save Draft`, alongside a Monaco command for `Ctrl+S`.
  4. Result: 0 Streamlit reruns during active typing; seamless and deterministic state synchronization on user action.

### B. Problem Submission & Automated Judge (`POST /execute/submit`)
- Queries test cases (`ProblemExample`) from SQLite database.
- Dispatches code and test suites to the configured `ExecutionProvider` (`OnlineCompilerProvider` or `MockProvider`).
- Evaluates test outcomes, computes execution times, and aggregates results into normalized verdicts: `ACCEPTED`, `WRONG_ANSWER`, or `RUNTIME_ERROR`.

### C. Google Gemini AI Debugging Assistant (`POST /ai/debug`)
- Diagnostic AI assistant service (`backend/services/ai_debug_service.py`).
- Inspects code, error message, stdin, stdout, and stderr.
- Pinpoints root cause, explains the algorithmic failure, identifies the faulty lines, and provides a surgical code fix.
- Gracefully handles unconfigured `GEMINI_API_KEY` by returning clear configuration instructions without crashing the app.

---

## 9. How to Run, Test, and Access the Applications

### 1. Starting the FastAPI Backend
```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn backend.main:app --port 8000
```

### 2. Starting the Streamlit Frontend
```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run frontend/app.py --server.port 8501
```

### 3. Seeding Initial Problems
```powershell
.\.venv\Scripts\Activate.ps1
python -m database.seed
```

### 4. Running the Automated Test Suite
```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest -v
```
All 72 automated tests run deterministically offline without external network dependency:
- 28 execution and judging tests using `httpx.MockTransport` and DB fixtures.
- 16 problem management tests using isolated in-memory SQLite (`sqlite:///:memory:`).
- 11 frontend API client unit tests verifying query construction, error handling, submit client, and AI debug client.
- 13 frontend workspace tests verifying Monaco configuration, session state caching, templates, and execution state.
- 4 AI Debugging Assistant tests verifying error diagnosis schemas, simulated fallbacks, and unconfigured states.
