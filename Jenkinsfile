pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'mkhnoori1/house-price-prediction'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS = credentials('docker-cred')
        SCANNER_HOME = tool 'sonar-scanner'
        SONAR_PROJECT_KEY = 'house-price-prediction'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/mkhnoori/house-price-prediction-app.git'
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

        stage('Trivy File Scan') {
            steps {
                sh '''
                    trivy fs --format json --output trivy-fs-report.json .
                    echo "Trivy file scan completed. Check trivy-fs-report.json for results."
                    cat trivy-fs-report.json
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Trivy Image Scan') {
            steps {
                sh '''
                    trivy image --format json --output trivy-image-report.json \
                    --severity CRITICAL \
                    --exit-code 0 \
                    ${DOCKER_IMAGE}:${DOCKER_TAG}
                    echo "Trivy image scan completed. Check trivy-image-report.json for results."
                    cat trivy-image-report.json
                '''
            }
        }
        
        stage('Push Docker Image') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh '''
                            echo "${DOCKER_PASS}" | docker login -u ${DOCKER_USER} --password-stdin
                            docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                            docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                            docker push ${DOCKER_IMAGE}:latest
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts(
                artifacts: '**/trivy-*.json',
                allowEmptyArchive: true
            )
            cleanWs()
            sh 'docker system prune -f'
        }
    }
}
