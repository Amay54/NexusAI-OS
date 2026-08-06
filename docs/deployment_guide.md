# NexusAI OS Production Deployment Guide

## Docker Compose Deployment

NexusAI OS includes a production-ready `docker-compose.yml` stack incorporating FastAPI, Redis, PostgreSQL, Qdrant, Prometheus, and Grafana.

### Step 1: Environment Configuration
Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

### Step 2: Launch Production Stack
```bash
docker-compose up -d --build
```

### Step 3: Verify Container Health
```bash
docker-compose ps
```

### Access Ports:
- **FastAPI Control Plane**: `http://localhost:8000`
- **Interactive OpenAPI Docs**: `http://localhost:8000/docs`
- **Qdrant Vector Console**: `http://localhost:6333`
- **Prometheus Metrics**: `http://localhost:9090`
- **Grafana Dashboard**: `http://localhost:3000`
