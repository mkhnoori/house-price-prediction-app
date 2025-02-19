pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'mkhnoori1/house-price-prediction'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS = credentials('docker-cred')
        SCANNER_HOME = tool 'sonar-scanner'
        SONAR_PROJECT_KEY = 'house-price-prediction'
        PYTHON_HOME = tool 'Python3'
    }
    
    tools {
        // Use the exact name configured in Jenkins
        python 'Python3'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/mkhnoori1/house-price-prediction-app.git'
                    ]]
                ])
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Set Python path
                    env.PATH = "${PYTHON_HOME}/bin:${env.PATH}"
                    
                    sh '''
                        # Verify Python installation
                        python3 --version
                        
                        # Create virtual environment
                        python3 -m venv .venv
                        
                        # Activate virtual environment and install dependencies
                        . .venv/bin/activate
                        python -m pip install --upgrade pip wheel setuptools
                    '''
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    . .venv/bin/activate
                    # Install project dependencies
                    pip install -r requirements.txt
                    pip install pytest pytest-cov bandit
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m pytest --junitxml=test-results.xml \
                        --cov=. \
                        --cov-report=xml \
                        --cov-report=html
                '''
            }
            post {
                always {
                    junit(
                        allowEmptyResults: true,
                        testResults: 'test-results.xml'
                    )
                    publishCoverage(
                        adapters: [coberturaAdapter(path: 'coverage.xml')],
                        sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                    )
                    publishHTML(
                        target: [
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: 'htmlcov',
                            reportFiles: 'index.html',
                            reportName: 'Coverage Report'
                        ]
                    )
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        ${SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.sources=. \
                        -Dsonar.python.coverage.reportPaths=coverage.xml \
                        -Dsonar.python.version=3.11 \
                        -Dsonar.qualitygate.wait=true
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Security Scan - Python') {
            steps {
                sh '''
                    . .venv/bin/activate
                    bandit -r . -f json -o bandit-report.json
                '''
            }
            post {
                always {
                    recordIssues(
                        enabledForFailure: true,
                        tool: bandit(pattern: 'bandit-report.json'),
                        qualityGates: [[threshold: 1, type: 'TOTAL_HIGH', unstable: true]]
                    )
                }
            }
        }

        stage('Trivy File Scan') {
            steps {
                sh '''
                    trivy fs --format json --output trivy-fs-report.json .
                '''
            }
            post {
                always {
                    recordIssues(
                        enabledForFailure: true,
                        tool: trivy(pattern: 'trivy-fs-report.json'),
                        qualityGates: [[threshold: 1, type: 'TOTAL_HIGH', unstable: true]]
                    )
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }
        
        stage('Trivy Image Scan') {
            steps {
                sh '''
                    trivy image --format json --output trivy-image-report.json \
                    --severity HIGH,CRITICAL \
                    --exit-code 1 \
                    ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
            post {
                always {
                    recordIssues(
                        enabledForFailure: true,
                        tool: trivy(pattern: 'trivy-image-report.json'),
                        qualityGates: [[threshold: 1, type: 'TOTAL_HIGH', unstable: true]]
                    )
                }
            }
        }
        
        stage('Push Docker Image') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-cred') {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts(
                artifacts: '**/trivy-*.json, **/bandit-report.json, coverage.xml, test-results.xml',
                allowEmptyArchive: true
            )
            cleanWs()
            sh 'docker system prune -f'
        }
    }
}