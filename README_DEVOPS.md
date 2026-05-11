# DSA Visualizer — DevOps Pipeline Guide

Complete DevOps pipeline for deploying the Pygame-based DSA Visualizer to the web using X11 + noVNC.

## 🏗️ Architecture

```
User Browser → noVNC (WebSockets) → websockify → x11vnc → Xvfb → Pygame (Python)
```

```
GitHub → Jenkins CI/CD → Docker Hub → Terraform (AWS EC2) → Kubernetes → Prometheus/Grafana
```

## 🐳 Docker (Local Test)

```bash
# Build the image
docker build -t dsa-visualizer .

# Run the container
docker run -p 6080:6080 dsa-visualizer

# Open in browser
# http://localhost:6080/vnc.html → Click "Connect"
```

## ☸️ Kubernetes Deployment

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

# Access via NodePort
# http://<Node-IP>:30080/vnc.html
```

## 👷 Jenkins CI/CD

1. Create a **Pipeline** job in Jenkins.
2. Link it to: `https://github.com/VardhanVarikuti/dsa-visualizer`
3. Configure credentials:
   - `dockerhub-credentials`: DockerHub username/password
   - `kubeconfig`: Kubernetes config file

**Pipeline Stages**: Checkout → Build Docker Image → Push to DockerHub → Deploy to Kubernetes

## 🌍 Terraform (AWS Infrastructure)

```bash
cd terraform
terraform init
terraform apply -var="key_name=your-aws-key-pair"
```

**Provisions**: EC2 `t3.medium` in `ap-south-1` (Mumbai) with security groups for SSH (22), noVNC (6080), and NodePort (30080).

## 📊 Monitoring Stack

```bash
cd monitoring
docker compose -f docker-compose-monitoring.yml up -d
```

| Service | Port | URL |
|---|---|---|
| Prometheus | 9090 | `http://localhost:9090` |
| Grafana | 3000 | `http://localhost:3000` (admin/admin) |
| Node Exporter | 9100 | `http://localhost:9100/metrics` |

## 🔄 GitHub Actions CI

Automated on every push to `main`:
- Checks out code
- Sets up Python 3.11
- Installs Pygame
- Runs import test

## 📁 DevOps File Structure

```
├── Dockerfile                    # X11 + noVNC container
├── Jenkinsfile                   # CI/CD pipeline
├── scripts/start.sh              # Container entrypoint
├── kubernetes/
│   ├── deployment.yaml           # K8s Deployment (1 replica)
│   └── service.yaml              # NodePort Service (30080)
├── terraform/
│   ├── main.tf                   # AWS EC2 + Security Groups
│   ├── variables.tf              # Region, instance type, AMI
│   └── outputs.tf                # Public IP output
├── monitoring/
│   ├── prometheus.yml            # Scrape config
│   └── docker-compose-monitoring.yml  # Prometheus + Grafana + Node Exporter
└── .github/workflows/ci.yml     # GitHub Actions
```

## 🛠️ Setup Order

1. **Push to GitHub**
2. **Terraform**: Provision AWS EC2 instance
3. **SSH into EC2**: Install Docker + Kubernetes
4. **Jenkins**: Configure credentials and run pipeline
5. **Monitoring**: Start Prometheus + Grafana stack
6. **Access**: `http://<EC2-Public-IP>:30080/vnc.html`
