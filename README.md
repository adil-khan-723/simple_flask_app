# Dockerized Flask API with PostgreSQL and Adminer

## Overview
This project demonstrates a simple multi-container application using Docker and Docker Compose.  
It includes:

- Flask API: Returns JSON with a message and PostgreSQL version.
- PostgreSQL: Database container initialized with a user and database.
- Adminer: Web-based database management interface.

Key Docker/DevOps concepts demonstrated:

- Multi-stage Docker build
- Docker Compose orchestration
- Environment variables
- Healthchecks
- Inter-container networking
- Custom ports

---

## Application Functionality

This application is a simple Flask API that connects to a PostgreSQL database and returns information about the database version.  

- **API Endpoint:** `/`  
  Returns JSON with:
  - `message`: Confirmation that the Flask API is running
  - `db_version`: The current PostgreSQL version obtained by querying the database

- **Adminer:** Provides a web interface to explore and manage the PostgreSQL database.

This project is mainly for learning purposes and demonstrates containerization, networking between services, environment variable usage, and health checks in Docker.

---

## Project Structure

project/
├── app.py
├── requirements.txt
├── Dockerfile_multistage
└── docker-compose.yml

---

## Prerequisites

- Docker >= 20.x  
- Docker Compose >= 1.29.x  
- Python 3.11 (optional for local testing)

---

## Running the Application

1. Clone the repository:

git clone <your-repo-url>
cd project

2. Build and start containers:

docker-compose up --build

3. Access services:

- Flask API: http://localhost:5001/  
- Adminer: http://localhost:8080/

---

## Environment Variables

Defined in docker-compose.yml:

DB Container:

POSTGRES_USER: user
POSTGRES_PASSWORD: password
POSTGRES_DB: testdb

API Container:

POSTGRES_HOST: db
POSTGRES_USER: user
POSTGRES_PASSWORD: password
POSTGRES_DB: testdb

Note: API uses these to connect to Postgres; DB uses its own variables to initialize the database.

---

## Dockerfile Details

- Multi-stage build: first stage installs dependencies, second stage copies only necessary files.  
- System libraries installed (gcc, libpq-dev) to support psycopg2.  
- Final image uses the same python:3.11-slim base for compatibility.  

Example snippet:
```bash
FROM python:3.11-slim AS build
WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
FROM python:3.11-slim
WORKDIR /app
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY app.py .
EXPOSE 5001
CMD ["python", "app.py"]

---

## Docker Compose Features

- Defines three services: app, db, adminer
- depends_on with healthcheck ensures API waits for DB readiness
- Environment variables injected into containers
- Exposes ports 5001 (API) and 8080 (Adminer)

---

## Example API Response

{
  "message": "Flask API is running",
  "db_version": "PostgreSQL 13.22 ..."
}

---

## Notes

- The Adminer "role root does not exist" warning appears if the default login is used.  
- Correct Adminer credentials:

System: PostgreSQL
Server: db
Username: user
Password: password
Database: testdb

- Healthchecks make the setup more production-like.  
- No volumes defined; DB data will not persist across container removal.  

---

## Author

- Adil khan
- GitHub: adil-khan-723
