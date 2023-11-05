# researchAgent R0D1

## Description

The `researchAgent` is designed to streamline and automate various research tasks. It takes in user questions and employs advanced web scraping and natural language processing (NLP) techniques to search the internet for the most relevant and accurate information. The results are presented with concise key point summaries and URL evidence, helping researchers significantly enhance their research efficiency., helping researchers significantly enhance their research efficiency.

The `researchAgent` project is an autonomous research agent powered by `Flask API`. The end-to-end pipeline from `Docker` containerization, image push to `AWS ECR`, and deployment to `AWS ECS Fargate` with a `load balancer` is fully automated with `Github Actions`.

## CI/CD Deployment Logs:

- [Build and Push Flask Image to AWS ECR](https://github.com/HieuFromWaterloo/researchAgent/actions/workflows/main_ecr.yaml)
- [Deploy to ECS Fargate](https://github.com/HieuFromWaterloo/researchAgent/actions/workflows/main_ecs.yaml)

---

## Technologies

The Agent project leverages a range of cutting-edge technologies to provide a high-performance machine learning service at scale, and with high availability and security. Here are the key benefits of using these technologies:

### 1. Docker Containerization

- **Isolation:** Docker containers encapsulate the application and its dependencies, ensuring consistent behavior across different environments.

- **Portability:** Containers can run on any system that supports Docker, making it easy to move and deploy applications.

- **Resource Efficiency:** Docker containers are lightweight and share the host OS kernel, reducing resource overhead.

### 2. AWS ECR (Elastic Container Registry)

- **Managed Container Registry:** AWS ECR provides a secure and scalable container registry for storing Docker images.

- **Integration with AWS Services:** Seamless integration with AWS ECS simplifies the deployment process.

- **High Availability:** Images are stored redundantly across multiple Availability Zones, ensuring high availability.

### 3. AWS ECS (Elastic Container Service)

- **Orchestration:** AWS ECS automates the deployment, scaling, and management of containerized applications.

- **Fargate Integration:** ECS Fargate eliminates the need to manage infrastructure, enabling serverless container deployments.

- **Load Balancing:** Integration with AWS Elastic Load Balancing ensures high availability and scalability.

### 4. GitHub Actions for CI/CD

- **Automation:** GitHub Actions automates the entire CI/CD pipeline, from code changes to deployment.

- **Consistency:** Ensures consistent and reliable builds and deployments.

- **Visibility:** Provides visibility into the CI/CD process with detailed logs and status checks.

### 5. Flask API with Gunicorn and Nginx

- **High Performance:** Gunicorn, a Python WSGI HTTP server, combined with Nginx as a reverse proxy, delivers high-performance and scalable API endpoints.

- **Load Balancing:** Nginx acts as a load balancer, distributing incoming traffic across multiple instances of your Flask API, ensuring even load distribution and high availability.

- **Scaling:** With Gunicorn, you can easily scale your Flask API by adding more worker processes to handle increased request loads.

### 6. Secrets Management for Enhanced Security

- **Secrets Protection:** Sensitive information, such as API keys, is securely stored using GitHub Secrets, ensuring that they are not exposed in your repository.

- **Access Control:** GitHub Secrets are only accessible by authorized users, enhancing access control and limiting exposure to sensitive data.

- **Secure CI/CD:** Secrets are securely accessed during the CI/CD process, ensuring that sensitive information is protected throughout the deployment pipeline.
