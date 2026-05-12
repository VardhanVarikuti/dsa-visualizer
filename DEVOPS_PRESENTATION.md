# 🚀 DSA Visualizer: DevOps & Cloud Architecture

This document summarizes the DevOps infrastructure, automation, and cloud deployment strategies implemented for the DSA Visualizer project.

---

## 🏗️ Architectural Overview
The DSA Visualizer is not just a desktop application; it is a **Cloud-Native, Headless GUI** system. It uses a virtual framebuffer to render graphics on a server and streams them to the browser via noVNC.

### Key Challenges Solved:
1.  **GUI in Cloud**: Running a Pygame (SDL) app on a server without a physical monitor.
2.  **Scalability**: Handling multiple users through Kubernetes orchestration.
3.  **Automation**: Continuous Integration and Deployment (CI/CD) from code to production.

---

## 🛠️ Toolstack & Rationale

| Tool | Purpose | Why We Used It? |
| :--- | :--- | :--- |
| **Docker** | Containerization | Packages the app with its OS-level GUI dependencies (X11, Xvfb, SDL) to run identically everywhere. |
| **Xvfb & noVNC** | Headless Streaming | `Xvfb` provides a virtual display; `noVNC` translates the VNC protocol to WebSockets for browser access. |
| **Terraform** | Infrastructure as Code | Automates the creation of AWS resources (VPC, Security Groups, EC2/EKS) ensuring consistent environments. |
| **Kubernetes (K8s)** | Orchestration | Manages container lifecycles, health checks, and scaling. |
| **Jenkins** | CI/CD | Automates the build-test-push-deploy lifecycle on every code change. |
| **Prometheus & Grafana** | Monitoring | Provides real-time metrics on CPU, Memory, and application health. |

---

## 📦 Containerization (Docker)
The `Dockerfile` builds a custom Linux environment that includes a lightweight window manager (**Fluxbox**) and a virtual display server.

**Key Command:**
```bash
# Build and tag the image
docker build -t dsa-visualizer .

# Run locally to test the web interface
docker run -p 6080:6080 dsa-visualizer
```

---

## 🌍 Infrastructure as Code (Terraform)
We use Terraform to manage AWS resources in the `ap-south-1` (Mumbai) region. This prevents "Configuration Drift" and allows us to tear down and rebuild infrastructure in minutes.

**Essential Ports Opened:**
*   `22`: SSH for management.
*   `6080`: noVNC (Visualizer access).
*   `8080`: Jenkins dashboard.
*   `3000/9090`: Monitoring (Grafana/Prometheus).

**Key Commands:**
```bash
terraform init    # Initialize providers
terraform plan    # Preview changes
terraform apply   # Deploy to AWS
```

---

## 🔄 CI/CD Pipeline (Jenkins)
The `Jenkinsfile` defines a multi-stage pipeline that runs in a Kubernetes Pod:
1.  **Checkout**: Pulls code from GitHub.
2.  **Build**: Creates the Docker image.
3.  **Push**: Pushes the image to DockerHub (`varikutivardhan/dsa-visualizer`).
4.  **Deploy**: Updates the Kubernetes deployment with the new image.

---

## ☸️ Orchestration (Kubernetes)
The application is deployed as a **Deployment** with a **Service** (NodePort/LoadBalancer).

**Key Commands:**
```bash
# Apply configurations
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

# Check status
kubectl get pods
kubectl get service dsa-visualizer-service
```

---

## 📊 Observability (Monitoring)
We use a sidecar pattern or separate deployment for monitoring.
*   **Prometheus**: Scrapes metrics from the cluster.
*   **Grafana**: Visualizes the metrics in a premium dashboard.

---

## 🏁 Summary for Presentation
"Our project demonstrates a modern DevOps lifecycle: we treat our infrastructure like code with **Terraform**, our environment like a package with **Docker**, and our delivery like a factory line with **Jenkins**. By utilizing **Xvfb**, we bridge the gap between legacy desktop GUI applications and modern cloud-native web accessibility."
