# E-commerce App using Microservices

*This README provides a comprehensive guide to setting up, running, and deploying the e-commerce application, ensuring seamless integration with Docker, Docker-Compose, and Kubernetes for efficient microservices management and scalability.*

---

## Overview

This project is an e-commerce platform built using microservices architecture. It consists of multiple services handling functionalities such as user authentication, product catalog, and cart management. To ensure scalability, reliability, and efficient deployment, we utilize Docker, Docker-Compose, and Kubernetes.

### Technologies Used:
- **Flask:** For building APIs.
- **PostgreSQL:** Database management system.
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

1. **Clone the Repository:**
   - Clone the repository to your local machine:
     ```sh
     git clone https://github.com/your-repo/ecommerce-app.git
     cd ecommerce-app
     ```

2. **Create a Docker-Compose File:**
   - Create a `docker-compose.yml` file with the following content:

     ```yaml
     version: '3.8'

     services:
       postgres:
         image: postgres
         environment:
           POSTGRES_USER: postgres
           POSTGRES_PASSWORD: 1234
         ports:
           - "5432:5432"
         volumes:
           - postgres-data:/var/lib/postgresql/data

       auth_service:
         image: omaraliii1/cloud:auth_v1
         ports:
           - "5000:5000"
         depends_on:
           - postgres

       account_service:
         image: omaraliii1/cloud:account_v1
         ports:
           - "5001:5001"
         depends_on:
           - postgres

       product_service:
         image: omaraliii1/cloud:product_v1
         ports:
           - "5002:5002"
         depends_on:
           - postgres

     volumes:
       postgres-data:
     ```

3. **Run Docker-Compose:**
   - Start all services using Docker-Compose:
     ```sh
     docker-compose up -d
     ```

4. **Check Running Containers:**
   - Verify that all containers are running:
     ```sh
     docker-compose ps
     ```

5. **Test APIs Using Postman:**
   - Utilize Postman to test the exposed APIs.

---

## Kubernetes Deployment

1. **Start Minikube:**
   - Ensure Minikube is running:
     ```sh
     minikube start
     ```

2. **Apply Deployments and ConfigMaps:**
   - Apply the Kubernetes deployment and configmap files for each service:
     ```sh
     kubectl apply -f <file>-deployment.yml
     kubectl apply -f <file>-configmap.yml
     ```

3. **Apply Services:**
   - Apply Kubernetes service configuration for each service:
     ```sh
     kubectl apply -f <file>-service.yml
     ```

4. **Access Services via Minikube:**
   - Retrieve the IP and nodePort of services using:
     ```sh
     minikube service <service-name>
     ```

---
