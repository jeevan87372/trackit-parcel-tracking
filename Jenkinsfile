// =============================================================================
// TrackIt — Parcel Tracking System (DevOps Laboratory Project)
// Declarative Jenkins CI/CD Pipeline Specification (Jenkinsfile)
// Cross-Platform Engine: Auto-detects Linux (sh) vs Windows (bat)
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
    }

    stages {
        // ---------------------------------------------------------------------
        // STAGE 1: Code Checkout & Environment Verification
        // ---------------------------------------------------------------------
        stage('Checkout SCM') {
            steps {
                echo '=== [Stage 1] Checking out source code and validating environment ==='
                checkout scm
                script {
                    if (isUnix()) {
                        sh 'git status && docker --version'
                    } else {
                        bat 'git status && docker --version'
                    }
                }
            }
        }

        // ---------------------------------------------------------------------
        // STAGE 2: Dependency Resolution & Environment Setup
        // ---------------------------------------------------------------------
        stage('Install Dependencies') {
            steps {
                echo '=== [Stage 2] Setting up virtual environment & installing dependencies ==='
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv venv || python -m venv venv
                            . venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            if not exist venv (
                                py -m venv venv || python -m venv venv
                            )
                            call venv\\Scripts\\activate.bat
                            python -m pip install --upgrade pip
                            python -m pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        // ---------------------------------------------------------------------
        // STAGE 3: Static Analysis & Code Linting
        // ---------------------------------------------------------------------
        stage('Code Quality & Linting') {
            steps {
                echo '=== [Stage 3] Executing syntax validation and code inspection ==='
                script {
                    if (isUnix()) {
                        sh '''
                            . venv/bin/activate
                            python -m py_compile app.py database.py
                            echo "Python syntax validation passed successfully."
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate.bat
                            python -m py_compile app.py database.py
                            echo Python syntax validation passed successfully.
                        '''
                    }
                }
            }
        }

        // ---------------------------------------------------------------------
        // STAGE 4: Automated Testing & Test Reporting
        // ---------------------------------------------------------------------
        stage('Run Unit & Integration Tests') {
            steps {
                echo '=== [Stage 4] Running automated test suite with pytest ==='
                script {
                    if (isUnix()) {
                        sh '''
                            . venv/bin/activate
                            pytest -v --junitxml=reports/test-results.xml
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate.bat
                            pytest -v --junitxml=reports/test-results.xml
                        '''
                    }
                }
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
                script {
                    if (isUnix()) {
                        sh "docker build -t ${IMAGE_NAME} -t ${LATEST_IMAGE} ."
                    } else {
                        bat "docker build -t ${IMAGE_NAME} -t ${LATEST_IMAGE} ."
                    }
                }
            }
        }

        // ---------------------------------------------------------------------
        // STAGE 6: Container Smoke Test & Security Verification
        // ---------------------------------------------------------------------
        stage('Container Smoke Test') {
            steps {
                echo '=== [Stage 6] Running smoke tests on live container instance ==='
                script {
                    if (isUnix()) {
                        sh """
                            docker rm -f trackit-smoketest 2>/dev/null || true
                            docker run -d --name trackit-smoketest -p 5055:5000 ${IMAGE_NAME}
                            sleep 5
                            curl -f http://127.0.0.1:5055/ || python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5055/')"
                            docker rm -f trackit-smoketest
                        """
                    } else {
                        bat """
                            docker rm -f trackit-smoketest >nul 2>&1 || ver >nul
                            docker run -d --name trackit-smoketest -p 5055:5000 ${IMAGE_NAME}
                            timeout /t 5 /nobreak >nul
                            docker inspect --format="{{.State.Status}}" trackit-smoketest
                            docker rm -f trackit-smoketest
                        """
                    }
                }
            }
        }

        // ---------------------------------------------------------------------
        // STAGE 7: Ansible Automated Deployment
        // ---------------------------------------------------------------------
        stage('Ansible Deployment') {
            steps {
                echo '=== [Stage 7] Deploying application container via Ansible Automation ==='
                script {
                    if (isUnix()) {
                        sh '''
                            if command -v ansible-playbook >/dev/null 2>&1; then
                                ansible-playbook -i ansible/inventory.ini ansible/playbooks/deploy.yml
                            else
                                python3 ansible/run_ansible.py --playbook deploy.yml || python ansible/run_ansible.py --playbook deploy.yml
                            fi
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate.bat
                            python ansible\\run_ansible.py --playbook deploy.yml
                        '''
                    }
                }
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
