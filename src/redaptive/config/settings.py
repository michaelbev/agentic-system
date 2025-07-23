"""
Centralized configuration management for the Redaptive Agentic Platform.
"""

import os
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class DatabaseSettings:
    """Database configuration settings."""
    host: str = "localhost"
    port: int = 5432
    name: str = "energy_db"
    user: str = "energy_user"
    password: str = ""
    
    @classmethod
    def from_env(cls) -> "DatabaseSettings":
        """Load database settings from environment variables."""
        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            name=os.getenv("DB_NAME", "energy_db"),
            user=os.getenv("DB_ENERGYAPP_USER", "energy_user"),
            password=os.getenv("DB_ENERGYAPP_PASSWORD", "")
        )


@dataclass
class AgentSettings:
    """Agent configuration settings."""
    max_concurrent_agents: int = 10
    default_timeout: int = 30
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> "AgentSettings":
        """Load agent settings from environment variables."""
        return cls(
            max_concurrent_agents=int(os.getenv("MAX_CONCURRENT_AGENTS", "10")),
            default_timeout=int(os.getenv("AGENT_TIMEOUT", "30")),
            log_level=os.getenv("LOG_LEVEL", "INFO")
        )


@dataclass
class OrchestrationSettings:
    """Orchestration engine configuration."""
    enable_intelligent_routing: bool = True
    max_workflow_depth: int = 10
    cache_enabled: bool = True
    
    @classmethod
    def from_env(cls) -> "OrchestrationSettings":
        """Load orchestration settings from environment variables."""
        return cls(
            enable_intelligent_routing=os.getenv("ENABLE_INTELLIGENT_ROUTING", "true").lower() == "true",
            max_workflow_depth=int(os.getenv("MAX_WORKFLOW_DEPTH", "10")),
            cache_enabled=os.getenv("CACHE_ENABLED", "true").lower() == "true"
        )


@dataclass
class StreamingSettings:
    """Streaming configuration for IoT data processing."""
    backend: str = "auto"  # auto, redis, kafka
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_security_protocol: str = "PLAINTEXT"
    batch_size: int = 100
    max_retries: int = 3
    consumer_timeout: int = 30
    
    @classmethod
    def from_env(cls) -> "StreamingSettings":
        """Load streaming settings from environment variables."""
        return cls(
            backend=os.getenv("STREAMING_BACKEND", "auto"),
            redis_host=os.getenv("REDIS_HOST", "localhost"),
            redis_port=int(os.getenv("REDIS_PORT", "6379")),
            redis_password=os.getenv("REDIS_PASSWORD", ""),
            redis_db=int(os.getenv("REDIS_DB", "0")),
            kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            kafka_security_protocol=os.getenv("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT"),
            batch_size=int(os.getenv("STREAMING_BATCH_SIZE", "100")),
            max_retries=int(os.getenv("STREAMING_MAX_RETRIES", "3")),
            consumer_timeout=int(os.getenv("STREAMING_CONSUMER_TIMEOUT", "30"))
        )


@dataclass
class PlatformSettings:
    """Main platform configuration."""
    database: DatabaseSettings = field(default_factory=DatabaseSettings.from_env)
    agents: AgentSettings = field(default_factory=AgentSettings.from_env)
    orchestration: OrchestrationSettings = field(default_factory=OrchestrationSettings.from_env)
    streaming: StreamingSettings = field(default_factory=StreamingSettings.from_env)
    environment: str = "development"
    debug: bool = False
    api_version: str = "v1"
    
    @classmethod
    def from_env(cls) -> "PlatformSettings":
        """Load all settings from environment variables."""
        return cls(
            environment=os.getenv("ENVIRONMENT", "development"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            api_version=os.getenv("API_VERSION", "v1"),
            database=DatabaseSettings.from_env(),
            agents=AgentSettings.from_env(),
            orchestration=OrchestrationSettings.from_env(),
            streaming=StreamingSettings.from_env()
        )


# Global settings instance
settings = PlatformSettings.from_env()