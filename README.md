# E-commerce App using Microservices

*This README provides a comprehensive guide to setting up, running, and deploying the e-commerce application, ensuring seamless integration with Docker, Docker-Compose, and Kubernetes for efficient microservices management and scalability.*

---

## Overview

This project is an e-commerce platform built using microservices architecture. It consists of multiple services handling functionalities such as user authentication, product catalog, and cart management. To ensure scalability, reliability, and efficient deployment, we utilize Docker, Docker-Compose, and Kubernetes.

### Technologies Used:
- **Flask:** For building APIs.
- **PostgreSQL:** Database management system.
- **Pgadmin4:** PostgreSQL administration tool.
- **Docker:** Containerization of services.
- **Docker-compose:** Management of containers.
- **Docker Hub:** Repository for Docker images.
- **Kubernetes (on Minikube):** Orchestration of containers.
- **Postman:** Tool for testing APIs.

---

## Project Structure

Each service is isolated in a separate file, which includes:

- **Dockerfile:** Instructions for building Docker images.
- **ConfigMap:** Configuration data for the service.
- **Deployment and Service for Kubernetes:** Kubernetes configuration files.
- **app.py:** Flask-based APIs implementation.
- **models.py:** Database table definitions (using PostgreSQL).
- **requirements.txt:** Dependency list for setting up the environment inside Docker containers.

---

## How to Use the Project

1. **Pull Docker Images:**
   - Pull the required Docker images for services and PostgreSQL:
     ```
     docker pull omaraliii1/cloud:<tag-service-name>
     docker pull postgres
     ```

2. **Run PostgreSQL Container:**
   - Run PostgreSQL container on port 5432:
     ```
     docker run -d -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=1234 --name my-postgres -p 5432:5432 postgres
     ```

3. **Run Services with Docker:**
   - Start each service container, specifying the exposed ports:
     ```
     docker run -d -p 5000:5000 omaraliii1/cloud:auth_v1
     docker run -d -p 5001:5001 omaraliii1/cloud:account_v1
     docker run -d -p 5002:5002 omaraliii1/cloud:product_v1
     ```

4. **Test APIs Using Postman:**
   - Utilize Postman to test the exposed APIs.

---

## Kubernetes Deployment

1. **Start Minikube:**
   - Ensure Minikube is running:
     ```
     minikube start
     ```

2. **Apply Deployments and ConfigMaps:**
   - Apply the Kubernetes deployment and configmap files for each service:
     ```
     kubectl apply -f <file>-deployment.yml
     kubectl apply -f <file>-configmap.yml
     ```

3. **Apply Services:**
   - Apply Kubernetes service configuration for each service:
     ```
     kubectl apply -f <file>-service.yml
     ```

4. **Access Services via Minikube:**
   - Retrieve the IP and nodePort of services using:
     ```
     minikube service <service-name>
     ```

---

