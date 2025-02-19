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
