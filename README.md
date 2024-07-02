# E-commerce App using Microservices

_This README provides a comprehensive guide to setting up, running, and deploying the e-commerce application, ensuring seamless integration with Docker, Docker-Compose, and Kubernetes for efficient microservices management and scalability._

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
- **Deployment and Service for Kubernetes:** Kubernetes configuration files.
- **app.py:** Flask-based APIs implementation.
- **models.py:** Database table definitions (using PostgreSQL).
- **requirements.txt:** Dependency list for setting up the environment inside Docker containers.

---

## How to Use the Project

**Clone the Repository:**
   - Clone the repository to your local machine:
     ```sh
     git clone https://github.com/omaraliii1/e-commerce-using-microservices.git
     cd e-commerce-using-microservices
     ```

## Run Using Docker
1. **Run Docker-Compose:**

- Start all services using Docker-Compose:
  ```sh
  docker-compose up -d
  ```

2. **Check Running Containers:**

- Verify that all containers are running:
    ```sh
    docker-compose ps
    ```

- If there any errors occurs while running the containers, you can debug using:

  ```sh
  docker-compose logs
  ```

3. **Test APIs Using Postman:**

---

## Deploy to K8s Cluster

1. **Start Minikube:**

  - Ensure Minikube is running:
    ```sh
    minikube start
    ```

2. **Apply Deployments and ConfigMaps:**

  - Apply the Kubernetes deployment and configmap files for each service (in each file I wrote a script to apply all changes on the cluster):
    ```sh
    ./script
    ../account/script.sh
    ../auth/script.sh
    ../product/script.sh
    ```
  - Now all (Deployments, Services and configMaps) were applied  

3. **Add Database Queries**
  - Open db-init.sql, Copy all content of it then do the following:

    ```sh
    kubectl exec -it <postgres-pod> -- bash
    psql -U postgres 
    \c cloud <!--select our database-->
    **paste all the content on db-init.sql and hit enter**
    ``` 
  - Now you have created all the tables manually in the postgres pod
 
4. **Access Services via Minikube to test APIs:**
  - Retrieve the IP and nodePort of services using:
     ```sh
     minikube service account --> will return the IP:port of the account service 

     minikube service auth --> will return the IP:port of the auth service 

     minikube service product --> will return the IP:port of the product service 
     ```

---
