# 🌊 IoT Stream Processing Infrastructure

**High-performance streaming architecture for real-time energy data processing**

## 🌟 Overview

The IoT Stream Processing Infrastructure is designed to handle massive volumes of energy meter data in real-time, supporting 12,000+ energy meters with 48,000+ data points per hour. Built on Redis Streams and Apache Kafka, it provides sub-second latency for critical energy monitoring and alerting.

### Key Capabilities

- **High Throughput**: 12k+ meters, 48k+ data points/hour
- **Low Latency**: <100ms for critical alerts
- **Multi-Backend**: Redis Streams and Kafka Topics
- **Auto-Scaling**: Horizontal scaling with consumer groups
- **Fault Tolerance**: Robust error handling and recovery

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   IoT Stream Processing                         │
├─────────────────────────────────────────────────────────────────┤
│  🌊 Stream Management Layer                                     │
│  ├── EnergyStreamManager (Energy-specific streams)             │
│  ├── StreamManager (Unified interface)                         │
│  └── StreamBackend (Redis/Kafka/Auto selection)                │
├─────────────────────────────────────────────────────────────────┤
│  🔄 Processing Engines                                          │
│  ├── RedisStreamProcessor (Redis Streams)                      │
│  ├── KafkaStreamProcessor (Kafka Topics)                       │
│  └── Auto-Backend Selection                                    │
├─────────────────────────────────────────────────────────────────┤
│  📊 Data Models                                                 │
│  ├── MeterReading (Energy meter data)                          │
│  ├── StreamMessage (Generic stream messages)                   │
│  └── ProcessingResult (Processing outcomes)                    │
├─────────────────────────────────────────────────────────────────┤
│  ⚙️ Configuration & Monitoring                                  │
│  ├── StreamConfig (Stream configuration)                       │
│  ├── Metrics Collection                                        │
│  └── Health Monitoring                                         │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 Core Components

### 🌊 Stream Managers

#### StreamManager (Base)
The unified interface for all streaming operations:

```python
from redaptive.streaming import StreamManager, StreamBackend

# Initialize with automatic backend selection
manager = StreamManager(StreamBackend.AUTO)

# Start the stream manager
await manager.start()

# Publish messages
await manager.publish_message("energy_readings", message)

# Start consumers
await manager.start_consumer("energy_readings", "consumer_1")
```

#### EnergyStreamManager (Energy-Specific)
Pre-configured manager for energy domain operations:

```python
from redaptive.streaming import EnergyStreamManager

# Initialize energy-specific manager
energy_manager = EnergyStreamManager(StreamBackend.REDIS)

# Setup energy streams
await energy_manager.setup_energy_streams()

# Start energy consumers
await energy_manager.start_energy_consumers()

# Publish meter reading
await energy_manager.publish_meter_reading(meter_reading)

# Publish alerts and anomalies
await energy_manager.publish_alert(alert_data)
await energy_manager.publish_anomaly(anomaly_data)
```

### 🔄 Processing Engines

#### RedisStreamProcessor
High-performance Redis-based streaming:

```python
from redaptive.streaming.redis_client import RedisStreamProcessor

# Initialize processor
processor = RedisStreamProcessor("redis://localhost:6379")

# Connect to Redis
await processor.connect()

# Create stream with consumer group
config = StreamConfig(
    stream_name="energy_meters",
    consumer_group="energy_processors",
    batch_size=100,
    max_retries=3
)
await processor.create_stream("energy_meters", config)

# Register message processor
processor.register_processor("meter_reading", process_meter_reading)

# Start consumer
await processor.start_consumer("energy_meters", "consumer_1")
```

#### KafkaStreamProcessor
Scalable Kafka-based streaming:

```python
from redaptive.streaming.kafka_client import KafkaStreamProcessor

# Initialize processor
processor = KafkaStreamProcessor("localhost:9092")

# Connect to Kafka
await processor.connect()

# Create topic
await processor.create_topic("energy_meters", partitions=12)

# Publish with partition key
await processor.publish_message(
    "energy_meters", 
    message, 
    partition_key=meter_reading.building_id
)

# Start consumer group
await processor.start_consumer(
    "energy_meters", 
    "energy_processors",
    consumer_name="consumer_1"
)
```

## 📊 Data Models

### MeterReading
Structured energy meter data:

```python
from redaptive.streaming.data_models import MeterReading, MeterType

meter_reading = MeterReading(
    meter_id="meter_001",
    building_id="building_001",
    meter_type=MeterType.ELECTRICITY,
    timestamp=datetime.now(),
    value=150.5,
    unit="kWh",
    quality_score=0.95,
    metadata={"location": "Floor 1"}
)

# Serialize for transmission
data = meter_reading.to_dict()

# Deserialize from transmission
restored = MeterReading.from_dict(data)
```

### StreamMessage
Generic stream message wrapper:

```python
from redaptive.streaming.data_models import StreamMessage, MessageType

message = StreamMessage(
    message_id="msg_001",
    message_type=MessageType.METER_READING,
    source="energy_meter",
    timestamp=datetime.now(),
    payload=meter_reading.to_dict(),
    priority=1
)

# JSON serialization
json_data = message.to_json()
restored = StreamMessage.from_json(json_data)
```

### ProcessingResult
Processing outcome tracking:

```python
from redaptive.streaming.data_models import ProcessingResult, ProcessingStatus

result = ProcessingResult(
    message_id="msg_001",
    status=ProcessingStatus.SUCCESS,
    processor_name="anomaly_detector",
    processing_time=50.5,
    result_data={"anomaly_detected": False},
    error_message=None
)
```

## ⚙️ Configuration

### Stream Configuration

```python
# Redis configuration
redis_config = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "max_connections": 20,
    "decode_responses": True
}

# Kafka configuration
kafka_config = {
    "bootstrap_servers": "localhost:9092",
    "auto_offset_reset": "earliest",
    "enable_auto_commit": True,
    "group_id": "energy_processors"
}

# Stream configuration
stream_config = StreamConfig(
    stream_name="energy_meters",
    consumer_group="energy_processors",
    batch_size=100,
    max_retries=3,
    retry_delay=1.0
)
```

### Environment Variables

```bash
# Streaming backend selection
STREAMING_BACKEND=auto  # redis, kafka, or auto

# Redis configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_CONSUMER_GROUP=energy_processors

# Performance tuning
STREAMING_BATCH_SIZE=100
STREAMING_MAX_RETRIES=3
STREAMING_RETRY_DELAY=1.0
```

## 🚀 Performance Optimization

### Throughput Benchmarks

| Backend | Messages/Second | Latency (p95) | Memory Usage |
|---------|-----------------|---------------|---------------|
| Redis Streams | 15,000 msg/sec | <50ms | 512MB |
| Kafka Topics | 50,000 msg/sec | <100ms | 256MB |
| Auto-Selection | Depends on backend | Variable | Variable |

### Scaling Strategies

#### Horizontal Scaling
```python
# Multiple consumer instances
for i in range(num_consumers):
    consumer_name = f"consumer_{i}"
    await processor.start_consumer(
        "energy_meters", 
        consumer_name,
        consumer_group="energy_processors"
    )
```

#### Partitioning Strategy
```python
# Kafka partitioning by building
partition_key = meter_reading.building_id

# Redis partitioning by meter ID
stream_name = f"energy_meters_{meter_reading.meter_id[:2]}"
```

#### Load Balancing
```python
# Consumer group load balancing
consumer_group = "energy_processors"
await processor.start_consumer(
    "energy_meters",
    consumer_name,
    consumer_group=consumer_group
)
```

## 🔍 Monitoring & Metrics

### Built-in Metrics

```python
# Get processing metrics
metrics = manager.get_metrics()

# Example metrics output
{
    "messages_processed": 15000,
    "messages_failed": 25,
    "success_rate": 99.83,
    "average_processing_time_ms": 45.2,
    "active_consumers": 5,
    "backend": "redis",
    "running": True
}
```

### Health Monitoring

```python
# Perform health check
health = await manager.health_check()

# Example health check output
{
    "stream_manager": {
        "status": "healthy",
        "running": True,
        "streams_configured": 4
    },
    "processor": {
        "status": "healthy",
        "redis_connected": True,
        "active_consumers": 5
    }
}
```

### Custom Metrics

```python
# Register custom metrics
processor.register_metric("custom_processing_time", processing_time)
processor.register_metric("custom_error_rate", error_rate)

# Export metrics for monitoring systems
metrics_data = processor.export_metrics()
```

## 🛡️ Error Handling & Recovery

### Retry Mechanisms

```python
# Automatic retry configuration
retry_config = {
    "max_retries": 3,
    "retry_delay": 1.0,
    "exponential_backoff": True,
    "max_delay": 60.0
}

# Dead letter queue for failed messages
dead_letter_config = {
    "enabled": True,
    "max_attempts": 5,
    "dead_letter_stream": "energy_meters_dlq"
}
```

### Circuit Breaker Pattern

```python
# Circuit breaker for external services
circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=30,
    expected_exception=ConnectionError
)

@circuit_breaker
async def process_with_circuit_breaker(message):
    # Processing logic here
    return await external_service.process(message)
```

### Graceful Degradation

```python
# Fallback processing
async def process_with_fallback(message):
    try:
        return await primary_processor.process(message)
    except Exception as e:
        logger.warning(f"Primary processor failed: {e}")
        return await fallback_processor.process(message)
```

## 🔐 Security

### Authentication

```python
# Redis authentication
redis_config = {
    "host": "localhost",
    "port": 6379,
    "password": "secure_password",
    "ssl": True,
    "ssl_cert_reqs": None
}

# Kafka SASL authentication
kafka_config = {
    "bootstrap_servers": "localhost:9092",
    "security_protocol": "SASL_SSL",
    "sasl_mechanism": "PLAIN",
    "sasl_plain_username": "username",
    "sasl_plain_password": "password"
}
```

### Data Encryption

```python
# Message encryption
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt before publishing
encrypted_data = cipher_suite.encrypt(message.to_json().encode())
await processor.publish_message(stream_name, encrypted_data)

# Decrypt after consuming
decrypted_data = cipher_suite.decrypt(encrypted_data)
message = StreamMessage.from_json(decrypted_data.decode())
```

## 🧪 Testing

### Unit Testing

```python
import pytest
from unittest.mock import Mock, AsyncMock

@pytest.mark.asyncio
async def test_stream_manager():
    # Mock Redis processor
    mock_processor = Mock()
    mock_processor.connect = AsyncMock(return_value=True)
    mock_processor.publish_message = AsyncMock(return_value=True)
    
    manager = StreamManager(StreamBackend.REDIS)
    await manager.start()
    
    # Test message publishing
    success = await manager.publish_message("test_stream", message)
    assert success == True
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_end_to_end_processing():
    # Start stream manager
    manager = EnergyStreamManager(StreamBackend.REDIS)
    await manager.start()
    
    # Setup streams
    await manager.setup_energy_streams()
    
    # Publish test message
    meter_reading = MeterReading(
        meter_id="test_meter",
        building_id="test_building",
        meter_type=MeterType.ELECTRICITY,
        timestamp=datetime.now(),
        value=100.0,
        unit="kWh"
    )
    
    success = await manager.publish_meter_reading(meter_reading)
    assert success == True
    
    # Verify processing
    metrics = manager.get_metrics()
    assert metrics["messages_processed"] >= 1
```

### Performance Testing

```python
import asyncio
import time

async def test_throughput():
    manager = EnergyStreamManager(StreamBackend.REDIS)
    await manager.start()
    
    # Generate test data
    messages = [create_test_message(i) for i in range(10000)]
    
    # Measure throughput
    start_time = time.time()
    
    tasks = [
        manager.publish_meter_reading(msg) 
        for msg in messages
    ]
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    duration = end_time - start_time
    throughput = len(messages) / duration
    
    print(f"Throughput: {throughput:.2f} messages/second")
    assert throughput > 1000  # Minimum throughput requirement
```

## 📈 Production Deployment

### Docker Configuration

```dockerfile
# Dockerfile for streaming service
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ src/
COPY config/ config/

EXPOSE 8000

CMD ["python", "-m", "redaptive.streaming.server"]
```

### Kubernetes Deployment

```yaml
# streaming-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: streaming-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: streaming-service
  template:
    metadata:
      labels:
        app: streaming-service
    spec:
      containers:
      - name: streaming-service
        image: redaptive/streaming-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: STREAMING_BACKEND
          value: "redis"
        - name: REDIS_HOST
          value: "redis-service"
        - name: REDIS_PORT
          value: "6379"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Monitoring Stack

```yaml
# monitoring-stack.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'streaming-service'
      static_configs:
      - targets: ['streaming-service:8000']
      metrics_path: '/metrics'
```

## 🎯 Use Cases

### Real-Time Energy Monitoring

```python
# Example: Real-time anomaly detection
async def real_time_anomaly_detection():
    manager = EnergyStreamManager(StreamBackend.REDIS)
    await manager.start()
    
    # Register anomaly detector
    async def detect_anomaly(message):
        meter_reading = MeterReading.from_dict(message.payload)
        
        # Simple threshold-based detection
        if meter_reading.value > threshold:
            anomaly_data = {
                "meter_id": meter_reading.meter_id,
                "anomaly_type": "consumption_spike",
                "severity": "high",
                "timestamp": datetime.now().isoformat()
            }
            
            await manager.publish_anomaly(anomaly_data)
            return ProcessingResult(
                message_id=message.message_id,
                status=ProcessingStatus.SUCCESS,
                processor_name="anomaly_detector",
                result_data=anomaly_data
            )
    
    # Start processing
    await manager.start_energy_consumers()
    processor.register_processor("meter_reading", detect_anomaly)
```

### Demand Response Management

```python
# Example: Demand response coordination
async def demand_response_coordination():
    manager = EnergyStreamManager(StreamBackend.KAFKA)
    await manager.start()
    
    # Monitor grid events
    async def process_grid_event(message):
        grid_event = message.payload
        
        if grid_event["type"] == "peak_demand":
            # Trigger demand response
            response_data = {
                "event_id": grid_event["id"],
                "action": "reduce_load",
                "target_reduction": "20%",
                "duration": "2h"
            }
            
            await manager.publish_alert(response_data)
    
    processor.register_processor("grid_event", process_grid_event)
```

## 📚 Related Documentation

- **[Energy Agents](../agents/energy/)** - Energy intelligence agents
- **[API Documentation](../api/)** - Stream processing APIs
- **[Deployment Guide](../deployment/)** - Production deployment
- **[Development Guide](../development/)** - Building streaming applications

---

**🌊 IoT Stream Processing** - Enabling real-time energy intelligence through high-performance data streaming and processing.