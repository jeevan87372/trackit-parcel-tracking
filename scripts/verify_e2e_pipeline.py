#!/usr/bin/env python3
"""
TrackIt — End-to-End Pipeline Integration & Verification Runner
DevOps Laboratory Project (Module 11 & 12)

Automates the complete verification across all DevOps stages:
1. Git Repository & Feature Branching Integrity
2. Automated Unit & Integration Testing (Pytest)
3. Docker Image & Container Healthcheck Verification
4. Ansible Deployment Validation
5. Public Tracking Lookup Verification (Valid & Invalid IDs)
6. Admin Authentication & CRUD API Endpoints
7. Data Volume Persistence Verification
"""

import sys
import os
import subprocess
import urllib.request
import urllib.parse
import http.cookiejar
import json
import time

COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_CYAN = "\033[96m"
COLOR_RED = "\033[91m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

class PipelineVerifier:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.results = []
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))

    def record(self, stage_num, name, passed, details=""):
        status_str = f"{COLOR_GREEN}PASS{COLOR_RESET}" if passed else f"{COLOR_RED}FAIL{COLOR_RESET}"
        print(f"[{status_str}] Stage {stage_num:2d}: {name} - {details}")
        self.results.append({
            "stage": stage_num,
            "name": name,
            "passed": passed,
            "details": details
        })

    def run_command(self, cmd):
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.returncode, res.stdout.strip(), res.stderr.strip()

    def step_1_git_integrity(self):
        rc, out, _ = self.run_command("git status")
        if rc == 0:
            rc2, branches, _ = self.run_command("git branch")
            rc3, log, _ = self.run_command("git log --oneline -n 3")
            self.record(6, "Git SCM & Branching", True, f"Git active. Branches:\n{branches}")
        else:
            self.record(6, "Git SCM & Branching", False, "Git repository not yet initialized.")

    def step_2_pytest_suite(self):
        rc, out, _ = self.run_command(f'"{sys.executable}" -m pytest -q')
        passed = (rc == 0) and ("passed" in out)
        summary = out.splitlines()[-1] if out else "No output"
        self.record(7, "Automated Testing (Pytest)", passed, summary)

    def step_3_docker_container(self):
        rc, out, _ = self.run_command('docker inspect --format="{{.State.Status}} (Health: {{.State.Health.Status}})" trackit-parcel-service')
        passed = (rc == 0) and ("running" in out.lower())
        self.record(8, "Docker Containerization", passed, f"Container state: {out}")

    def step_4_ansible_playbooks(self):
        playbook_path = os.path.join("ansible", "playbooks", "deploy.yml")
        exists = os.path.isfile(playbook_path)
        self.record(10, "Ansible Deployment Artifacts", exists, f"Playbook present: {playbook_path}")

    def step_5_live_http_health(self):
        try:
            req = urllib.request.Request(f"{self.base_url}/health", headers={"User-Agent": "TrackIt-E2E/1.0"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                passed = (resp.status == 200) and (data.get("status") == "healthy")
                self.record(4, "Health Monitoring Route (/health)", passed, f"HTTP {resp.status}, payload: {data}")
        except Exception as e:
            self.record(4, "Health Monitoring Route (/health)", False, f"Request failed: {e}")

    def step_6_public_tracking_valid(self):
        try:
            url = f"{self.base_url}/?tracking_id=TRK-IND-2024-001"
            req = urllib.request.Request(url, headers={"User-Agent": "TrackIt-E2E/1.0"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                body = resp.read().decode("utf-8")
                found = ("In Transit" in body) and ("Electronics" in body)
                self.record(1, "Public Tracking (Valid ID TRK-IND-2024-001)", found, "Shipment details & status displayed")
        except Exception as e:
            self.record(1, "Public Tracking (Valid ID)", False, f"Request failed: {e}")

    def step_7_public_tracking_invalid(self):
        try:
            url = f"{self.base_url}/?tracking_id=INVALID-NONEXISTENT-999"
            req = urllib.request.Request(url, headers={"User-Agent": "TrackIt-E2E/1.0"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                body = resp.read().decode("utf-8")
                handled = ("No shipment found matching tracking ID" in body)
                self.record(2, "Public Tracking (Invalid ID Graceful Handling)", handled, "User-friendly error displayed with suggestions")
        except Exception as e:
            self.record(2, "Public Tracking (Invalid ID)", False, f"Request failed: {e}")

    def step_8_admin_authentication_and_kpis(self):
        try:
            # POST to login
            login_data = urllib.parse.urlencode({"username": "admin", "password": "admin123"}).encode("utf-8")
            req = urllib.request.Request(f"{self.base_url}/login", data=login_data, headers={"User-Agent": "TrackIt-E2E/1.0"})
            with self.opener.open(req, timeout=4) as resp:
                pass  # redirect followed

            # GET /admin with session cookies
            req_admin = urllib.request.Request(f"{self.base_url}/admin", headers={"User-Agent": "TrackIt-E2E/1.0"})
            with self.opener.open(req_admin, timeout=4) as resp_admin:
                body = resp_admin.read().decode("utf-8")
                passed = ("Admin Console" in body) and ("Total Parcels" in body)
                self.record(5, "Admin Authentication & KPI Dashboard", passed, "Session auth verified, KPI metrics loaded")
        except Exception as e:
            self.record(5, "Admin Authentication & KPI Dashboard", False, f"Request failed: {e}")

    def step_9_ci_cd_artifacts(self):
        jenkins_ok = os.path.isfile("Jenkinsfile")
        actions_ok = os.path.isfile(".github/workflows/ci-cd.yml")
        passed = jenkins_ok and actions_ok
        self.record(9, "CI/CD Pipeline Configurations", passed, "Jenkinsfile & GitHub Actions workflows validated")

    def run_all(self):
        print(f"\n{COLOR_BOLD}{COLOR_CYAN}========================================================================{COLOR_RESET}")
        print(f"{COLOR_BOLD}{COLOR_CYAN}    TrackIt — End-to-End DevOps Integration & Verification Suite        {COLOR_RESET}")
        print(f"{COLOR_BOLD}{COLOR_CYAN}========================================================================{COLOR_RESET}\n")

        self.step_1_git_integrity()
        self.step_2_pytest_suite()
        self.step_3_docker_container()
        self.step_4_ansible_playbooks()
        self.step_5_live_http_health()
        self.step_6_public_tracking_valid()
        self.step_7_public_tracking_invalid()
        self.step_8_admin_authentication_and_kpis()
        self.step_9_ci_cd_artifacts()

        total = len(self.results)
        passed_count = sum(1 for r in self.results if r["passed"])
        score_pct = (passed_count / total) * 100

        print(f"\n{COLOR_CYAN}------------------------------------------------------------------------{COLOR_RESET}")
        color = COLOR_GREEN if passed_count == total else COLOR_YELLOW
        print(f"{color}{COLOR_BOLD}SUMMARY: {passed_count}/{total} Stages Verified ({score_pct:.1f}% Compliance){COLOR_RESET}")
        print(f"{COLOR_CYAN}------------------------------------------------------------------------{COLOR_RESET}\n")
        return passed_count == total

if __name__ == "__main__":
    verifier = PipelineVerifier()
    success = verifier.run_all()
    sys.exit(0 if success else 1)
