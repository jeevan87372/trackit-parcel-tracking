# TrackIt — Parcel Tracking System
**College DevOps Laboratory Project**  
*Academic Year 2025–2026*

---

## 📦 Project Overview
**TrackIt** is a complete, modular web-based parcel tracking system developed as part of the College DevOps Laboratory curriculum. The project follows an iterative development methodology spanning all 4 core modules:
- **Module 1 (Completed):** Project directory setup, Flask application skeleton, responsive white-and-blue UI, tracking search bar, and sample status cards.
- **Module 2 (Completed):** Relational SQLite database integration (`trackit.db`), schema design (`shipments` and `tracking_updates`), parameterized SQL lookups, dynamic parcel tracking results, and chronological event timelines.
- **Module 3 (Completed):** Admin Authentication, Session Management, Operations Dashboard with KPI statistics, and Full CRUD Shipment Management (Consignment Intake, Status & Checkpoint Updates, and Deletions).
- **Module 4 (Completed & Active):** DevOps Containerization (Docker), Multi-Container Orchestration (Docker Compose), Automated Testing Suite (Pytest: 15/15 passed), and CI/CD Automation Pipelines (Declarative Jenkinsfile & GitHub Actions).

---

## 🗂️ Complete Project Directory Structure
```text
d:/devops project/
├── app.py                      # Flask entry point, routes, session auth, CRUD & /health API
├── database.py                 # SQLite database layer (parameterized queries, CRUD, KPI counts)
├── trackit.db                  # SQLite relational database file
├── Dockerfile                  # Multi-stage production container specification (non-root user, Gunicorn)
├── docker-compose.yml          # Container orchestration with volume persistence & healthcheck
├── Jenkinsfile                 # Declarative 7-stage CI/CD pipeline specification
├── .dockerignore               # Docker build context exclusion rules
├── .gitignore                  # Git ignore rules for Python, venv, and cache files
├── pytest.ini                  # Pytest configuration file (pythonpath = .)
├── requirements.txt            # Python dependencies (Flask, Gunicorn, Pytest)
├── README.md                   # Complete laboratory documentation & viva preparation guide
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # Automated GitHub Actions CI/CD workflow
├── tests/                      # Automated test suite (15 Unit & Integration tests)
│   ├── test_app.py             # HTTP endpoints, authentication, and CRUD workflow tests
│   └── test_database.py        # Database schema, foreign keys, and business logic tests
├── templates/
│   ├── index.html              # Public parcel tracking homepage & live search
│   └── admin/                  # Administrative operations console templates
│       ├── login.html          # Admin authentication portal
│       ├── dashboard.html      # KPI overview & shipment management data table
│       ├── new_shipment.html   # Parcel intake registration form (with ID generator)
│       └── update_shipment.html# Status update & milestone event logging form
└── static/
    ├── css/
    │   └── style.css           # Clean white-and-blue theme, admin styles & pipeline workflow
    └── js/
        └── main.js             # Client interactivity, ID generator, & live query handling
```

---

## 🔐 Administrative Access & Credentials

For academic and laboratory evaluation:
- **Admin Login URL:** `http://127.0.0.1:5000/login`
- **Username:** `admin`
- **Password:** `admin123`

---

## 🌐 Application Endpoints & Routes

| Endpoint | Method | Access | Purpose |
| :--- | :--- | :--- | :--- |
| `/` | `GET`, `POST` | Public | Homepage & live parcel search by tracking number |
| `/health` | `GET` | Public | Container health check & monitoring JSON endpoint |
| `/login` | `GET`, `POST` | Public | Admin authentication portal |
| `/logout` | `GET` | Admin | Clears session cookie and signs out |
| `/admin` | `GET` | Admin (`@admin_required`) | Operations console with KPIs and shipment inventory |
| `/admin/shipments/new` | `GET`, `POST` | Admin (`@admin_required`) | Consignment intake and initial checkpoint registration |
| `/admin/shipments/<id>/update` | `GET`, `POST` | Admin (`@admin_required`) | Advance milestone status and append milestone to timeline |
| `/admin/shipments/<id>/delete` | `POST` | Admin (`@admin_required`) | Deletes shipment and cascades timeline event history |

---

## 🧪 Module 4: Automated Testing Suite (Pytest)

The automated test suite in `tests/` contains **15 comprehensive unit and integration tests**:
- **Database Tests (`tests/test_database.py`):** Schema initialization, case-insensitive lookups, milestone auto-logging, duplicate prevention, status updates, cascading deletions, and KPI calculations.
- **Application & Route Tests (`tests/test_app.py`):** Public tracking rendering, valid/invalid search handling, `/health` JSON monitoring, `/favicon.ico` 204, unauthenticated route protection, admin login/logout, and end-to-end CRUD workflow.

### Running the Test Suite:
```powershell
# From project directory
.\venv\Scripts\pytest.exe -v
```

**Result:**
```text
tests/test_app.py::test_public_homepage_renders PASSED                   [  6%]
tests/test_app.py::test_public_search_valid_parcel PASSED                [ 13%]
tests/test_app.py::test_public_search_invalid_parcel PASSED              [ 20%]
tests/test_app.py::test_favicon_endpoint PASSED                          [ 26%]
tests/test_app.py::test_health_endpoint PASSED                           [ 33%]
tests/test_app.py::test_admin_route_unauthenticated_redirect PASSED      [ 40%]
tests/test_app.py::test_admin_login_failure PASSED                       [ 46%]
tests/test_app.py::test_admin_login_success_and_logout PASSED            [ 53%]
tests/test_app.py::test_admin_crud_workflow PASSED                       [ 60%]
tests/test_database.py::test_database_initialization PASSED              [ 66%]
tests/test_database.py::test_get_shipment_by_tracking_id_found PASSED    [ 73%]
tests/test_database.py::test_get_shipment_by_tracking_id_not_found PASSED [ 80%]
tests/test_database.py::test_get_shipment_updates_history PASSED         [ 86%]
tests/test_database.py::test_create_and_delete_shipment PASSED           [ 93%]
tests/test_database.py::test_kpi_stats_calculation PASSED                [100%]

============================= 15 passed in 0.67s ==============================
```

---

## 🐳 Module 4: Docker Containerization

The project includes an enterprise-grade `Dockerfile`:
- **Base Image:** `python:3.12-slim` (lightweight, minimal attack surface).
- **Security:** Creates a non-root system user (`appuser:appgroup`) with dedicated home directory `/app`.
- **WSGI Production Server:** Runs via **Gunicorn** (`gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 4 app:app`).
- **Healthcheck:** Automated 30-second container healthcheck probing `http://127.0.0.1:5000/`.

### 1. Build and Run Standalone Container:
```powershell
# Build image
docker build -t trackit:latest .

# Run container
docker run -d --name trackit-container -p 5000:5000 trackit:latest

# Check status and health
docker ps
```

### 2. Multi-Container Orchestration (Docker Compose):
```powershell
# Start with persistent volume and automatic restart
docker compose up -d

# Check service logs
docker compose logs

# Stop service
docker compose down
```

---

## 🔄 Module 4: CI/CD Pipeline Automation

### 1. Jenkins Pipeline (`Jenkinsfile`)
A declarative 7-stage Jenkins pipeline:
1. **Stage 1 (Checkout SCM):** Verifies Git checkout, Python version, and Docker availability.
2. **Stage 2 (Install Dependencies):** Prepares virtual environment and installs `requirements.txt`.
3. **Stage 3 (Code Quality & Linting):** Syntax validation with `py_compile` and static analysis.
4. **Stage 4 (Automated Testing):** Runs pytest with JUnit XML reporting (`--junitxml=reports/test-results.xml`).
5. **Stage 5 (Docker Build):** Compiles Docker image tagged with build number and `latest`.
6. **Stage 6 (Container Smoke Test):** Launches a test container on port 5050 and verifies HTTP 200 response.
7. **Stage 7 (Deploy Staging):** Deploys container service via `docker compose up -d`.

### 2. GitHub Actions (`.github/workflows/ci-cd.yml`)
Automated multi-job workflow triggered on every push and pull request:
- **Job 1 (test-and-lint):** Python 3.12 environment setup, pip caching, syntax checks, and pytest execution.
- **Job 2 (docker-build-and-test):** Docker Buildx image compilation and container smoke testing.

---

## 🎓 Viva Preparation Notes (Module 4)

### Q1: Why containerize with Docker instead of running directly on the host OS?
> **Answer:** Containerization eliminates the "it works on my machine" problem. Docker packages the application along with its exact Python runtime, dependencies (`requirements.txt`), system libraries, and configuration into an immutable container image. This guarantees identical behavior across developer laptops, Jenkins CI/CD servers, staging clusters, and production servers.

### Q2: Why use Gunicorn instead of Flask's built-in development server in Docker?
> **Answer:** Flask's built-in `app.run()` server is single-threaded, intended only for local development, and cannot handle concurrent traffic. **Gunicorn (Green Unicorn)** is a production-grade WSGI (Web Server Gateway Interface) HTTP server. It uses a master-worker process model (with multiple worker processes and threads) capable of handling concurrent requests efficiently, managing worker restarts on crashes, and providing production stability.

### Q3: Why is running the container as a non-root user important for security?
> **Answer:** By default, Docker containers run as `root` (UID 0). If an attacker discovers an application vulnerability (e.g., remote code execution), running as root would grant them superuser privileges inside the container, increasing the risk of container escape and compromising the host system. In our `Dockerfile`, we create and switch to a dedicated system user (`appuser`), following the principle of least privilege.

### Q4: What is the purpose of `.dockerignore`?
> **Answer:** When building a Docker image, Docker transfers the "build context" (files in the project directory) to the Docker daemon. `.dockerignore` excludes unnecessary files like `venv/`, `__pycache__/`, `.git/`, and `.pytest_cache/`. This drastically speeds up build times, keeps the final image size minimal, and prevents sensitive files from being baked into the image.

### Q5: How does the CI/CD pipeline ensure quality before deployment?
> **Answer:** The pipeline implements automated **Quality Gates**:
> 1. Code is checked out from version control.
> 2. Syntax validation ensures no uncompilable Python files.
> 3. Pytest executes 15 automated test cases covering authentication, database lookups, and business logic.
> 4. If ANY test fails, the pipeline immediately halts, blocking the build from progressing.
> 5. Only when tests pass is the Docker image compiled and smoke-tested before deployment.

### Q6: How does SQLite database data persist across container restarts?
> **Answer:** Containers are ephemeral by default (data written inside a container is lost when the container is deleted). In `docker-compose.yml`, we define a named volume `trackit-data:/app/data` and configure `TRACKIT_DB_PATH=/app/data/trackit.db`. Docker manages this volume on the host filesystem independently of the container lifecycle, ensuring parcel data is preserved across container updates and restarts.
