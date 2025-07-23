"""
Stream Manager for IoT Data Processing
======================================

Unified interface for managing Redis and Kafka stream processing.
Handles 12k+ energy meters with 48k+ data points per hour.
"""

import asyncio
import logging
from typing import Dict, Optional, Callable, Any, List
from datetime import datetime
from enum import Enum

from redaptive.config import settings
from .data_models import StreamMessage, StreamConfig, MessageType, MeterReading
from .redis_client import RedisStreamProcessor, REDIS_AVAILABLE
from .kafka_client import KafkaStreamProcessor, KAFKA_AVAILABLE

logger = logging.getLogger(__name__)


class StreamBackend(Enum):
    """Supported streaming backends."""
    REDIS = "redis"
    KAFKA = "kafka"
    AUTO = "auto"


class StreamManager:
    """
    Unified stream manager for IoT energy data processing.
    
    Features:
    - Automatic backend selection (Redis/Kafka)
    - Unified API for both backends
    - High-throughput processing
    - Automatic failover and retry
    - Monitoring and metrics
    """
    
    def __init__(self, backend: StreamBackend = StreamBackend.AUTO):
        self.backend = backend
        self.processor: Optional[Any] = None
        self.running = False
        self.streams: Dict[str, StreamConfig] = {}
        self.message_processors: Dict[str, Callable] = {}
        
        # Initialize processor based on backend
        self._initialize_processor()
    
    def _initialize_processor(self):
        """Initialize the appropriate stream processor."""
        if self.backend == StreamBackend.REDIS:
            if not REDIS_AVAILABLE:
                raise ImportError("Redis not available. Install with: pip install redis")
            self.processor = RedisStreamProcessor()
            
        elif self.backend == StreamBackend.KAFKA:
            if not KAFKA_AVAILABLE:
                raise ImportError("Kafka not available. Install with: pip install aiokafka")
            self.processor = KafkaStreamProcessor()
            
        elif self.backend == StreamBackend.AUTO:
            # Prefer Kafka for production, fallback to Redis
            if KAFKA_AVAILABLE:
                self.processor = KafkaStreamProcessor()
                self.backend = StreamBackend.KAFKA
                logger.info("Auto-selected Kafka backend")
            elif REDIS_AVAILABLE:
                self.processor = RedisStreamProcessor()
                self.backend = StreamBackend.REDIS
                logger.info("Auto-selected Redis backend")
            else:
                raise ImportError("No streaming backend available. Install redis or aiokafka")
        
        logger.info(f"Initialized stream manager with {self.backend.value} backend")
    
    async def start(self) -> bool:
        """Start the stream manager."""
        try:
            success = await self.processor.connect()
            if success:
                self.running = True
                logger.info("Stream manager started successfully")
                
                # Register default message processors
                self._register_default_processors()
                
                return True
            else:
                logger.error("Failed to start stream manager")
                return False
                
        except Exception as e:
            logger.error(f"Error starting stream manager: {e}")
            return False
    
    async def stop(self):
        """Stop the stream manager."""
        if self.processor:
            await self.processor.disconnect()
            self.running = False
            logger.info("Stream manager stopped")
    
    def _register_default_processors(self):
        """Register default message processors."""
        self.register_processor(MessageType.METER_READING.value, self._process_meter_reading)
        self.register_processor(MessageType.ALERT.value, self._process_alert)
        self.register_processor(MessageType.ANOMALY.value, self._process_anomaly)
    
    async def create_stream(self, stream_name: str, config: Optional[StreamConfig] = None) -> bool:
        """Create a new stream."""
        if not config:
            config = StreamConfig(
                stream_name=stream_name,
                batch_size=100,
                max_retries=3,
                consumer_group=f"{stream_name}_processors"
            )
        
        self.streams[stream_name] = config
        
        if self.backend == StreamBackend.REDIS:
            return await self.processor.create_stream(stream_name, config)
        elif self.backend == StreamBackend.KAFKA:
            return await self.processor.create_topic(stream_name, config)
        
        return False
    
    async def publish_meter_reading(self, stream_name: str, meter_reading: MeterReading) -> bool:
        """Publish a meter reading to the stream."""
        return await self.processor.publish_meter_reading(stream_name, meter_reading.to_dict())
    
    async def publish_message(self, stream_name: str, message: StreamMessage) -> bool:
        """Publish a message to the stream."""
        return await self.processor.publish_message(stream_name, message)
    
    def register_processor(self, message_type: str, processor: Callable):
        """Register a message processor."""
        self.message_processors[message_type] = processor
        self.processor.register_processor(message_type, processor)
    
    async def start_consumer(self, stream_name: str, consumer_id: str,
                           consumer_group: Optional[str] = None) -> bool:
        """Start a consumer for a stream."""
        if not consumer_group:
            consumer_group = f"{stream_name}_processors"
        
        return await self.processor.start_consumer(stream_name, consumer_id, consumer_group)
    
    async def stop_consumer(self, stream_name: str, consumer_id: str):
        """Stop a consumer."""
        await self.processor.stop_consumer(stream_name, consumer_id)
    
    async def get_stream_info(self, stream_name: str) -> Dict[str, Any]:
        """Get stream information."""
        if self.backend == StreamBackend.REDIS:
            return await self.processor.get_stream_info(stream_name)
        elif self.backend == StreamBackend.KAFKA:
            return await self.processor.get_topic_info(stream_name)
        
        return {}
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get processing metrics."""
        base_metrics = self.processor.get_metrics()
        base_metrics.update({
            "backend": self.backend.value,
            "streams_configured": len(self.streams),
            "processors_registered": len(self.message_processors),
            "running": self.running
        })
        return base_metrics
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check."""
        processor_health = await self.processor.health_check()
        return {
            "stream_manager": {
                "status": "healthy" if self.running else "stopped",
                "backend": self.backend.value,
                "streams_configured": len(self.streams),
                "processors_registered": len(self.message_processors)
            },
            "processor": processor_health
        }
    
    # Default message processors
    async def _process_meter_reading(self, message: StreamMessage) -> Dict[str, Any]:
        """Process meter reading messages."""
        try:
            meter_data = message.payload
            
            # Basic validation
            required_fields = ['meter_id', 'building_id', 'value', 'timestamp']
            if not all(field in meter_data for field in required_fields):
                raise ValueError(f"Missing required fields: {required_fields}")
            
            # Convert to MeterReading object
            meter_reading = MeterReading.from_dict(meter_data)
            
            # Store in database (integration with energy monitoring agent)
            # This would typically call the energy monitoring agent
            logger.info(f"Processed meter reading: {meter_reading.meter_id} = {meter_reading.value} {meter_reading.unit}")
            
            return {
                "status": "processed",
                "meter_id": meter_reading.meter_id,
                "value": meter_reading.value,
                "timestamp": meter_reading.timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to process meter reading: {e}")
            raise
    
    async def _process_alert(self, message: StreamMessage) -> Dict[str, Any]:
        """Process alert messages."""
        try:
            alert_data = message.payload
            
            # Log alert
            logger.warning(f"Energy alert: {alert_data.get('message', 'Unknown alert')}")
            
            # Forward to appropriate handlers
            # This would typically integrate with monitoring systems
            
            return {
                "status": "processed",
                "alert_type": alert_data.get("type", "unknown"),
                "processed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to process alert: {e}")
            raise
    
    async def _process_anomaly(self, message: StreamMessage) -> Dict[str, Any]:
        """Process anomaly detection messages."""
        try:
            anomaly_data = message.payload
            
            # Log anomaly
            logger.warning(f"Energy anomaly detected: {anomaly_data.get('description', 'Unknown anomaly')}")
            
            # Forward to anomaly analysis systems
            # This would typically integrate with ML pipelines
            
            return {
                "status": "processed",
                "anomaly_type": anomaly_data.get("type", "unknown"),
                "severity": anomaly_data.get("severity", "low"),
                "processed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to process anomaly: {e}")
            raise


class EnergyStreamManager(StreamManager):
    """
    Specialized stream manager for energy data processing.
    
    Pre-configured for Redaptive's energy monitoring requirements.
    """
    
    def __init__(self, backend: StreamBackend = StreamBackend.AUTO):
        super().__init__(backend)
        self.energy_streams = {
            "meter_readings": "energy_meter_readings",
            "alerts": "energy_alerts", 
            "anomalies": "energy_anomalies",
            "diagnostics": "energy_diagnostics"
        }
    
    async def setup_energy_streams(self) -> bool:
        """Setup pre-configured energy streams."""
        success = True
        
        # Setup meter readings stream (high throughput)
        meter_config = StreamConfig(
            stream_name=self.energy_streams["meter_readings"],
            batch_size=500,  # Higher batch size for meter readings
            max_retries=3,
            consumer_group="meter_processors"
        )
        success &= await self.create_stream(self.energy_streams["meter_readings"], meter_config)
        
        # Setup alerts stream (low latency)
        alert_config = StreamConfig(
            stream_name=self.energy_streams["alerts"],
            batch_size=50,  # Lower batch size for alerts
            max_retries=5,
            consumer_group="alert_processors"
        )
        success &= await self.create_stream(self.energy_streams["alerts"], alert_config)
        
        # Setup anomalies stream
        anomaly_config = StreamConfig(
            stream_name=self.energy_streams["anomalies"],
            batch_size=100,
            max_retries=3,
            consumer_group="anomaly_processors"
        )
        success &= await self.create_stream(self.energy_streams["anomalies"], anomaly_config)
        
        # Setup diagnostics stream
        diagnostic_config = StreamConfig(
            stream_name=self.energy_streams["diagnostics"],
            batch_size=100,
            max_retries=3,
            consumer_group="diagnostic_processors"
        )
        success &= await self.create_stream(self.energy_streams["diagnostics"], diagnostic_config)
        
        if success:
            logger.info("Energy streams setup completed successfully")
        else:
            logger.error("Failed to setup some energy streams")
        
        return success
    
    async def publish_meter_reading(self, meter_reading: MeterReading) -> bool:
        """Publish a meter reading to the appropriate stream."""
        return await super().publish_meter_reading(
            self.energy_streams["meter_readings"], 
            meter_reading
        )
    
    async def publish_alert(self, alert_data: Dict[str, Any]) -> bool:
        """Publish an energy alert."""
        message = StreamMessage(
            message_id=f"alert_{datetime.now().timestamp()}",
            message_type=MessageType.ALERT,
            source="energy_monitor",
            timestamp=datetime.now(),
            payload=alert_data
        )
        
        return await self.publish_message(self.energy_streams["alerts"], message)
    
    async def publish_anomaly(self, anomaly_data: Dict[str, Any]) -> bool:
        """Publish an energy anomaly."""
        message = StreamMessage(
            message_id=f"anomaly_{datetime.now().timestamp()}",
            message_type=MessageType.ANOMALY,
            source="anomaly_detector",
            timestamp=datetime.now(),
            payload=anomaly_data
        )
        
        return await self.publish_message(self.energy_streams["anomalies"], message)
    
    async def start_energy_consumers(self) -> bool:
        """Start consumers for all energy streams."""
        success = True
        
        # Start meter reading consumers (multiple for high throughput)
        for i in range(3):  # 3 consumers for high throughput
            success &= await self.start_consumer(
                self.energy_streams["meter_readings"],
                f"meter_consumer_{i}"
            )
        
        # Start alert consumer (single consumer for low latency)
        success &= await self.start_consumer(
            self.energy_streams["alerts"],
            "alert_consumer"
        )
        
        # Start anomaly consumer
        success &= await self.start_consumer(
            self.energy_streams["anomalies"],
            "anomaly_consumer"
        )
        
        # Start diagnostic consumer
        success &= await self.start_consumer(
            self.energy_streams["diagnostics"],
            "diagnostic_consumer"
        )
        
        logger.info(f"Energy consumers started: {'success' if success else 'with errors'}")
        return success