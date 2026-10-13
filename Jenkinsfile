// =============================================================================
// TrackIt — Parcel Tracking System (DevOps Laboratory Project)
// Module 4: Declarative Jenkins CI/CD Pipeline Specification (Jenkinsfile)
// =============================================================================

pipeline {
    agent any

    environment {
        APP_NAME     = 'trackit-app'
        IMAGE_NAME   = "trackit:${env.BUILD_NUMBER}"
        LATEST_IMAGE = "trackit:latest"
        APP_PORT     = "5000"
    }

    options {
        // Stop execution if any stage exceeds 15 minutes
        timeout(time: 15, unit: 'MINUTES')
        // Colorize console output
        ansiColor('xterm')
    }

    stages {
        // ---------------------------------------------------------------------
        // STAGE 1: Code Checkout & Environment Verification
        // ---------------------------------------------------------------------
        stage('Checkout SCM') {
            steps {
                echo '=== [Stage 1] Checking out source code and validating environment ==='
                checkout scm
                sh 'git status'
                sh 'python3 --version || python --version'
                sh 'docker --version'
            }
        }

        // ---------------------------------------------------------------------
        // STAGE 2: Dependency Resolution & Environment Setup
        // ---------------------------------------------------------------------
        stage('Install Dependencies') {
            steps {
                echo '=== [Stage 2] Setting up virtual environment & installing dependencies ==='
                sh '''
                    python3 -m venv venv || python -m venv venv
                    . venv/bin/activate || . venv/Scripts/activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }

        // ---------------------------------------------------------------------
        // STAGE 3: Static Analysis & Code Linting
        // ---------------------------------------------------------------------
        stage('Code Quality & Linting') {
            steps {
                echo '=== [Stage 3] Executing syntax validation and code inspection ==='
                sh '''
                    . venv/bin/activate || . venv/Scripts/activate
                    python -m py_compile app.py database.py
                    echo "Python syntax validation passed successfully."
                '''
            }
        }

        // ---------------------------------------------------------------------
        // STAGE 4: Automated Testing & Test Reporting
        // ---------------------------------------------------------------------
        stage('Run Unit & Integration Tests') {
            steps {
                echo '=== [Stage 4] Running automated test suite with pytest ==='
                sh '''
                    . venv/bin/activate || . venv/Scripts/activate
                    pytest -v --junitxml=reports/test-results.xml
                '''
            }
            post {
                always {
                    // Archive and publish JUnit XML test results in Jenkins UI
                    junit testResults: 'reports/test-results.xml', allowEmptyResults: true
                }
            }
        }

        // ---------------------------------------------------------------------
        // STAGE 5: Docker Container Image Build
        // ---------------------------------------------------------------------
        stage('Docker Build') {
            steps {
                echo '=== [Stage 5] Building production Docker container image ==='
                sh """
                    docker build -t ${IMAGE_NAME} -t ${LATEST_IMAGE} .
                """
            }
        }

        // ---------------------------------------------------------------------
        // STAGE 6: Container Smoke Test & Security Verification
        // ---------------------------------------------------------------------
        stage('Container Smoke Test') {
            steps {
                echo '=== [Stage 6] Running smoke tests on live container instance ==='
                sh """
                    # Spin up temporary container on test port 5050
                    docker run -d --name trackit-smoketest -p 5050:5000 ${IMAGE_NAME}
                    sleep 5
                    
                    # Verify HTTP endpoint returns 200 OK
                    curl -f http://127.0.0.1:5050/ || python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5050/')"
                    echo "Smoke test passed: Container responded with HTTP 200 OK."
                    
                    # Clean up smoke test container
                    docker rm -f trackit-smoketest
                """
            }
        }

        // ---------------------------------------------------------------------
        // STAGE 7: Ansible Automated Deployment (Local / Staging Environment)
        // ---------------------------------------------------------------------
        stage('Ansible Deployment') {
            steps {
                echo '=== [Stage 7] Deploying application container via Ansible Automation ==='
                sh '''
                    if command -v ansible-playbook >/dev/null 2>&1; then
                        ansible-playbook -i ansible/inventory.ini ansible/playbooks/deploy.yml
                    else
                        python3 ansible/run_ansible.py --playbook deploy.yml || python ansible/run_ansible.py --playbook deploy.yml
                    fi
                    echo "TrackIt Parcel Tracking System deployed successfully via Ansible."
                '''
            }
        }
    }

    // -------------------------------------------------------------------------
    // POST-BUILD ACTIONS
    // -------------------------------------------------------------------------
    post {
        success {
            echo "SUCCESS: Pipeline build #${env.BUILD_NUMBER} completed without errors!"
        }
        failure {
            echo "FAILURE: Pipeline build #${env.BUILD_NUMBER} failed. Check stage logs."
        }
        always {
            echo '=== Pipeline Execution Completed ==='
        }
    }
}
