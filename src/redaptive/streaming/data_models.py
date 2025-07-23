"""
Data models for IoT streaming.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum
import json


class MeterType(Enum):
    """Energy meter types."""
    ELECTRICITY = "electricity"
    GAS = "gas"
    WATER = "water"
    STEAM = "steam"
    CHILLED_WATER = "chilled_water"


class MessageType(Enum):
    """Stream message types."""
    METER_READING = "meter_reading"
    ALERT = "alert"
    ANOMALY = "anomaly"
    DIAGNOSTIC = "diagnostic"
    HEARTBEAT = "heartbeat"


class ProcessingStatus(Enum):
    """Processing status for stream messages."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class MeterReading:
    """Standardized meter reading data model."""
    meter_id: str
    building_id: str
    meter_type: MeterType
    timestamp: datetime
    value: float
    unit: str
    quality_score: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "meter_id": self.meter_id,
            "building_id": self.building_id,
            "meter_type": self.meter_type.value,
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "unit": self.unit,
            "quality_score": self.quality_score,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MeterReading":
        """Create from dictionary."""
        return cls(
            meter_id=data["meter_id"],
            building_id=data["building_id"],
            meter_type=MeterType(data["meter_type"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            value=float(data["value"]),
            unit=data["unit"],
            quality_score=float(data.get("quality_score", 1.0)),
            metadata=data.get("metadata", {})
        )


@dataclass
class StreamMessage:
    """Generic stream message wrapper."""
    message_id: str
    message_type: MessageType
    source: str
    timestamp: datetime
    payload: Dict[str, Any]
    priority: int = 0
    retry_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        data = {
            "message_id": self.message_id,
            "message_type": self.message_type.value,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "payload": self.payload,
            "priority": self.priority,
            "retry_count": self.retry_count,
            "metadata": self.metadata
        }
        return json.dumps(data)
    
    @classmethod
    def from_json(cls, json_str: str) -> "StreamMessage":
        """Create from JSON string."""
        data = json.loads(json_str)
        return cls(
            message_id=data["message_id"],
            message_type=MessageType(data["message_type"]),
            source=data["source"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            payload=data["payload"],
            priority=data.get("priority", 0),
            retry_count=data.get("retry_count", 0),
            metadata=data.get("metadata", {})
        )


@dataclass
class ProcessingResult:
    """Result of stream message processing."""
    message_id: str
    status: ProcessingStatus
    processed_at: datetime
    processing_time_ms: float
    result_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    retry_after: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "message_id": self.message_id,
            "status": self.status.value,
            "processed_at": self.processed_at.isoformat(),
            "processing_time_ms": self.processing_time_ms,
            "result_data": self.result_data,
            "error_message": self.error_message,
            "retry_after": self.retry_after.isoformat() if self.retry_after else None
        }


@dataclass
class StreamConfig:
    """Configuration for stream processing."""
    stream_name: str
    batch_size: int = 100
    max_retries: int = 3
    retry_delay_seconds: int = 60
    dead_letter_queue: Optional[str] = None
    consumer_group: Optional[str] = None
    auto_commit: bool = True
    processing_timeout_seconds: int = 30
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "stream_name": self.stream_name,
            "batch_size": self.batch_size,
            "max_retries": self.max_retries,
            "retry_delay_seconds": self.retry_delay_seconds,
            "dead_letter_queue": self.dead_letter_queue,
            "consumer_group": self.consumer_group,
            "auto_commit": self.auto_commit,
            "processing_timeout_seconds": self.processing_timeout_seconds
        }