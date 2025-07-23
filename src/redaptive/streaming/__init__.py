"""
IoT Stream Processing Infrastructure for Redaptive Platform
===========================================================

Real-time data streaming components for processing 12k+ energy meters
supporting 48k+ data points per hour.
"""

from .redis_client import RedisStreamProcessor
from .kafka_client import KafkaStreamProcessor
from .stream_manager import StreamManager, EnergyStreamManager, StreamBackend
from .data_models import MeterReading, StreamMessage, ProcessingResult

__all__ = [
    "RedisStreamProcessor",
    "KafkaStreamProcessor", 
    "StreamManager",
    "EnergyStreamManager",
    "StreamBackend",
    "MeterReading",
    "StreamMessage",
    "ProcessingResult"
]