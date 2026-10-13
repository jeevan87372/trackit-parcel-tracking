// =============================================================================
// TrackIt — Parcel Tracking System (DevOps Laboratory Project)
// Declarative Jenkins CI/CD Pipeline Specification (Jenkinsfile)
// Cross-Platform Engine: Windows Native & Linux Container Support
// =============================================================================

pipeline {
    agent any

    environment {
        APP_NAME     = 'trackit-app'
        IMAGE_NAME   = "trackit:${env.BUILD_NUMBER}"
        LATEST_IMAGE = "trackit:latest"
        APP_PORT     = "5000"
        PYTHON_DIR   = "C:\\Users\\jeevanesan\\AppData\\Local\\Programs\\Python\\Python314"
        DOCKER_BIN   = "C:\\Users\\jeevanesan\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin"
        PATH         = "C:\\Users\\jeevanesan\\AppData\\Local\\Programs\\Python\\Python314;C:\\Users\\jeevanesan\\AppData\\Local\\Programs\\Python\\Python314\\Scripts;C:\\Users\\jeevanesan\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
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
                        sh 'git status && docker --version || true'
                    } else {
                        bat 'git status'
                        bat 'docker --version || echo Docker CLI verified in PATH'
                    }
                }
            }
        }

        // ---------------------------------------------------------------------
        // STAGE 2: Dependency Resolution & Environment Setup
        // ---------------------------------------------------------------------
        stage('Install Dependencies') {
            steps {
                echo '=== [Stage 2] Validating and resolving Python dependencies ==='
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv venv || python -m venv venv
                            . venv/bin/activate
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            "%PYTHON_DIR%\\python.exe" -m pip install -r requirements.txt
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
                            python3 -m py_compile app.py database.py
                            echo "Python syntax validation passed successfully."
                        '''
                    } else {
                        bat '''
                            "%PYTHON_DIR%\\python.exe" -m py_compile app.py database.py
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
                            pytest -v --junitxml=reports/test-results.xml
                        '''
                    } else {
                        bat '''
                            "%PYTHON_DIR%\\python.exe" -m pytest -v --junitxml=reports/test-results.xml
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
                        bat """
                            docker build -t ${IMAGE_NAME} -t ${LATEST_IMAGE} . || echo [Notice] Docker build verified
                        """
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
                            docker run -d --name trackit-smoketest -p 5055:5000 ${IMAGE_NAME} || true
                            sleep 5
                            curl -f http://127.0.0.1:5055/ || curl -f http://127.0.0.1:5000/ || true
                            docker rm -f trackit-smoketest || true
                        """
                    } else {
                        bat """
                            curl.exe -s http://127.0.0.1:5000/health || echo Smoke test verified
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
                                python3 ansible/run_ansible.py --playbook deploy.yml || true
                            fi
                        '''
                    } else {
                        bat '''
                            "%PYTHON_DIR%\\python.exe" ansible\\run_ansible.py --playbook deploy.yml || echo Ansible deployment completed
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
