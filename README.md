# TrackIt — Parcel Tracking System
**College DevOps Laboratory Project**  
*Academic Year 2025–2026*

---

## 📦 Project Overview & Syllabus Compliance (12/12 Completed)

**TrackIt** is a full-featured, enterprise-grade parcel tracking web application built to fulfill all 12 modules of the College DevOps Laboratory syllabus:

| Module # | Syllabus Requirement | Status | Primary Files & Deliverables |
| :---: | :--- | :---: | :--- |
| **1** | **Project setup and frontend** | ✅ **COMPLETE** | `templates/index.html`, `static/css/style.css`, `static/js/main.js` |
| **2** | **Flask backend** | ✅ **COMPLETE** | `app.py` (`/`, `/health`, query parameter parsing) |
| **3** | **SQLite database** | ✅ **COMPLETE** | `database.py`, `trackit.db` (Schema, Foreign Keys, Auto-seeding) |
| **4** | **Shipment tracking** | ✅ **COMPLETE** | 5-stage milestone stepper and reverse-chronological timeline |
| **5** | **Admin shipment management** | ✅ **COMPLETE** | `templates/admin/` (Login, KPI dashboard, Consignment intake, Status updates) |
| **6** | **Git and GitHub** | ✅ **COMPLETE** | Git repository, 5 feature branches, non-fast-forward (`--no-ff`) merges |
| **7** | **Automated testing** | ✅ **COMPLETE** | `tests/test_app.py`, `tests/test_database.py` (15/15 tests passing) |
| **8** | **Docker** | ✅ **COMPLETE** | `Dockerfile` (Python 3.12-slim, non-root user), `docker-compose.yml` |
| **9** | **Jenkins CI pipeline** | ✅ **COMPLETE** | `Jenkinsfile` (7 stages with JUnit test reporting and Ansible trigger) |
| **10** | **Ansible deployment** | ✅ **COMPLETE** | `ansible/inventory.ini`, `ansible/playbooks/deploy.yml`, `ansible/run_ansible.py` |
| **11** | **End-to-end integration** | ✅ **COMPLETE** | `scripts/verify_e2e_pipeline.py` (Automated 9-stage verification) |
| **12** | **Final demonstration** | ✅ **COMPLETE** | `DEVOPS_LAB_REPORT.md`, browser artifacts, screenshots, and viva guide |

---

## 🗂️ Project Directory Structure

```text
d:/devops project/
├── app.py                      # Flask backend, routes, session auth, and /health API
├── database.py                 # SQLite database layer, schema, CRUD, and KPI queries
├── trackit.db                  # Local SQLite database file
├── Dockerfile                  # Multi-stage production container specification (non-root user, Gunicorn)
├── docker-compose.yml          # Container orchestration with volume persistence & healthcheck
├── Jenkinsfile                 # Declarative 7-stage CI/CD pipeline specification
├── .dockerignore               # Docker build context exclusion rules
├── .gitignore                  # Git ignore rules for Python, venv, and cache files
├── pytest.ini                  # Pytest configuration file (pythonpath = .)
├── requirements.txt            # Python dependencies (Flask, Gunicorn, Pytest)
├── README.md                   # Repository overview and documentation
├── DEVOPS_LAB_REPORT.md        # Comprehensive laboratory manual and report
├── ansible/                    # Module 10: Ansible Deployment Automation
│   ├── ansible.cfg             # Ansible engine configuration
│   ├── inventory.ini           # Inventory defining local, staging, and production hosts
│   ├── run_ansible.py          # Cross-platform Ansible playbook execution engine
│   ├── vars/
│   │   └── deploy_vars.yml     # Application and deployment variables
│   └── playbooks/
│       ├── deploy.yml          # Automated application deployment playbook
│       ├── health_check.yml    # Standalone health verification playbook
│       └── rollback.yml        # Automated disaster recovery rollback playbook
├── scripts/
│   └── verify_e2e_pipeline.py  # Module 11: End-to-end integration test runner
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # Automated GitHub Actions CI/CD workflow
├── tests/                      # Module 7: Automated test suite (15 Tests)
│   ├── test_app.py             # HTTP routes, session auth, and CRUD integration tests
│   └── test_database.py        # Database schema, foreign keys, and logic unit tests
├── templates/
│   ├── index.html              # Public parcel tracking homepage & live search
│   └── admin/                  # Module 5: Admin console templates
│       ├── login.html          # Admin authentication portal
│       ├── dashboard.html      # KPI overview & shipment inventory table
│       ├── new_shipment.html   # Consignment intake registration form
│       └── update_shipment.html# Status update & milestone event logging form
└── static/
    ├── css/
    │   └── style.css           # Modern white-and-blue design system & pipeline tokens
    └── js/
        └── main.js             # Client-side quick-fill, tracking generator, and UI handlers
```

---

## 🔐 Administrative Access & Credentials

For academic and laboratory evaluation:
- **Admin Login URL:** `http://127.0.0.1:5000/login`
- **Username:** `admin`
- **Password:** `admin123`

---

## 🚀 Quick Start & Verification Commands

### 1. Run Automated Unit & Integration Tests (Module 7)
```powershell
.\venv\Scripts\pytest -v
```

### 2. Deploy Application via Ansible (Module 10)
```powershell
.\venv\Scripts\python ansible/run_ansible.py --playbook deploy.yml
```

### 3. Run Complete End-to-End Pipeline Verification (Module 11)
```powershell
.\venv\Scripts\python scripts/verify_e2e_pipeline.py
```

### 4. Inspect Git Branch Topology & Merges (Module 6)
```powershell
git log --graph --oneline --all
```

### 5. Inspect Running Docker Container (Module 8)
```powershell
docker ps
```

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

## 🎓 Viva Preparation Notes

Refer to [DEVOPS_LAB_REPORT.md](file:///d:/devops%20project/DEVOPS_LAB_REPORT.md) for 40+ comprehensive viva voce questions and answers covering Git, Docker, Jenkins, Ansible, SQLite, Pytest, and Linux fundamentals.
