# 🔌 API Documentation

**Comprehensive API reference for Redaptive Agentic Platform agents and tools**

## 🌟 Overview

The Redaptive Agentic Platform provides a comprehensive set of APIs for energy intelligence, stream processing, and agent orchestration. All APIs follow the Model Context Protocol (MCP) specification for seamless integration and interoperability.

### API Categories

```
🔌 Redaptive Platform APIs
├── 🔋 Energy Intelligence APIs
│   ├── Portfolio Intelligence API
│   ├── Real-Time Monitoring API
│   └── Energy Finance API
├── 🌊 Stream Processing APIs
│   ├── Stream Management API
│   ├── Data Processing API
│   └── Monitoring API
├── 🧠 Orchestration APIs
│   ├── Agent Management API
│   ├── Workflow Execution API
│   └── Planning API
└── 🛠️ Foundation APIs
    ├── Configuration API
    ├── Database API
    └── Tool Registry API
```

## 🔋 Energy Intelligence APIs

### Portfolio Intelligence API

**Base URL**: `/agents/energy/portfolio`

#### Endpoints

##### `POST /analyze_portfolio_energy_usage`
Comprehensive energy consumption analysis for portfolios

**Request Body**:
```json
{
  "portfolio_id": "port_123",
  "date_range": "2024-01-01:2024-12-31",
  "granularity": "monthly",
  "include_weather": true,
  "include_occupancy": true
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "portfolio_id": "port_123",
    "total_consumption": 1500000.5,
    "total_cost": 180000.75,
    "buildings": [
      {
        "building_id": "bldg_001",
        "consumption": 450000.2,
        "cost": 54000.25,
        "efficiency_score": 0.85
      }
    ],
    "trends": {
      "monthly_consumption": [125000, 130000, 135000],
      "efficiency_trends": [0.82, 0.84, 0.85]
    },
    "analysis_timestamp": "2024-01-15T10:30:00Z"
  }
}
```

##### `POST /identify_optimization_opportunities`
AI-driven identification of energy optimization opportunities

**Request Body**:
```json
{
  "portfolio_id": "port_123",
  "focus_areas": ["efficiency", "cost_reduction", "sustainability"],
  "priority_level": "high",
  "budget_limit": 500000,
  "payback_period": "3y"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "opportunities": [
      {
        "id": "opp_001",
        "type": "HVAC_optimization",
        "description": "Upgrade HVAC system with smart controls",
        "building_id": "bldg_001",
        "estimated_savings": 25000,
        "implementation_cost": 75000,
        "payback_period": "3.0y",
        "priority": "high",
        "confidence": 0.92
      }
    ],
    "total_potential_savings": 125000,
    "total_investment": 300000,
    "roi": 0.42
  }
}
```

##### `POST /calculate_energy_savings`
Precision savings calculations for energy projects

**Request Body**:
```json
{
  "project_id": "proj_456",
  "baseline_period": "2023-01-01:2023-12-31",
  "performance_period": "2024-01-01:2024-12-31",
  "adjustment_factors": ["weather", "occupancy", "operational_changes"]
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "project_id": "proj_456",
    "baseline_consumption": 500000,
    "performance_consumption": 425000,
    "gross_savings": 75000,
    "adjusted_savings": 72500,
    "savings_percentage": 14.5,
    "verification_method": "M&V_option_C",
    "confidence_interval": {
      "lower": 68000,
      "upper": 77000
    }
  }
}
```

### Real-Time Monitoring API

**Base URL**: `/agents/energy/monitoring`

#### Endpoints

##### `POST /process_meter_data`
High-throughput meter data processing

**Request Body**:
```json
{
  "meter_id": "meter_001",
  "data_points": [
    {
      "timestamp": "2024-01-15T10:00:00Z",
      "value": 150.5,
      "unit": "kWh",
      "quality_score": 0.95
    }
  ],
  "validation_rules": ["range_check", "consistency_check"],
  "processing_options": {
    "normalize": true,
    "aggregate": "none"
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "meter_id": "meter_001",
    "processed_points": 1,
    "validation_results": {
      "passed": 1,
      "failed": 0,
      "warnings": []
    },
    "processing_time_ms": 45.2,
    "next_expected": "2024-01-15T10:15:00Z"
  }
}
```

##### `POST /detect_anomalies`
AI-powered anomaly detection

**Request Body**:
```json
{
  "meter_id": "meter_001",
  "data_window": "1h",
  "sensitivity": "high",
  "detection_methods": ["statistical", "ml_based"],
  "alert_threshold": 0.8
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "meter_id": "meter_001",
    "anomalies": [
      {
        "id": "anom_001",
        "type": "consumption_spike",
        "severity": "high",
        "confidence": 0.92,
        "timestamp": "2024-01-15T10:30:00Z",
        "value": 250.0,
        "expected_range": [120, 180],
        "impact": "Consumption 39% above expected"
      }
    ],
    "analysis_window": "2024-01-15T09:30:00Z:2024-01-15T10:30:00Z",
    "detection_time_ms": 85.3
  }
}
```

##### `POST /generate_alerts`
Intelligent alert generation and management

**Request Body**:
```json
{
  "meter_id": "meter_001",
  "alert_type": "consumption_anomaly",
  "severity": "high",
  "data": {
    "anomaly_id": "anom_001",
    "description": "Consumption spike detected",
    "impact": "39% above expected"
  },
  "notification_channels": ["email", "sms", "webhook"]
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "alert_id": "alert_001",
    "created_at": "2024-01-15T10:30:00Z",
    "status": "active",
    "notifications_sent": 3,
    "escalation_level": 1,
    "estimated_resolution": "2024-01-15T11:00:00Z"
  }
}
```

### Energy Finance API

**Base URL**: `/agents/energy/finance`

#### Endpoints

##### `POST /calculate_project_roi`
Comprehensive ROI calculations for energy projects

**Request Body**:
```json
{
  "project_id": "proj_456",
  "investment_amount": 500000,
  "time_horizon": "10y",
  "discount_rate": 0.08,
  "escalation_rate": 0.03,
  "analysis_type": "detailed"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "project_id": "proj_456",
    "roi_metrics": {
      "simple_roi": 0.42,
      "npv": 125000,
      "irr": 0.15,
      "payback_period": "3.2y",
      "discounted_payback": "4.1y"
    },
    "cash_flows": [
      {"year": 1, "savings": 75000, "costs": 25000, "net": 50000},
      {"year": 2, "savings": 77250, "costs": 25750, "net": 51500}
    ],
    "risk_analysis": {
      "sensitivity": {"discount_rate": 0.05, "savings": 0.8},
      "scenario_analysis": {
        "optimistic": {"npv": 185000, "irr": 0.22},
        "base_case": {"npv": 125000, "irr": 0.15},
        "pessimistic": {"npv": 65000, "irr": 0.08}
      }
    }
  }
}
```

##### `POST /optimize_eaas_contract`
EaaS contract optimization and analysis

**Request Body**:
```json
{
  "contract_id": "contract_789",
  "optimization_goals": ["revenue_max", "risk_min"],
  "constraints": ["regulatory", "technical", "operational"],
  "contract_terms": {
    "duration": "10y",
    "performance_guarantee": 0.15,
    "sharing_ratio": 0.8
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "contract_id": "contract_789",
    "optimization_results": {
      "recommended_terms": {
        "sharing_ratio": 0.85,
        "performance_guarantee": 0.12,
        "escalation_clause": "cpi_based"
      },
      "financial_impact": {
        "revenue_increase": 125000,
        "risk_reduction": 0.15,
        "expected_roi": 0.38
      }
    },
    "alternative_structures": [
      {
        "name": "Fixed Payment",
        "benefits": ["Predictable revenue", "Lower risk"],
        "drawbacks": ["Limited upside", "No performance incentive"]
      }
    ]
  }
}
```

## 🌊 Stream Processing APIs

### Stream Management API

**Base URL**: `/streaming/management`

#### Endpoints

##### `POST /streams/{stream_name}/publish`
Publish messages to streams

**Request Body**:
```json
{
  "messages": [
    {
      "message_id": "msg_001",
      "message_type": "meter_reading",
      "source": "energy_meter",
      "timestamp": "2024-01-15T10:30:00Z",
      "payload": {
        "meter_id": "meter_001",
        "value": 150.5,
        "unit": "kWh"
      },
      "priority": 1
    }
  ],
  "partition_key": "building_001"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "published_count": 1,
    "message_ids": ["msg_001"],
    "stream_name": "energy_readings",
    "partition": 0,
    "offset": 12345
  }
}
```

##### `GET /streams/{stream_name}/info`
Get stream information and metrics

**Response**:
```json
{
  "status": "success",
  "data": {
    "stream_name": "energy_readings",
    "message_count": 125000,
    "consumer_groups": 3,
    "active_consumers": 8,
    "partition_count": 12,
    "retention_period": "7d",
    "throughput": {
      "messages_per_second": 1250,
      "bytes_per_second": 512000
    }
  }
}
```

##### `GET /consumers/{consumer_group}/status`
Get consumer group status

**Response**:
```json
{
  "status": "success",
  "data": {
    "consumer_group": "energy_processors",
    "active_consumers": 5,
    "lag": 125,
    "consumers": [
      {
        "consumer_id": "consumer_001",
        "status": "running",
        "processed_messages": 15000,
        "last_processed": "2024-01-15T10:29:45Z"
      }
    ]
  }
}
```

### Data Processing API

**Base URL**: `/streaming/processing`

#### Endpoints

##### `POST /process/meter_readings`
Process meter readings through streaming pipeline

**Request Body**:
```json
{
  "meter_readings": [
    {
      "meter_id": "meter_001",
      "building_id": "building_001",
      "timestamp": "2024-01-15T10:30:00Z",
      "value": 150.5,
      "unit": "kWh",
      "quality_score": 0.95
    }
  ],
  "processing_options": {
    "validate": true,
    "normalize": true,
    "detect_anomalies": true
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "processed_count": 1,
    "validation_results": {
      "valid": 1,
      "invalid": 0
    },
    "anomalies_detected": 0,
    "processing_time_ms": 45.2,
    "next_steps": ["storage", "analysis"]
  }
}
```

## 🧠 Orchestration APIs

### Agent Management API

**Base URL**: `/orchestration/agents`

#### Endpoints

##### `GET /agents`
List all available agents

**Response**:
```json
{
  "status": "success",
  "data": {
    "agents": [
      {
        "agent_id": "portfolio_intelligence",
        "name": "Portfolio Intelligence Agent",
        "status": "active",
        "capabilities": [
          "analyze_portfolio_energy_usage",
          "identify_optimization_opportunities"
        ],
        "load": 0.25,
        "last_health_check": "2024-01-15T10:30:00Z"
      }
    ],
    "total_agents": 5,
    "active_agents": 4
  }
}
```

##### `POST /agents/{agent_id}/execute`
Execute agent tool

**Request Body**:
```json
{
  "tool_name": "analyze_portfolio_energy_usage",
  "parameters": {
    "portfolio_id": "port_123",
    "date_range": "2024-01-01:2024-12-31"
  },
  "execution_options": {
    "timeout": 30000,
    "retry_count": 3
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "execution_id": "exec_001",
    "agent_id": "portfolio_intelligence",
    "tool_name": "analyze_portfolio_energy_usage",
    "result": {
      "portfolio_id": "port_123",
      "total_consumption": 1500000.5,
      "analysis_timestamp": "2024-01-15T10:30:00Z"
    },
    "execution_time_ms": 850,
    "completed_at": "2024-01-15T10:30:00Z"
  }
}
```

### Workflow Execution API

**Base URL**: `/orchestration/workflows`

#### Endpoints

##### `POST /workflows/execute`
Execute multi-agent workflow

**Request Body**:
```json
{
  "workflow_name": "comprehensive_energy_analysis",
  "parameters": {
    "portfolio_id": "port_123",
    "analysis_depth": "comprehensive"
  },
  "execution_options": {
    "parallel_execution": true,
    "timeout": 120000
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "workflow_id": "wf_001",
    "execution_id": "exec_002",
    "status": "running",
    "steps": [
      {
        "step_id": "step_001",
        "agent_id": "portfolio_intelligence",
        "status": "completed",
        "result": {...}
      },
      {
        "step_id": "step_002",
        "agent_id": "monitoring",
        "status": "running",
        "progress": 0.65
      }
    ],
    "estimated_completion": "2024-01-15T10:32:00Z"
  }
}
```

## 🛠️ Foundation APIs

### Configuration API

**Base URL**: `/config`

#### Endpoints

##### `GET /config/agents/{agent_id}`
Get agent configuration

**Response**:
```json
{
  "status": "success",
  "data": {
    "agent_id": "portfolio_intelligence",
    "configuration": {
      "analysis_depth": "comprehensive",
      "forecasting_horizon": "12m",
      "optimization_algorithm": "genetic_algorithm",
      "cache_ttl": 3600
    },
    "last_updated": "2024-01-15T09:00:00Z"
  }
}
```

##### `PUT /config/agents/{agent_id}`
Update agent configuration

**Request Body**:
```json
{
  "configuration": {
    "analysis_depth": "detailed",
    "forecasting_horizon": "18m",
    "optimization_algorithm": "simulated_annealing"
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "agent_id": "portfolio_intelligence",
    "updated_fields": ["analysis_depth", "forecasting_horizon", "optimization_algorithm"],
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

## 🔐 Authentication

### API Key Authentication

All API requests require authentication using API keys:

```http
Authorization: Bearer your_api_key_here
Content-Type: application/json
```

### OAuth 2.0 Authentication

For user-based authentication:

```http
Authorization: Bearer oauth_access_token
Content-Type: application/json
```

### Rate Limiting

API endpoints are subject to rate limiting:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642262400
```

## 📊 Response Formats

### Success Response

```json
{
  "status": "success",
  "data": {
    // Response data
  },
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_001",
    "execution_time_ms": 150
  }
}
```

### Error Response

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "Portfolio ID is required",
    "details": {
      "parameter": "portfolio_id",
      "expected": "string",
      "received": "null"
    }
  },
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_002"
  }
}
```

## 🔄 Webhooks

### Webhook Configuration

Configure webhooks to receive real-time notifications:

```json
{
  "webhook_url": "https://your-domain.com/webhooks/energy",
  "events": ["anomaly_detected", "analysis_completed"],
  "authentication": {
    "type": "bearer_token",
    "token": "webhook_secret_token"
  }
}
```

### Webhook Payload

```json
{
  "event": "anomaly_detected",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "meter_id": "meter_001",
    "anomaly_type": "consumption_spike",
    "severity": "high",
    "confidence": 0.92
  },
  "metadata": {
    "agent_id": "monitoring",
    "webhook_id": "webhook_001"
  }
}
```

## 📈 Metrics and Monitoring

### API Metrics

Monitor API performance and usage:

```json
{
  "api_metrics": {
    "requests_per_second": 125,
    "average_response_time_ms": 250,
    "error_rate": 0.002,
    "uptime": 0.9999
  },
  "agent_metrics": {
    "active_agents": 5,
    "total_executions": 15000,
    "success_rate": 0.998
  }
}
```

### Health Check Endpoint

**GET `/health`**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "kafka": "healthy",
    "agents": "healthy"
  },
  "uptime": 86400
}
```

## 🚀 SDK and Client Libraries

### Python SDK

```python
from redaptive_sdk import RedaptiveClient

# Initialize client
client = RedaptiveClient(
    api_key="your_api_key",
    base_url="https://api.redaptive.com"
)

# Portfolio analysis
result = await client.energy.portfolio.analyze_energy_usage(
    portfolio_id="port_123",
    date_range="2024-01-01:2024-12-31"
)

# Real-time monitoring
anomalies = await client.energy.monitoring.detect_anomalies(
    meter_id="meter_001",
    sensitivity="high"
)
```

### JavaScript SDK

```javascript
import { RedaptiveClient } from '@redaptive/sdk';

const client = new RedaptiveClient({
  apiKey: 'your_api_key',
  baseUrl: 'https://api.redaptive.com'
});

// Portfolio analysis
const result = await client.energy.portfolio.analyzeEnergyUsage({
  portfolioId: 'port_123',
  dateRange: '2024-01-01:2024-12-31'
});

// Real-time monitoring
const anomalies = await client.energy.monitoring.detectAnomalies({
  meterId: 'meter_001',
  sensitivity: 'high'
});
```

## 📚 Related Documentation

- **[Energy Agents](../agents/energy/)** - Detailed agent documentation
- **[Streaming Architecture](../streaming/)** - Stream processing infrastructure
- **[Deployment Guide](../deployment/)** - Production deployment strategies
- **[Development Guide](../development/)** - Building applications with the API

---

**🔌 Redaptive Platform APIs** - Comprehensive API suite for intelligent energy management and automation.