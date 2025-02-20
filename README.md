# House Price Prediction Application

A machine learning application that predicts house prices based on various features using a trained linear regression model. The application is containerized and deployed using Kubernetes and ArgoCD.

## Project Structure
```
house-price-prediction-app/
├── app/                    # Application directory
├── data/                   # Data directory
├── models/                 # Model training and storage
│   ├── AmesHousing.csv    # Training dataset
│   ├── train_model.py     # Model training script
├── k8s-deployment/        # Kubernetes deployment files
│   ├── namespace.yml      # Namespace configuration
│   ├── deployment.yml     # Deployment configuration
│   ├── service.yml        # Service configuration
├── Dockerfile             # Docker image configuration
├── requirements.txt       # Python dependencies
└── main.py               # Streamlit application
```

## Prerequisites
- Python 3.9+
- Docker
- Kubernetes cluster
- ArgoCD installed on the cluster
- DockerHub account

## Local Development

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Train the model:
```bash
cd models
python train_model.py
```

4. Run the Streamlit app:
```bash
streamlit run main.py
```

## Docker Build and Push

1. Build the Docker image:
```bash
docker build -t mkhnoori1/house-price-prediction:latest .
```

2. Login to DockerHub:
```bash
docker login
```

3. Push the image:
```bash
docker push mkhnoori1/house-price-prediction:latest
```

## Kubernetes Deployment with ArgoCD

### 1. Prepare the Kubernetes Manifests
The application uses three main Kubernetes manifests:
- `namespace.yml`: Creates a dedicated namespace
- `deployment.yml`: Configures the application deployment
- `service.yml`: Exposes the application

### 2. Deploy with ArgoCD

1. Create an ArgoCD application:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: house-price-prediction
  namespace: argocd
spec:
  project: default
  source:
    repoURL: <your-git-repo-url>
    path: k8s-deployment
    targetRevision: HEAD
  destination:
    server: https://kubernetes.default.svc
    namespace: house-price-prediction
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

2. Apply the ArgoCD application:
```bash
kubectl apply -f application.yml -n argocd
```

### 3. Access the Application

Once deployed, the application will be available through the LoadBalancer service. Get the external IP:
```bash
kubectl get svc -n house-price-prediction
```

## Application Features

The application provides a user-friendly interface to predict house prices based on:
- Lot Area
- Overall Quality
- Year Built
- Total Basement Square Footage
- First Floor Square Footage
- Full Bathrooms
- Ground Living Area
- Garage Cars

## Model Information

- Type: Linear Regression
- Features: 8 key house characteristics
- Training Data: Ames Housing dataset
- Preprocessing: Standard scaling and median imputation
- Performance Metrics:
  - MAE: Approximately $25,020
  - RMSE: Approximately $39,696

## Deployment Features

- High Availability: 2 replicas
- Zero-downtime deployments with RollingUpdate strategy
- Resource management with requests and limits
- Health monitoring with readiness and liveness probes
- Automated synchronization with ArgoCD
- LoadBalancer service type for external access

## Monitoring and Maintenance

The application includes:
- Health endpoints at `/_stcore/health`
- Resource monitoring through Kubernetes
- Automated healing through ArgoCD
- Rolling updates for zero-downtime deployments

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## Jenkins Pipeline Setup

The project includes a comprehensive CI/CD pipeline implemented in Jenkins. Here's how to set it up and use it:

### Prerequisites

1. Jenkins server with the following plugins installed:
   - Docker Pipeline
   - SonarQube Scanner
   - Credentials Plugin
   - Pipeline Utility Steps
   - Trivy Scanner

2. Required tools:
   - Docker
   - SonarQube
   - Trivy

### Jenkins Credentials Setup

1. Create Docker Hub credentials:
   - Go to Jenkins > Manage Jenkins > Credentials > System > Global credentials
   - Click "Add Credentials"
   - Choose "Username with password"
   - ID: `docker-cred`
   - Add your Docker Hub username and password

2. Configure SonarQube:
   - Install SonarQube Scanner tool in Jenkins
   - Configure SonarQube server URL in Jenkins configuration
   - Name the SonarQube installation as 'SonarQube'

### Jenkinsfile Implementation

Our pipeline is implemented in a declarative Jenkinsfile with the following structure:

```groovy
pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'mkhnoori1/house-price-prediction'
        DOCKER_TAG = "${BUILD_NUMBER}"
        SCANNER_HOME = tool 'sonar-scanner'
        SONAR_PROJECT_KEY = 'house-price-prediction'
    }
    
    stages {
        // Stages implementation
    }
    
    post {
        always {
            // Post-build actions
        }
    }
}
```

### Stage Details

1. **Checkout Stage**
   ```groovy
   stage('Checkout') {
       steps {
           git branch: 'main', url: 'https://github.com/mkhnoori/house-price-prediction-app.git'
       }
   }
   ```
   - Clones the repository from GitHub
   - Uses the main branch

2. **SonarQube Analysis Stage**
   ```groovy
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
   ```
   - Uses SonarQube environment
   - Configures Python-specific settings
   - Waits for analysis completion

3. **Quality Gate Stage**
   ```groovy
   stage('Quality Gate') {
       steps {
           timeout(time: 5, unit: 'MINUTES') {
               waitForQualityGate abortPipeline: true
           }
       }
   }
   ```
   - 5-minute timeout
   - Fails pipeline if quality gate fails

4. **Trivy File Scan Stage**
   ```groovy
   stage('Trivy File Scan') {
       steps {
           sh '''
               trivy fs --format json --output trivy-fs-report.json .
               echo "Trivy file scan completed. Check trivy-fs-report.json for results."
               cat trivy-fs-report.json
           '''
       }
   }
   ```
   - Scans project files
   - Outputs results in JSON format
   - Displays results in console

5. **Build Docker Image Stage**
   ```groovy
   stage('Build Docker Image') {
       steps {
           script {
               docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
           }
       }
   }
   ```
   - Uses Docker Pipeline plugin
   - Tags image with build number

6. **Trivy Image Scan Stage**
   ```groovy
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
   ```
   - Scans Docker image
   - Focuses on critical vulnerabilities
   - Non-blocking scan (exit-code 0)

7. **Push Docker Image Stage**
   ```groovy
   stage('Push Docker Image') {
       when {
           expression {
               currentBuild.result == null || currentBuild.result == 'SUCCESS'
           }
       }
       steps {
           withCredentials([usernamePassword(credentialsId: 'docker-cred', 
                          usernameVariable: 'DOCKER_USER', 
                          passwordVariable: 'DOCKER_PASS')]) {
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
   ```
   - Conditional execution
   - Secure credential handling
   - Pushes both versioned and latest tags

### Post-Build Actions
```groovy
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
```
- Archives scan reports
- Cleans workspace
- Removes unused Docker resources

### Required Jenkins Configuration

1. **Plugins**
   - Docker Pipeline
   - SonarQube Scanner
   - Credentials Binding

2. **Tools**
   - SonarQube Scanner configured as 'sonar-scanner'
   - Docker installed on Jenkins agent
   - Trivy installed on Jenkins agent

3. **Credentials**
   - Docker Hub credentials stored as 'docker-cred'
   - SonarQube configured in Jenkins

### Pipeline Features

- **Security**
  - Secure credential handling
  - Multiple security scans
  - No hardcoded secrets

- **Reliability**
  - Quality gates
  - Conditional stages
  - Proper error handling

- **Maintainability**
  - Modular stage design
  - Clear stage dependencies
  - Comprehensive artifact archival

### Troubleshooting

Common issues and solutions:

1. **Docker Login Fails**
   - Verify Docker Hub credentials in Jenkins
   - Ensure credential ID matches Jenkinsfile

2. **SonarQube Analysis Fails**
   - Check SonarQube server is running
   - Verify scanner configuration
   - Check project key is correct

3. **Trivy Scan Fails**
   - Ensure Trivy is installed on Jenkins server
   - Check file permissions
   - Verify JSON output format

### Best Practices

1. **Security**
   - Never store credentials in Jenkinsfile
   - Use Jenkins credentials manager
   - Regular security scans

2. **Maintenance**
   - Regular pipeline updates
   - Monitor scan results
   - Keep dependencies updated
