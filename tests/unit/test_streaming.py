"""
Test streaming infrastructure.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from redaptive.streaming import StreamManager, EnergyStreamManager, StreamBackend
from redaptive.streaming.data_models import (
    MeterReading, MeterType, StreamMessage, MessageType, 
    StreamConfig, ProcessingStatus
)


class TestDataModels:
    """Test data models for streaming."""
    
    def test_meter_reading_serialization(self):
        """Test meter reading serialization."""
        reading = MeterReading(
            meter_id="meter_001",
            building_id="building_001",
            meter_type=MeterType.ELECTRICITY,
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
            value=150.5,
            unit="kWh",
            quality_score=0.95,
            metadata={"location": "Floor 1"}
        )
        
        # Test to_dict
        data = reading.to_dict()
        assert data["meter_id"] == "meter_001"
        assert data["meter_type"] == "electricity"
        assert data["value"] == 150.5
        assert data["metadata"]["location"] == "Floor 1"
        
        # Test from_dict
        restored = MeterReading.from_dict(data)
        assert restored.meter_id == reading.meter_id
        assert restored.meter_type == reading.meter_type
        assert restored.value == reading.value
        assert restored.timestamp == reading.timestamp
    
    def test_stream_message_serialization(self):
        """Test stream message serialization."""
        message = StreamMessage(
            message_id="msg_001",
            message_type=MessageType.METER_READING,
            source="test_source",
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
            payload={"test": "data"},
            priority=1
        )
        
        # Test to_json
        json_str = message.to_json()
        assert isinstance(json_str, str)
        
        # Test from_json
        restored = StreamMessage.from_json(json_str)
        assert restored.message_id == message.message_id
        assert restored.message_type == message.message_type
        assert restored.payload == message.payload
        assert restored.priority == message.priority
    
    def test_stream_config(self):
        """Test stream configuration."""
        config = StreamConfig(
            stream_name="test_stream",
            batch_size=50,
            max_retries=2,
            consumer_group="test_group"
        )
        
        data = config.to_dict()
        assert data["stream_name"] == "test_stream"
        assert data["batch_size"] == 50
        assert data["max_retries"] == 2
        assert data["consumer_group"] == "test_group"


class TestStreamManager:
    """Test stream manager functionality."""
    
    def test_stream_manager_initialization(self):
        """Test stream manager initialization."""
        # Test auto backend selection (should work without dependencies)
        with patch('redaptive.streaming.stream_manager.KAFKA_AVAILABLE', False):
            with patch('redaptive.streaming.stream_manager.REDIS_AVAILABLE', False):
                with pytest.raises(ImportError):
                    StreamManager(StreamBackend.AUTO)
    
    @patch('redaptive.streaming.stream_manager.REDIS_AVAILABLE', True)
    @patch('redaptive.streaming.stream_manager.RedisStreamProcessor')
    def test_redis_backend_selection(self, mock_redis_processor):
        """Test Redis backend selection."""
        manager = StreamManager(StreamBackend.REDIS)
        assert manager.backend == StreamBackend.REDIS
        mock_redis_processor.assert_called_once()
    
    @patch('redaptive.streaming.stream_manager.KAFKA_AVAILABLE', True)
    @patch('redaptive.streaming.stream_manager.KafkaStreamProcessor')
    def test_kafka_backend_selection(self, mock_kafka_processor):
        """Test Kafka backend selection."""
        manager = StreamManager(StreamBackend.KAFKA)
        assert manager.backend == StreamBackend.KAFKA
        mock_kafka_processor.assert_called_once()
    
    @patch('redaptive.streaming.stream_manager.REDIS_AVAILABLE', True)
    @patch('redaptive.streaming.stream_manager.RedisStreamProcessor')
    @pytest.mark.asyncio
    async def test_start_and_stop(self, mock_redis_processor):
        """Test stream manager start and stop."""
        mock_processor = Mock()
        mock_processor.connect = AsyncMock(return_value=True)
        mock_processor.disconnect = AsyncMock()
        mock_processor.register_processor = Mock()
        mock_redis_processor.return_value = mock_processor
        
        manager = StreamManager(StreamBackend.REDIS)
        
        # Test start
        success = await manager.start()
        assert success == True
        assert manager.running == True
        mock_processor.connect.assert_called_once()
        
        # Test stop
        await manager.stop()
        assert manager.running == False
        mock_processor.disconnect.assert_called_once()
    
    @patch('redaptive.streaming.stream_manager.REDIS_AVAILABLE', True)
    @patch('redaptive.streaming.stream_manager.RedisStreamProcessor')
    @pytest.mark.asyncio
    async def test_message_publishing(self, mock_redis_processor):
        """Test message publishing."""
        mock_processor = Mock()
        mock_processor.connect = AsyncMock(return_value=True)
        mock_processor.publish_meter_reading = AsyncMock(return_value=True)
        mock_processor.publish_message = AsyncMock(return_value=True)
        mock_processor.register_processor = Mock()
        mock_redis_processor.return_value = mock_processor
        
        manager = StreamManager(StreamBackend.REDIS)
        await manager.start()
        
        # Test meter reading publishing
        reading = MeterReading(
            meter_id="meter_001",
            building_id="building_001",
            meter_type=MeterType.ELECTRICITY,
            timestamp=datetime.now(),
            value=150.5,
            unit="kWh"
        )
        
        success = await manager.publish_meter_reading("test_stream", reading)
        assert success == True
        mock_processor.publish_meter_reading.assert_called_once()
        
        # Test message publishing
        message = StreamMessage(
            message_id="msg_001",
            message_type=MessageType.ALERT,
            source="test",
            timestamp=datetime.now(),
            payload={"test": "data"}
        )
        
        success = await manager.publish_message("test_stream", message)
        assert success == True
        mock_processor.publish_message.assert_called_once()
    
    @patch('redaptive.streaming.stream_manager.REDIS_AVAILABLE', True)
    @patch('redaptive.streaming.stream_manager.RedisStreamProcessor')
    @pytest.mark.asyncio
    async def test_consumer_management(self, mock_redis_processor):
        """Test consumer management."""
        mock_processor = Mock()
        mock_processor.connect = AsyncMock(return_value=True)
        mock_processor.start_consumer = AsyncMock(return_value=True)
        mock_processor.stop_consumer = AsyncMock()
        mock_processor.register_processor = Mock()
        mock_redis_processor.return_value = mock_processor
        
        manager = StreamManager(StreamBackend.REDIS)
        await manager.start()
        
        # Test start consumer
        success = await manager.start_consumer("test_stream", "consumer_1")
        assert success == True
        mock_processor.start_consumer.assert_called_once()
        
        # Test stop consumer
        await manager.stop_consumer("test_stream", "consumer_1")
        mock_processor.stop_consumer.assert_called_once()


class TestEnergyStreamManager:
    """Test energy-specific stream manager."""
    
    @patch('redaptive.streaming.stream_manager.REDIS_AVAILABLE', True)
    @patch('redaptive.streaming.stream_manager.RedisStreamProcessor')
    def test_energy_stream_initialization(self, mock_redis_processor):
        """Test energy stream manager initialization."""
        manager = EnergyStreamManager(StreamBackend.REDIS)
        
        # Check pre-configured streams
        assert "meter_readings" in manager.energy_streams
        assert "alerts" in manager.energy_streams
        assert "anomalies" in manager.energy_streams
        assert "diagnostics" in manager.energy_streams
    
    @patch('redaptive.streaming.stream_manager.REDIS_AVAILABLE', True)
    @patch('redaptive.streaming.stream_manager.RedisStreamProcessor')
    @pytest.mark.asyncio
    async def test_energy_stream_setup(self, mock_redis_processor):
        """Test energy stream setup."""
        mock_processor = Mock()
        mock_processor.connect = AsyncMock(return_value=True)
        mock_processor.create_stream = AsyncMock(return_value=True)
        mock_processor.register_processor = Mock()
        mock_redis_processor.return_value = mock_processor
        
        manager = EnergyStreamManager(StreamBackend.REDIS)
        await manager.start()
        
        # Test setup energy streams
        success = await manager.setup_energy_streams()
        assert success == True
        
        # Should have created 4 streams
        assert mock_processor.create_stream.call_count == 4
    
    @patch('redaptive.streaming.stream_manager.REDIS_AVAILABLE', True)
    @patch('redaptive.streaming.stream_manager.RedisStreamProcessor')
    @pytest.mark.asyncio
    async def test_energy_consumer_setup(self, mock_redis_processor):
        """Test energy consumer setup."""
        mock_processor = Mock()
        mock_processor.connect = AsyncMock(return_value=True)
        mock_processor.start_consumer = AsyncMock(return_value=True)
        mock_processor.register_processor = Mock()
        mock_redis_processor.return_value = mock_processor
        
        manager = EnergyStreamManager(StreamBackend.REDIS)
        await manager.start()
        
        # Test start energy consumers
        success = await manager.start_energy_consumers()
        assert success == True
        
        # Should have started multiple consumers
        assert mock_processor.start_consumer.call_count >= 4
    
    @patch('redaptive.streaming.stream_manager.REDIS_AVAILABLE', True)
    @patch('redaptive.streaming.stream_manager.RedisStreamProcessor')
    @pytest.mark.asyncio
    async def test_energy_specific_publishing(self, mock_redis_processor):
        """Test energy-specific message publishing."""
        mock_processor = Mock()
        mock_processor.connect = AsyncMock(return_value=True)
        mock_processor.publish_meter_reading = AsyncMock(return_value=True)
        mock_processor.publish_message = AsyncMock(return_value=True)
        mock_processor.register_processor = Mock()
        mock_redis_processor.return_value = mock_processor
        
        manager = EnergyStreamManager(StreamBackend.REDIS)
        await manager.start()
        
        # Test meter reading publishing
        reading = MeterReading(
            meter_id="meter_001",
            building_id="building_001",
            meter_type=MeterType.ELECTRICITY,
            timestamp=datetime.now(),
            value=150.5,
            unit="kWh"
        )
        
        success = await manager.publish_meter_reading(reading)
        assert success == True
        
        # Test alert publishing
        alert_data = {
            "type": "high_consumption",
            "meter_id": "meter_001",
            "message": "High consumption detected"
        }
        
        success = await manager.publish_alert(alert_data)
        assert success == True
        
        # Test anomaly publishing
        anomaly_data = {
            "type": "consumption_spike",
            "meter_id": "meter_001",
            "severity": "high"
        }
        
        success = await manager.publish_anomaly(anomaly_data)
        assert success == True


class TestStreamProcessing:
    """Test stream processing functionality."""
    
    @patch('redaptive.streaming.stream_manager.REDIS_AVAILABLE', True)
    @patch('redaptive.streaming.stream_manager.RedisStreamProcessor')
    @pytest.mark.asyncio
    async def test_message_processing(self, mock_redis_processor):
        """Test message processing."""
        mock_processor = Mock()
        mock_processor.connect = AsyncMock(return_value=True)
        mock_processor.register_processor = Mock()
        mock_redis_processor.return_value = mock_processor
        
        manager = StreamManager(StreamBackend.REDIS)
        await manager.start()
        
        # Test meter reading processing
        message = StreamMessage(
            message_id="msg_001",
            message_type=MessageType.METER_READING,
            source="test_meter",
            timestamp=datetime.now(),
            payload={
                "meter_id": "meter_001",
                "building_id": "building_001",
                "meter_type": "electricity",
                "timestamp": datetime.now().isoformat(),
                "value": 150.5,
                "unit": "kWh"
            }
        )
        
        result = await manager._process_meter_reading(message)
        
        assert result["status"] == "processed"
        assert result["meter_id"] == "meter_001"
        assert result["value"] == 150.5
    
    @patch('redaptive.streaming.stream_manager.REDIS_AVAILABLE', True)
    @patch('redaptive.streaming.stream_manager.RedisStreamProcessor')
    @pytest.mark.asyncio
    async def test_metrics_collection(self, mock_redis_processor):
        """Test metrics collection."""
        mock_processor = Mock()
        mock_processor.connect = AsyncMock(return_value=True)
        mock_processor.get_metrics = Mock(return_value={
            "messages_processed": 100,
            "messages_failed": 5,
            "success_rate": 95.0
        })
        mock_processor.register_processor = Mock()
        mock_redis_processor.return_value = mock_processor
        
        manager = StreamManager(StreamBackend.REDIS)
        await manager.start()
        
        metrics = manager.get_metrics()
        
        assert "messages_processed" in metrics
        assert "backend" in metrics
        assert "streams_configured" in metrics
        assert "running" in metrics
        assert metrics["running"] == True
    
    @patch('redaptive.streaming.stream_manager.REDIS_AVAILABLE', True)
    @patch('redaptive.streaming.stream_manager.RedisStreamProcessor')
    @pytest.mark.asyncio
    async def test_health_check(self, mock_redis_processor):
        """Test health check."""
        mock_processor = Mock()
        mock_processor.connect = AsyncMock(return_value=True)
        mock_processor.health_check = AsyncMock(return_value={
            "status": "healthy",
            "redis_connected": True
        })
        mock_processor.register_processor = Mock()
        mock_redis_processor.return_value = mock_processor
        
        manager = StreamManager(StreamBackend.REDIS)
        await manager.start()
        
        health = await manager.health_check()
        
        assert "stream_manager" in health
        assert "processor" in health
        assert health["stream_manager"]["status"] == "healthy"
        assert health["processor"]["status"] == "healthy"