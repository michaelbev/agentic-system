# 🚀 Deployment Guide

**Production deployment strategies for the Redaptive Agentic AI Platform**

## 🌟 Overview

This guide covers comprehensive deployment strategies for the Redaptive Agentic AI Platform, including infrastructure setup, scaling configurations, monitoring, and operational best practices for Energy-as-a-Service (EaaS) operations.

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Production Architecture                       │
├─────────────────────────────────────────────────────────────────┤
│  🌐 Load Balancer & API Gateway                                 │
│  ├── NGINX/HAProxy (Load Balancing)                            │
│  ├── Kong/Envoy (API Gateway)                                  │
│  └── SSL/TLS Termination                                       │
├─────────────────────────────────────────────────────────────────┤
│  🧠 Agent Services (Auto-Scaling)                               │
│  ├── Portfolio Intelligence Service (3+ replicas)             │
│  ├── Real-Time Monitoring Service (5+ replicas)               │
│  ├── Energy Finance Service (2+ replicas)                     │
│  └── Orchestration Engine (2+ replicas)                       │
├─────────────────────────────────────────────────────────────────┤
│  🌊 Stream Processing (High Availability)                       │
│  ├── Redis Cluster (3+ nodes)                                 │
│  ├── Kafka Cluster (3+ brokers)                               │
│  └── Stream Processors (Auto-scaling)                         │
├─────────────────────────────────────────────────────────────────┤
│  💾 Data Layer (Distributed)                                   │
│  ├── PostgreSQL Cluster (Primary + Replicas)                  │
│  ├── TimescaleDB (Time-series data)                           │
│  └── Object Storage (S3/MinIO)                                │
├─────────────────────────────────────────────────────────────────┤
│  📊 Observability Stack                                         │
│  ├── Prometheus (Metrics)                                     │
│  ├── Grafana (Visualization)                                  │
│  ├── Jaeger (Tracing)                                         │
│  └── ELK Stack (Logging)                                      │
└─────────────────────────────────────────────────────────────────┘
```

## 🏗️ Infrastructure Requirements

### Minimum Production Requirements

#### Compute Resources
- **CPU**: 16 cores minimum (32 cores recommended)
- **Memory**: 32GB RAM minimum (64GB recommended)
- **Storage**: 500GB SSD minimum (1TB recommended)
- **Network**: 10Gbps network connectivity

#### Service-Specific Requirements

| Service | CPU | Memory | Storage | Replicas |
|---------|-----|--------|---------|----------|
| Portfolio Intelligence | 2 cores | 4GB | 100GB | 3 |
| Real-Time Monitoring | 4 cores | 8GB | 200GB | 5 |
| Energy Finance | 2 cores | 4GB | 100GB | 2 |
| Orchestration Engine | 2 cores | 4GB | 50GB | 2 |
| Stream Processors | 4 cores | 8GB | 100GB | 3-10 |
| PostgreSQL | 4 cores | 16GB | 500GB | 3 |
| Redis/Kafka | 2 cores | 8GB | 100GB | 3 |

### Scaling Thresholds

#### Auto-Scaling Triggers
- **CPU Usage**: Scale up at 70%, scale down at 30%
- **Memory Usage**: Scale up at 80%, scale down at 40%
- **Queue Length**: Scale up at 1000 messages, scale down at 100
- **Response Time**: Scale up at 500ms p95, scale down at 100ms p95

#### Performance Targets
- **Throughput**: 12,000+ meters, 48,000+ data points/hour
- **Latency**: <100ms for critical alerts, <500ms for analysis
- **Availability**: 99.9% uptime SLA
- **Recovery Time**: <5 minutes for service recovery

## 🐳 Container Deployment

### Docker Configuration

#### Base Images

```dockerfile
# Base image for all services
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
COPY config/ config/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

#### Service-Specific Dockerfiles

```dockerfile
# Portfolio Intelligence Service
FROM base as portfolio-intelligence
EXPOSE 8001
CMD ["python", "-m", "redaptive.agents.energy.portfolio_intelligence"]

# Real-Time Monitoring Service
FROM base as monitoring
EXPOSE 8002
CMD ["python", "-m", "redaptive.agents.energy.monitoring"]

# Energy Finance Service
FROM base as finance
EXPOSE 8003
CMD ["python", "-m", "redaptive.agents.energy.finance"]

# Stream Processing Service
FROM base as streaming
EXPOSE 8004
CMD ["python", "-m", "redaptive.streaming.server"]

# Orchestration Engine
FROM base as orchestration
EXPOSE 8000
CMD ["python", "-m", "redaptive.orchestration.engine"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Core Services
  orchestration:
    build:
      context: .
      target: orchestration
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/redaptive
      - REDIS_URL=redis://redis:6379
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    depends_on:
      - postgres
      - redis
      - kafka
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  portfolio-intelligence:
    build:
      context: .
      target: portfolio-intelligence
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/redaptive
    depends_on:
      - postgres
    deploy:
      replicas: 3

  monitoring:
    build:
      context: .
      target: monitoring
    ports:
      - "8002:8002"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    deploy:
      replicas: 5

  finance:
    build:
      context: .
      target: finance
    ports:
      - "8003:8003"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432
    depends_on:
      - postgres
    deploy:
      replicas: 2

  streaming:
    build:
      context: .
      target: streaming
    ports:
      - "8004:8004"
    environment:
      - REDIS_URL=redis://redis:6379
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    depends_on:
      - redis
      - kafka
    deploy:
      replicas: 3

  # Data Services
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=redaptive
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  timescaledb:
    image: timescale/timescaledb:latest-pg15
    environment:
      - POSTGRES_DB=timeseries
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - timescale_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  kafka:
    image: confluentinc/cp-kafka:7.4.0
    ports:
      - "9092:9092"
    environment:
      - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
      - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
      - KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
    depends_on:
      - zookeeper

  zookeeper:
    image: confluentinc/cp-zookeeper:7.4.0
    ports:
      - "2181:2181"
    environment:
      - ZOOKEEPER_CLIENT_PORT=2181
      - ZOOKEEPER_TICK_TIME=2000

  # Load Balancer
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - orchestration
      - portfolio-intelligence
      - monitoring
      - finance

volumes:
  postgres_data:
  timescale_data:
  redis_data:
```

## ☸️ Kubernetes Deployment

### Namespace and Configuration

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: redaptive-platform
  labels:
    name: redaptive-platform
```

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redaptive-config
  namespace: redaptive-platform
data:
  DATABASE_URL: "postgresql://user:pass@postgres-service:5432/redaptive"
  REDIS_URL: "redis://redis-service:6379"
  KAFKA_BOOTSTRAP_SERVERS: "kafka-service:9092"
  STREAMING_BACKEND: "redis"
  LOG_LEVEL: "INFO"
```

### Secrets Management

```yaml
# secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: redaptive-secrets
  namespace: redaptive-platform
type: Opaque
data:
  DATABASE_PASSWORD: <base64-encoded-password>
  REDIS_PASSWORD: <base64-encoded-password>
  API_SECRET_KEY: <base64-encoded-secret>
  JWT_SECRET: <base64-encoded-jwt-secret>
```

### Service Deployments

```yaml
# orchestration-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orchestration-engine
  namespace: redaptive-platform
spec:
  replicas: 2
  selector:
    matchLabels:
      app: orchestration-engine
  template:
    metadata:
      labels:
        app: orchestration-engine
    spec:
      containers:
      - name: orchestration-engine
        image: redaptive/orchestration-engine:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            configMapKeyRef:
              name: redaptive-config
              key: DATABASE_URL
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: redaptive-secrets
              key: DATABASE_PASSWORD
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

```yaml
# monitoring-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: monitoring-service
  namespace: redaptive-platform
spec:
  replicas: 5
  selector:
    matchLabels:
      app: monitoring-service
  template:
    metadata:
      labels:
        app: monitoring-service
    spec:
      containers:
      - name: monitoring-service
        image: redaptive/monitoring-service:latest
        ports:
        - containerPort: 8002
        env:
        - name: DATABASE_URL
          valueFrom:
            configMapKeyRef:
              name: redaptive-config
              key: DATABASE_URL
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: redaptive-config
              key: REDIS_URL
        resources:
          requests:
            memory: "4Gi"
            cpu: "2000m"
          limits:
            memory: "8Gi"
            cpu: "4000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8002
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Auto-Scaling Configuration

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: monitoring-hpa
  namespace: redaptive-platform
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: monitoring-service
  minReplicas: 5
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
```

### Service Definitions

```yaml
# services.yaml
apiVersion: v1
kind: Service
metadata:
  name: orchestration-service
  namespace: redaptive-platform
spec:
  selector:
    app: orchestration-engine
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
  type: ClusterIP

---
apiVersion: v1
kind: Service
metadata:
  name: monitoring-service
  namespace: redaptive-platform
spec:
  selector:
    app: monitoring-service
  ports:
  - protocol: TCP
    port: 8002
    targetPort: 8002
  type: ClusterIP

---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: redaptive-platform
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    name: http
  - protocol: TCP
    port: 443
    targetPort: 443
    name: https
  type: LoadBalancer
```

## 📊 Monitoring and Observability

### Prometheus Configuration

```yaml
# prometheus.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: redaptive-platform
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    rule_files:
      - "/etc/prometheus/rules/*.yml"
    
    scrape_configs:
    - job_name: 'orchestration-engine'
      static_configs:
      - targets: ['orchestration-service:8000']
      metrics_path: '/metrics'
      scrape_interval: 30s
    
    - job_name: 'monitoring-service'
      static_configs:
      - targets: ['monitoring-service:8002']
      metrics_path: '/metrics'
      scrape_interval: 10s
    
    - job_name: 'streaming-service'
      static_configs:
      - targets: ['streaming-service:8004']
      metrics_path: '/metrics'
      scrape_interval: 10s
    
    - job_name: 'postgres-exporter'
      static_configs:
      - targets: ['postgres-exporter:9187']
    
    - job_name: 'redis-exporter'
      static_configs:
      - targets: ['redis-exporter:9121']
    
    alerting:
      alertmanagers:
      - static_configs:
        - targets: ['alertmanager:9093']
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Redaptive Platform Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "title": "Stream Processing Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(stream_messages_processed_total[5m])",
            "legendFormat": "{{stream_name}}"
          }
        ]
      }
    ]
  }
}
```

### Alert Rules

```yaml
# alert-rules.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: alert-rules
  namespace: redaptive-platform
data:
  alerts.yml: |
    groups:
    - name: redaptive-platform
      rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} for {{ $labels.service }}"
      
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "95th percentile response time is {{ $value }}s"
      
      - alert: StreamProcessingLag
        expr: stream_processing_lag > 1000
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Stream processing lag detected"
          description: "Stream {{ $labels.stream_name }} has {{ $value }} messages lagging"
      
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "Service {{ $labels.job }} is down"
```

## 🔒 Security Configuration

### Network Security

```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: redaptive-network-policy
  namespace: redaptive-platform
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: redaptive-platform
  - from:
    - podSelector:
        matchLabels:
          app: nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: redaptive-platform
  - to: []
    ports:
    - protocol: TCP
      port: 443
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
```

### RBAC Configuration

```yaml
# rbac.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: redaptive-service-role
  namespace: redaptive-platform
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: redaptive-service-binding
  namespace: redaptive-platform
subjects:
- kind: ServiceAccount
  name: redaptive-service-account
  namespace: redaptive-platform
roleRef:
  kind: Role
  name: redaptive-service-role
  apiGroup: rbac.authorization.k8s.io
```

### SSL/TLS Configuration

```yaml
# tls-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: redaptive-tls
  namespace: redaptive-platform
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-certificate>
  tls.key: <base64-encoded-private-key>
```

## 🏗️ Infrastructure as Code

### Terraform Configuration

```hcl
# main.tf
provider "aws" {
  region = var.aws_region
}

# VPC Configuration
resource "aws_vpc" "redaptive_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "redaptive-vpc"
  }
}

# EKS Cluster
resource "aws_eks_cluster" "redaptive_cluster" {
  name     = "redaptive-platform"
  role_arn = aws_iam_role.cluster_role.arn

  vpc_config {
    subnet_ids = [
      aws_subnet.private_subnet_1.id,
      aws_subnet.private_subnet_2.id,
      aws_subnet.public_subnet_1.id,
      aws_subnet.public_subnet_2.id
    ]
  }

  depends_on = [
    aws_iam_role_policy_attachment.cluster_policy,
    aws_iam_role_policy_attachment.service_policy,
  ]
}

# Node Group
resource "aws_eks_node_group" "redaptive_nodes" {
  cluster_name    = aws_eks_cluster.redaptive_cluster.name
  node_group_name = "redaptive-nodes"
  node_role_arn   = aws_iam_role.node_role.arn
  subnet_ids      = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]

  scaling_config {
    desired_size = 6
    max_size     = 20
    min_size     = 3
  }

  instance_types = ["m5.xlarge"]

  depends_on = [
    aws_iam_role_policy_attachment.node_policy,
    aws_iam_role_policy_attachment.cni_policy,
    aws_iam_role_policy_attachment.registry_policy,
  ]
}

# RDS PostgreSQL
resource "aws_db_instance" "redaptive_db" {
  identifier             = "redaptive-postgres"
  engine                 = "postgres"
  engine_version         = "15.3"
  instance_class         = "db.r5.2xlarge"
  allocated_storage      = 500
  storage_type           = "gp3"
  storage_encrypted      = true
  
  DB_NAME_ENERGY  = "redaptive"
  username = "redaptive_user"
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.redaptive_db_subnet.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = false
  final_snapshot_identifier = "redaptive-final-snapshot"
  
  tags = {
    Name = "redaptive-postgres"
  }
}

# ElastiCache Redis
resource "aws_elasticache_subnet_group" "redaptive_redis_subnet" {
  name       = "redaptive-redis-subnet"
  subnet_ids = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
}

resource "aws_elasticache_replication_group" "redaptive_redis" {
  replication_group_id       = "redaptive-redis"
  description                = "Redis cluster for Redaptive platform"
  
  port               = 6379
  parameter_group_name = "default.redis7"
  node_type          = "cache.r6g.xlarge"
  num_cache_clusters = 3
  
  subnet_group_name = aws_elasticache_subnet_group.redaptive_redis_subnet.name
  security_group_ids = [aws_security_group.redis_sg.id]
  
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  
  tags = {
    Name = "redaptive-redis"
  }
}
```

### Ansible Playbooks

```yaml
# playbook.yml
---
- name: Deploy Redaptive Platform
  hosts: kubernetes
  gather_facts: no
  vars:
    namespace: redaptive-platform
    
  tasks:
    - name: Create namespace
      kubernetes.core.k8s:
        name: "{{ namespace }}"
        api_version: v1
        kind: Namespace
        state: present
    
    - name: Deploy ConfigMap
      kubernetes.core.k8s:
        state: present
        definition:
          apiVersion: v1
          kind: ConfigMap
          metadata:
            name: redaptive-config
            namespace: "{{ namespace }}"
          data:
            DATABASE_URL: "{{ database_url }}"
            REDIS_URL: "{{ redis_url }}"
            KAFKA_BOOTSTRAP_SERVERS: "{{ kafka_servers }}"
    
    - name: Deploy Secrets
      kubernetes.core.k8s:
        state: present
        definition:
          apiVersion: v1
          kind: Secret
          metadata:
            name: redaptive-secrets
            namespace: "{{ namespace }}"
          type: Opaque
          data:
            DATABASE_PASSWORD: "{{ db_password | b64encode }}"
            API_SECRET_KEY: "{{ api_secret | b64encode }}"
    
    - name: Deploy Services
      kubernetes.core.k8s:
        state: present
        src: "{{ item }}"
      loop:
        - orchestration-deployment.yaml
        - monitoring-deployment.yaml
        - finance-deployment.yaml
        - portfolio-deployment.yaml
        - streaming-deployment.yaml
    
    - name: Wait for deployments
      kubernetes.core.k8s_info:
        api_version: apps/v1
        kind: Deployment
        namespace: "{{ namespace }}"
        wait: true
        wait_condition:
          type: Available
          status: "True"
        wait_timeout: 300
```

## 📈 Performance Tuning

### Database Optimization

```sql
-- PostgreSQL configuration
ALTER SYSTEM SET shared_buffers = '8GB';
ALTER SYSTEM SET effective_cache_size = '24GB';
ALTER SYSTEM SET maintenance_work_mem = '2GB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;

-- Indexes for energy data
CREATE INDEX CONCURRENTLY idx_meter_readings_timestamp 
ON meter_readings (timestamp DESC);

CREATE INDEX CONCURRENTLY idx_meter_readings_meter_id_timestamp 
ON meter_readings (meter_id, timestamp DESC);

CREATE INDEX CONCURRENTLY idx_energy_portfolios_building_id 
ON energy_portfolios USING HASH (building_id);

-- Partitioning for time-series data
CREATE TABLE meter_readings_2024 PARTITION OF meter_readings
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE meter_readings_2025 PARTITION OF meter_readings
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

### Redis Configuration

```conf
# redis.conf
maxmemory 8gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfsync everysec
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

### Kafka Configuration

```properties
# server.properties
num.network.threads=8
num.io.threads=16
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600
num.partitions=12
num.recovery.threads.per.data.dir=1
offsets.topic.replication.factor=3
transaction.state.log.replication.factor=3
transaction.state.log.min.isr=2
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000
zookeeper.connect=zookeeper:2181
zookeeper.connection.timeout.ms=18000
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v --cov=src/redaptive --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to ECR
      uses: aws-actions/amazon-ecr-login@v1
    
    - name: Build and push images
      run: |
        docker buildx build --target orchestration --tag $ECR_REGISTRY/orchestration:latest --push .
        docker buildx build --target monitoring --tag $ECR_REGISTRY/monitoring:latest --push .
        docker buildx build --target finance --tag $ECR_REGISTRY/finance:latest --push .
        docker buildx build --target portfolio-intelligence --tag $ECR_REGISTRY/portfolio:latest --push .
        docker buildx build --target streaming --tag $ECR_REGISTRY/streaming:latest --push .
    
    env:
      ECR_REGISTRY: ${{ secrets.ECR_REGISTRY }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure kubectl
      run: |
        aws eks update-kubeconfig --region $AWS_REGION --name redaptive-platform
    
    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f k8s/
        kubectl rollout status deployment/orchestration-engine -n redaptive-platform
        kubectl rollout status deployment/monitoring-service -n redaptive-platform
        kubectl rollout status deployment/finance-service -n redaptive-platform
        kubectl rollout status deployment/portfolio-service -n redaptive-platform
        kubectl rollout status deployment/streaming-service -n redaptive-platform
    
    env:
      AWS_REGION: ${{ secrets.AWS_REGION }}
```

## 📚 Related Documentation

- **[Energy Agents](../agents/energy/)** - Agent-specific deployment considerations
- **[Streaming Architecture](../streaming/)** - Stream processing deployment
- **[API Documentation](../api/)** - API gateway and load balancer configuration
- **[Development Guide](../development/)** - Development environment setup

---

**🚀 Redaptive Platform Deployment** - Comprehensive production deployment strategies for scalable energy intelligence automation.