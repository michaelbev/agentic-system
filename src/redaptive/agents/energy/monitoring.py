#!/usr/bin/env python3
"""
Real-time Energy Monitoring Agent - Redaptive Energy-as-a-Service Platform

This agent provides real-time monitoring capabilities for 12,000+ energy meters,
supporting Redaptive's IoT infrastructure and energy analytics platform.

Key capabilities:
- Real-time energy meter data processing (12k+ meters, 48k+ data points/hour)
- Anomaly detection and alerting
- Performance monitoring and diagnostics
- Field engineer alert system
- Energy usage pattern analysis
- Demand response management
- Equipment failure prediction
- Energy efficiency monitoring
"""

import sys
import os
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import statistics
import math

from redaptive.agents.base import BaseMCPServer
from redaptive.config.database import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnergyMonitoringAgent(BaseMCPServer):
    """
    Real-time Energy Monitoring Agent for Redaptive's IoT Energy Infrastructure
    
    Handles real-time processing of 12,000+ energy meters with advanced
    anomaly detection, alerting, and performance monitoring capabilities.
    """

    def __init__(self):
        super().__init__("energy-monitoring-agent")
        self.meter_data_cache = {}
        self.anomaly_thresholds = {
            "consumption_spike": 2.5,  # Standard deviations
            "consumption_drop": 2.0,
            "efficiency_drop": 0.15,   # 15% efficiency drop
            "equipment_temp": 85.0,    # Celsius
            "power_factor": 0.85       # Minimum power factor
        }
        self.alert_rules = {}
        self.setup_tools()
        logger.info("Real-time Energy Monitoring Agent initialized for 12k+ meters")

    def setup_tools(self):
        """Setup MCP tools for real-time energy monitoring"""
        
        # Tool 1: Get Latest Energy Usage Reading
        self.register_tool(
            "get_latest_energy_reading",
            "Get the most recent energy usage reading from the database",
            self.get_latest_energy_reading,
            {
                "type": "object",
                "properties": {
                    "meter_id": {
                        "type": "string",
                        "description": "Specific meter ID to query (optional, will get latest from all meters if not specified)"
                    },
                    "include_details": {
                        "type": "boolean",
                        "description": "Include detailed reading information",
                        "default": True
                    }
                }
            }
        )
        
        # Tool 2: Process Real-time Meter Data
        self.register_tool(
            "process_meter_data",
            "Process real-time data from energy meters with anomaly detection",
            self.process_meter_data,
            {
                "type": "object",
                "properties": {
                    "meter_readings": {
                        "type": "array",
                        "description": "Array of meter readings",
                        "items": {
                            "type": "object",
                            "properties": {
                                "meter_id": {"type": "string", "description": "Unique meter identifier"},
                                "timestamp": {"type": "string", "description": "Reading timestamp (ISO 8601)"},
                                "energy_kwh": {"type": "number", "description": "Energy consumption in kWh"},
                                "power_kw": {"type": "number", "description": "Current power in kW"},
                                "voltage": {"type": "number", "description": "Voltage reading"},
                                "current": {"type": "number", "description": "Current in amperes"},
                                "power_factor": {"type": "number", "description": "Power factor"},
                                "temperature": {"type": "number", "description": "Equipment temperature in Celsius"}
                            },
                            "required": ["meter_id", "timestamp", "energy_kwh", "power_kw"]
                        }
                    },
                    "enable_anomaly_detection": {
                        "type": "boolean",
                        "description": "Enable anomaly detection processing",
                        "default": True
                    },
                    "alert_threshold": {
                        "type": "string",
                        "description": "Alert sensitivity level",
                        "enum": ["low", "medium", "high"],
                        "default": "medium"
                    }
                },
                "required": ["meter_readings"]
            }
        )

        # Tool 3: Detect Energy Anomalies
        self.register_tool(
            "detect_anomalies",
            "Detect energy consumption and equipment anomalies",
            self.detect_anomalies,
            {
                "type": "object",
                "properties": {
                    "meter_id": {
                        "type": "string",
                        "description": "Meter identifier to analyze"
                    },
                    "analysis_window": {
                        "type": "integer",
                        "description": "Analysis window in hours",
                        "default": 24
                    },
                    "anomaly_types": {
                        "type": "array",
                        "description": "Types of anomalies to detect",
                        "items": {
                            "type": "string",
                            "enum": ["consumption_spike", "consumption_drop", "efficiency_drop", "equipment_overheating", "power_quality"]
                        },
                        "default": ["consumption_spike", "consumption_drop", "equipment_overheating"]
                    },
                    "sensitivity": {
                        "type": "string",
                        "description": "Detection sensitivity",
                        "enum": ["low", "medium", "high"],
                        "default": "medium"
                    }
                },
                "required": ["meter_id"]
            }
        )

        # Tool 4: Generate Field Engineer Alerts
        self.register_tool(
            "generate_field_alert",
            "Generate alerts for field engineers based on anomalies or equipment issues",
            self.generate_field_alert,
            {
                "type": "object",
                "properties": {
                    "alert_type": {
                        "type": "string",
                        "description": "Type of alert",
                        "enum": ["equipment_failure", "consumption_anomaly", "efficiency_issue", "maintenance_required", "emergency"]
                    },
                    "meter_id": {
                        "type": "string",
                        "description": "Affected meter identifier"
                    },
                    "severity": {
                        "type": "string",
                        "description": "Alert severity level",
                        "enum": ["low", "medium", "high", "critical"]
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the issue"
                    },
                    "recommended_action": {
                        "type": "string",
                        "description": "Recommended action for field engineer"
                    },
                    "priority": {
                        "type": "integer",
                        "description": "Priority level (1-10, 10 being highest)",
                        "minimum": 1,
                        "maximum": 10,
                        "default": 5
                    },
                    "location_info": {
                        "type": "object",
                        "description": "Location information for the field engineer",
                        "properties": {
                            "building_id": {"type": "string", "description": "Building identifier"},
                            "floor": {"type": "string", "description": "Floor location"},
                            "room": {"type": "string", "description": "Room or area"},
                            "coordinates": {"type": "string", "description": "GPS coordinates if available"}
                        }
                    }
                },
                "required": ["alert_type", "meter_id", "severity", "description"]
            }
        )

        # Tool 5: Monitor Equipment Performance
        self.register_tool(
            "monitor_equipment_performance",
            "Monitor and analyze equipment performance metrics",
            self.monitor_equipment_performance,
            {
                "type": "object",
                "properties": {
                    "equipment_id": {
                        "type": "string",
                        "description": "Equipment identifier"
                    },
                    "performance_metrics": {
                        "type": "array",
                        "description": "Performance metrics to monitor",
                        "items": {
                            "type": "string",
                            "enum": ["efficiency", "power_factor", "load_profile", "temperature", "vibration", "runtime_hours"]
                        },
                        "default": ["efficiency", "power_factor", "temperature"]
                    },
                    "monitoring_period": {
                        "type": "integer",
                        "description": "Monitoring period in hours",
                        "default": 24
                    },
                    "baseline_comparison": {
                        "type": "boolean",
                        "description": "Compare against baseline performance",
                        "default": True
                    }
                },
                "required": ["equipment_id"]
            }
        )

        # Tool 6: Analyze Energy Usage Patterns
        self.register_tool(
            "analyze_usage_patterns",
            "Analyze energy usage patterns for optimization opportunities",
            self.analyze_usage_patterns,
            {
                "type": "object",
                "properties": {
                    "scope": {
                        "type": "string",
                        "description": "Analysis scope",
                        "enum": ["single_meter", "building", "portfolio", "meter_group"]
                    },
                    "identifier": {
                        "type": "string",
                        "description": "Identifier for the scope (meter_id, building_id, etc.)"
                    },
                    "pattern_types": {
                        "type": "array",
                        "description": "Types of patterns to analyze",
                        "items": {
                            "type": "string",
                            "enum": ["daily_profile", "weekly_profile", "seasonal_trends", "load_curves", "peak_demand", "baseline_drift"]
                        },
                        "default": ["daily_profile", "weekly_profile", "peak_demand"]
                    },
                    "time_range": {
                        "type": "object",
                        "description": "Time range for analysis",
                        "properties": {
                            "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                            "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"}
                        },
                        "required": ["start_date", "end_date"]
                    },
                    "generate_recommendations": {
                        "type": "boolean",
                        "description": "Generate optimization recommendations",
                        "default": True
                    }
                },
                "required": ["scope", "identifier", "time_range"]
            }
        )

        # Tool 7: Real-time Demand Response
        self.register_tool(
            "manage_demand_response",
            "Manage demand response events and load shedding",
            self.manage_demand_response,
            {
                "type": "object",
                "properties": {
                    "event_type": {
                        "type": "string",
                        "description": "Type of demand response event",
                        "enum": ["peak_shaving", "load_shedding", "emergency_reduction", "scheduled_reduction"]
                    },
                    "target_reduction": {
                        "type": "number",
                        "description": "Target load reduction in kW"
                    },
                    "affected_meters": {
                        "type": "array",
                        "description": "List of affected meter IDs",
                        "items": {"type": "string"}
                    },
                    "duration": {
                        "type": "integer",
                        "description": "Event duration in minutes"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Event start time (ISO 8601)"
                    },
                    "priority_loads": {
                        "type": "array",
                        "description": "Critical loads to protect",
                        "items": {"type": "string"}
                    },
                    "auto_execute": {
                        "type": "boolean",
                        "description": "Automatically execute demand response",
                        "default": False
                    }
                },
                "required": ["event_type", "target_reduction", "affected_meters", "duration"]
            }
        )

    async def get_latest_energy_reading(self, meter_id: Optional[str] = None, include_details: bool = True) -> Dict[str, Any]:
        """Get the most recent energy usage reading from the database."""
        try:
            # Build the SQL query
            if meter_id:
                sql = """
                    SELECT 
                        eu.usage_id,
                        eu.meter_id,
                        eu.building_id,
                        eu.reading_date,
                        eu.energy_type,
                        eu.energy_consumption,
                        eu.energy_cost,
                        eu.demand_kw,
                        eu.power_factor,
                        eu.weather_temp_f,
                        eu.occupancy_percentage,
                        em.meter_type,
                        em.energy_type as meter_energy_type
                    FROM energy_usage eu
                    LEFT JOIN energy_meters em ON eu.meter_id = em.meter_id
                    WHERE eu.meter_id = %s
                    ORDER BY eu.reading_date DESC
                    LIMIT 1
                """
                params = (meter_id,)
            else:
                sql = """
                    SELECT 
                        eu.usage_id,
                        eu.meter_id,
                        eu.building_id,
                        eu.reading_date,
                        eu.energy_type,
                        eu.energy_consumption,
                        eu.energy_cost,
                        eu.demand_kw,
                        eu.power_factor,
                        eu.weather_temp_f,
                        eu.occupancy_percentage,
                        em.meter_type,
                        em.energy_type as meter_energy_type
                    FROM energy_usage eu
                    LEFT JOIN energy_meters em ON eu.meter_id = em.meter_id
                    ORDER BY eu.reading_date DESC
                    LIMIT 1
                """
                params = ()

            with db.get_cursor() as cursor:
                cursor.execute(sql, params)
                reading_data = cursor.fetchone()

            if not reading_data:
                return {
                    "status": "no_data",
                    "message": f"No energy readings found for meter {meter_id if meter_id else 'all meters'}"
                }

            # Convert reading_data to dict if it's not already
            if hasattr(reading_data, '_asdict'):
                reading_data = reading_data._asdict()

            if include_details:
                return {
                    "status": "success",
                    "usage_id": str(reading_data["usage_id"]),
                    "meter_id": reading_data["meter_id"],
                    "building_id": reading_data["building_id"],
                    "timestamp": reading_data["reading_date"].isoformat() if reading_data["reading_date"] else None,
                    "energy_type": reading_data["energy_type"],
                    "energy_kwh": float(reading_data["energy_consumption"]) if reading_data["energy_consumption"] else None,
                    "energy_cost": float(reading_data["energy_cost"]) if reading_data["energy_cost"] else None,
                    "power_kw": float(reading_data["demand_kw"]) if reading_data["demand_kw"] else None,
                    "power_factor": float(reading_data["power_factor"]) if reading_data["power_factor"] else None,
                    "temperature_f": float(reading_data["weather_temp_f"]) if reading_data["weather_temp_f"] else None,
                    "occupancy_percentage": float(reading_data["occupancy_percentage"]) if reading_data["occupancy_percentage"] else None,
                    "meter_type": reading_data["meter_type"],
                    "meter_energy_type": reading_data["meter_energy_type"]
                }
            else:
                return {
                    "status": "success",
                    "meter_id": reading_data["meter_id"],
                    "timestamp": reading_data["reading_date"].isoformat() if reading_data["reading_date"] else None,
                    "energy_kwh": float(reading_data["energy_consumption"]) if reading_data["energy_consumption"] else None,
                    "power_kw": float(reading_data["demand_kw"]) if reading_data["demand_kw"] else None
                }
        except Exception as e:
            logger.error(f"Error getting latest energy reading: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def process_meter_data(self, meter_readings: List[Dict], enable_anomaly_detection: bool = True, alert_threshold: str = "medium") -> Dict[str, Any]:
        """Process real-time meter data with anomaly detection"""
        try:
            # If no meter_readings provided, get the latest from database
            if not meter_readings:
                latest_reading_result = await self.get_latest_energy_reading()
                if latest_reading_result.get("status") == "success":
                    meter_readings = [latest_reading_result]
                else:
                    return {
                        "status": "error",
                        "error": "No meter readings provided and no data available in database",
                        "timestamp": datetime.now().isoformat()
                    }
            
            processed_count = 0
            anomalies_detected = []
            alerts_generated = []
            
            for reading in meter_readings:
                meter_id = reading["meter_id"]
                timestamp = reading["timestamp"]
                
                # Store in cache for trend analysis
                if meter_id not in self.meter_data_cache:
                    self.meter_data_cache[meter_id] = []
                
                self.meter_data_cache[meter_id].append(reading)
                
                # Keep only last 1000 readings per meter for performance
                if len(self.meter_data_cache[meter_id]) > 1000:
                    self.meter_data_cache[meter_id] = self.meter_data_cache[meter_id][-1000:]
                
                # Anomaly detection
                if enable_anomaly_detection:
                    anomaly = await self._detect_real_time_anomaly(reading, alert_threshold)
                    if anomaly:
                        anomalies_detected.append(anomaly)
                        
                        # Generate alert if severe
                        if anomaly["severity"] in ["high", "critical"]:
                            alert = await self._generate_anomaly_alert(anomaly)
                            alerts_generated.append(alert)
                
                processed_count += 1
            
            # Calculate processing statistics
            processing_rate = processed_count / max(1, len(meter_readings)) * 100
            
            result = {
                "status": "success",
                "processed_readings": processed_count,
                "total_readings": len(meter_readings),
                "processing_rate": f"{processing_rate:.1f}%",
                "anomalies_detected": len(anomalies_detected),
                "alerts_generated": len(alerts_generated),
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "anomalies": anomalies_detected[:10],  # Show first 10
                    "alerts": alerts_generated,
                    "processing_summary": {
                        "meters_processed": len(set(r["meter_id"] for r in meter_readings)),
                        "time_span": self._calculate_time_span(meter_readings),
                        "data_quality": self._assess_data_quality(meter_readings)
                    }
                }
            }
            
            logger.info(f"Processed {processed_count} meter readings, detected {len(anomalies_detected)} anomalies")
            return result
            
        except Exception as e:
            logger.error(f"Error processing meter data: {e}")
            return {
                "status": "error",
                "error": str(e),
                "processed_readings": 0,
                "timestamp": datetime.now().isoformat()
            }

    async def detect_anomalies(self, meter_id: str, analysis_window: int = 24, anomaly_types: List[str] = None, sensitivity: str = "medium") -> Dict[str, Any]:
        """Detect energy anomalies for a specific meter"""
        try:
            if anomaly_types is None:
                anomaly_types = ["consumption_spike", "consumption_drop", "equipment_overheating"]
            
            if meter_id not in self.meter_data_cache:
                return {
                    "status": "error",
                    "error": f"No data available for meter {meter_id}",
                    "meter_id": meter_id
                }
            
            meter_data = self.meter_data_cache[meter_id]
            cutoff_time = datetime.now() - timedelta(hours=analysis_window)
            
            # Filter data within analysis window
            recent_data = [
                reading for reading in meter_data
                if datetime.fromisoformat(reading["timestamp"].replace('Z', '+00:00')) > cutoff_time
            ]
            
            if len(recent_data) < 10:
                return {
                    "status": "insufficient_data",
                    "message": f"Insufficient data for analysis (need at least 10 readings, have {len(recent_data)})",
                    "meter_id": meter_id
                }
            
            anomalies = []
            
            # Analyze each anomaly type
            for anomaly_type in anomaly_types:
                detected = await self._analyze_anomaly_type(recent_data, anomaly_type, sensitivity)
                anomalies.extend(detected)
            
            # Calculate anomaly statistics
            severity_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
            for anomaly in anomalies:
                severity_counts[anomaly.get("severity", "low")] += 1
            
            result = {
                "status": "success",
                "meter_id": meter_id,
                "analysis_window_hours": analysis_window,
                "data_points_analyzed": len(recent_data),
                "anomalies_detected": len(anomalies),
                "severity_breakdown": severity_counts,
                "anomalies": anomalies,
                "analysis_summary": {
                    "avg_consumption": statistics.mean([r["energy_kwh"] for r in recent_data]),
                    "peak_power": max([r["power_kw"] for r in recent_data]),
                    "data_quality_score": self._calculate_data_quality_score(recent_data),
                    "trending": self._calculate_trend(recent_data)
                },
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Anomaly analysis for {meter_id}: {len(anomalies)} anomalies detected")
            return result
            
        except Exception as e:
            logger.error(f"Error detecting anomalies for {meter_id}: {e}")
            return {
                "status": "error",
                "error": str(e),
                "meter_id": meter_id,
                "timestamp": datetime.now().isoformat()
            }

    async def generate_field_alert(self, alert_type: str, meter_id: str, severity: str, description: str, 
                                 recommended_action: str = None, priority: int = 5, location_info: Dict = None) -> Dict[str, Any]:
        """Generate alerts for field engineers"""
        try:
            alert_id = f"ALERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{meter_id}"
            
            alert = {
                "alert_id": alert_id,
                "alert_type": alert_type,
                "meter_id": meter_id,
                "severity": severity,
                "priority": priority,
                "description": description,
                "recommended_action": recommended_action or self._get_default_action(alert_type),
                "location_info": location_info or self._get_meter_location(meter_id),
                "created_timestamp": datetime.now().isoformat(),
                "status": "open",
                "estimated_response_time": self._calculate_response_time(severity, priority),
                "required_tools": self._get_required_tools(alert_type),
                "safety_considerations": self._get_safety_considerations(alert_type)
            }
            
            # Store alert (in production, this would go to a real alerting system)
            logger.info(f"Generated field alert {alert_id} for meter {meter_id} - {severity} severity")
            
            return {
                "status": "success",
                "alert": alert,
                "notification_sent": True,
                "field_engineer_assigned": self._assign_field_engineer(location_info, priority),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating field alert: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def monitor_equipment_performance(self, equipment_id: str, performance_metrics: List[str] = None, 
                                          monitoring_period: int = 24, baseline_comparison: bool = True) -> Dict[str, Any]:
        """Monitor equipment performance metrics"""
        try:
            if performance_metrics is None:
                performance_metrics = ["efficiency", "power_factor", "temperature"]
            
            # Simulate equipment performance data (in production, this would query real data)
            performance_data = await self._collect_equipment_data(equipment_id, monitoring_period)
            
            analysis_results = {}
            issues_detected = []
            
            for metric in performance_metrics:
                metric_data = performance_data.get(metric, [])
                analysis = await self._analyze_performance_metric(metric, metric_data, baseline_comparison)
                analysis_results[metric] = analysis
                
                if analysis.get("status") == "degraded":
                    issues_detected.append({
                        "metric": metric,
                        "issue": analysis.get("issue"),
                        "severity": analysis.get("severity"),
                        "recommendation": analysis.get("recommendation")
                    })
            
            # Calculate overall performance score
            performance_score = self._calculate_performance_score(analysis_results)
            
            result = {
                "status": "success",
                "equipment_id": equipment_id,
                "monitoring_period_hours": monitoring_period,
                "overall_performance_score": performance_score,
                "performance_status": "optimal" if performance_score > 85 else "degraded" if performance_score > 70 else "poor",
                "metrics_analyzed": performance_metrics,
                "issues_detected": len(issues_detected),
                "detailed_analysis": analysis_results,
                "issues": issues_detected,
                "recommendations": self._generate_performance_recommendations(analysis_results),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Equipment performance analysis for {equipment_id}: Score {performance_score}/100")
            return result
            
        except Exception as e:
            logger.error(f"Error monitoring equipment performance: {e}")
            return {
                "status": "error",
                "error": str(e),
                "equipment_id": equipment_id,
                "timestamp": datetime.now().isoformat()
            }

    async def analyze_usage_patterns(self, scope: str, identifier: str, pattern_types: List[str] = None, 
                                   time_range: Dict[str, str] = None, generate_recommendations: bool = True) -> Dict[str, Any]:
        """Analyze energy usage patterns"""
        try:
            if pattern_types is None:
                pattern_types = ["daily_profile", "weekly_profile", "peak_demand"]
            
            # Simulate pattern analysis (in production, this would analyze real historical data)
            patterns_analysis = {}
            
            for pattern_type in pattern_types:
                pattern_data = await self._analyze_pattern_type(scope, identifier, pattern_type, time_range)
                patterns_analysis[pattern_type] = pattern_data
            
            # Generate insights and recommendations
            insights = self._extract_usage_insights(patterns_analysis)
            recommendations = []
            if generate_recommendations:
                recommendations = self._generate_usage_recommendations(patterns_analysis, insights)
            
            # Calculate potential savings
            savings_potential = self._calculate_savings_potential(patterns_analysis)
            
            result = {
                "status": "success",
                "scope": scope,
                "identifier": identifier,
                "analysis_period": time_range,
                "patterns_analyzed": pattern_types,
                "key_insights": insights,
                "pattern_analysis": patterns_analysis,
                "optimization_opportunities": len(recommendations),
                "recommendations": recommendations,
                "savings_potential": savings_potential,
                "efficiency_score": self._calculate_efficiency_score(patterns_analysis),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Usage pattern analysis for {scope} {identifier}: {len(insights)} insights, {len(recommendations)} recommendations")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing usage patterns: {e}")
            return {
                "status": "error",
                "error": str(e),
                "scope": scope,
                "identifier": identifier,
                "timestamp": datetime.now().isoformat()
            }

    async def manage_demand_response(self, event_type: str, target_reduction: float, affected_meters: List[str], 
                                   duration: int, start_time: str = None, priority_loads: List[str] = None, 
                                   auto_execute: bool = False) -> Dict[str, Any]:
        """Manage demand response events"""
        try:
            event_id = f"DR_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            if start_time is None:
                start_time = datetime.now().isoformat()
            
            # Calculate load reduction strategy
            reduction_strategy = await self._calculate_reduction_strategy(
                target_reduction, affected_meters, priority_loads or []
            )
            
            # Simulate demand response execution
            if auto_execute:
                execution_result = await self._execute_demand_response(reduction_strategy)
            else:
                execution_result = {"status": "pending_approval", "message": "Demand response ready for manual execution"}
            
            result = {
                "status": "success",
                "event_id": event_id,
                "event_type": event_type,
                "target_reduction_kw": target_reduction,
                "affected_meters": len(affected_meters),
                "duration_minutes": duration,
                "start_time": start_time,
                "end_time": (datetime.fromisoformat(start_time) + timedelta(minutes=duration)).isoformat(),
                "reduction_strategy": reduction_strategy,
                "execution_status": execution_result["status"],
                "estimated_actual_reduction": reduction_strategy.get("estimated_reduction", 0),
                "participant_meters": affected_meters,
                "protected_loads": priority_loads or [],
                "auto_executed": auto_execute,
                "compliance_forecast": self._forecast_compliance(reduction_strategy),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Demand response event {event_id}: Target {target_reduction}kW reduction across {len(affected_meters)} meters")
            return result
            
        except Exception as e:
            logger.error(f"Error managing demand response: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    # Helper methods for internal processing
    async def _detect_real_time_anomaly(self, reading: Dict, threshold: str) -> Optional[Dict]:
        """Detect anomalies in real-time meter reading"""
        meter_id = reading["meter_id"]
        
        if meter_id not in self.meter_data_cache or len(self.meter_data_cache[meter_id]) < 5:
            return None
        
        recent_readings = self.meter_data_cache[meter_id][-10:]  # Last 10 readings
        current_power = reading["power_kw"]
        historical_power = [r["power_kw"] for r in recent_readings]
        
        if len(historical_power) < 3:
            return None
        
        avg_power = statistics.mean(historical_power)
        std_power = statistics.stdev(historical_power) if len(historical_power) > 1 else 0
        
        # Consumption spike detection
        if std_power > 0 and current_power > avg_power + (self.anomaly_thresholds["consumption_spike"] * std_power):
            return {
                "type": "consumption_spike",
                "meter_id": meter_id,
                "severity": "high" if current_power > avg_power + (3 * std_power) else "medium",
                "current_value": current_power,
                "expected_range": f"{avg_power - std_power:.2f} - {avg_power + std_power:.2f}",
                "deviation": f"{((current_power - avg_power) / avg_power * 100):.1f}%",
                "timestamp": reading["timestamp"]
            }
        
        # Equipment overheating
        if "temperature" in reading and reading["temperature"] > self.anomaly_thresholds["equipment_temp"]:
            return {
                "type": "equipment_overheating",
                "meter_id": meter_id,
                "severity": "critical" if reading["temperature"] > 95 else "high",
                "current_value": reading["temperature"],
                "threshold": self.anomaly_thresholds["equipment_temp"],
                "timestamp": reading["timestamp"]
            }
        
        return None

    async def _generate_anomaly_alert(self, anomaly: Dict) -> Dict:
        """Generate alert from detected anomaly"""
        alert_type_map = {
            "consumption_spike": "consumption_anomaly",
            "consumption_drop": "consumption_anomaly",
            "equipment_overheating": "equipment_failure",
            "efficiency_drop": "efficiency_issue"
        }
        
        return {
            "alert_type": alert_type_map.get(anomaly["type"], "equipment_failure"),
            "meter_id": anomaly["meter_id"],
            "severity": anomaly["severity"],
            "description": f"Detected {anomaly['type']}: {anomaly.get('deviation', 'N/A')}",
            "auto_generated": True,
            "source_anomaly": anomaly
        }

    def _calculate_time_span(self, readings: List[Dict]) -> str:
        """Calculate time span of meter readings"""
        timestamps = [datetime.fromisoformat(r["timestamp"].replace('Z', '+00:00')) for r in readings]
        if not timestamps:
            return "0 minutes"
        
        time_span = max(timestamps) - min(timestamps)
        return f"{time_span.total_seconds() / 60:.1f} minutes"

    def _assess_data_quality(self, readings: List[Dict]) -> str:
        """Assess data quality of meter readings"""
        if not readings:
            return "no_data"
        
        # Check for missing values
        missing_count = sum(1 for r in readings if not all(k in r for k in ["meter_id", "energy_kwh", "power_kw"]))
        missing_rate = missing_count / len(readings)
        
        if missing_rate > 0.1:
            return "poor"
        elif missing_rate > 0.05:
            return "fair"
        else:
            return "good"

    async def _analyze_anomaly_type(self, data: List[Dict], anomaly_type: str, sensitivity: str) -> List[Dict]:
        """Analyze specific anomaly type"""
        anomalies = []
        
        if anomaly_type == "consumption_spike":
            power_values = [r["power_kw"] for r in data]
            if len(power_values) > 3:
                mean_power = statistics.mean(power_values)
                std_power = statistics.stdev(power_values)
                threshold_multiplier = {"low": 3.0, "medium": 2.5, "high": 2.0}[sensitivity]
                
                for reading in data:
                    if reading["power_kw"] > mean_power + (threshold_multiplier * std_power):
                        anomalies.append({
                            "type": "consumption_spike",
                            "severity": "high" if reading["power_kw"] > mean_power + (3 * std_power) else "medium",
                            "timestamp": reading["timestamp"],
                            "value": reading["power_kw"],
                            "expected": mean_power,
                            "deviation_percent": ((reading["power_kw"] - mean_power) / mean_power * 100)
                        })
        
        return anomalies

    def _calculate_data_quality_score(self, data: List[Dict]) -> float:
        """Calculate data quality score (0-100)"""
        if not data:
            return 0.0
        
        # Check completeness, consistency, and validity
        complete_readings = sum(1 for r in data if all(k in r and r[k] is not None for k in ["energy_kwh", "power_kw"]))
        completeness_score = (complete_readings / len(data)) * 100
        
        # Additional quality checks would go here
        return min(100.0, completeness_score)

    def _calculate_trend(self, data: List[Dict]) -> str:
        """Calculate consumption trend"""
        if len(data) < 2:
            return "insufficient_data"
        
        power_values = [r["power_kw"] for r in data]
        first_half = power_values[:len(power_values)//2]
        second_half = power_values[len(power_values)//2:]
        
        if not first_half or not second_half:
            return "insufficient_data"
        
        avg_first = statistics.mean(first_half)
        avg_second = statistics.mean(second_half)
        
        change_percent = ((avg_second - avg_first) / avg_first) * 100
        
        if change_percent > 10:
            return "increasing"
        elif change_percent < -10:
            return "decreasing"
        else:
            return "stable"

    def _get_default_action(self, alert_type: str) -> str:
        """Get default recommended action for alert type"""
        actions = {
            "equipment_failure": "Inspect equipment for hardware failure, check connections and sensors",
            "consumption_anomaly": "Investigate consumption patterns, check for unusual loads or equipment operation",
            "efficiency_issue": "Perform efficiency assessment, check equipment settings and operating conditions",
            "maintenance_required": "Schedule maintenance inspection, review equipment maintenance history",
            "emergency": "Immediate on-site response required, ensure safety protocols are followed"
        }
        return actions.get(alert_type, "Investigate and assess situation")

    def _get_meter_location(self, meter_id: str) -> Dict:
        """Get location information for meter (simulated)"""
        return {
            "building_id": f"BLDG_{meter_id[:3]}",
            "floor": "3",
            "room": f"Electrical Room {meter_id[-2:]}",
            "coordinates": "40.7128,-74.0060"  # NYC coordinates as example
        }

    def _calculate_response_time(self, severity: str, priority: int) -> str:
        """Calculate estimated response time"""
        base_times = {"low": 240, "medium": 120, "high": 60, "critical": 30}  # minutes
        base_time = base_times.get(severity, 120)
        adjusted_time = base_time - (priority * 5)  # Reduce by 5 min per priority point
        return f"{max(15, adjusted_time)} minutes"

    def _get_required_tools(self, alert_type: str) -> List[str]:
        """Get required tools for alert type"""
        tools = {
            "equipment_failure": ["multimeter", "thermal_camera", "hand_tools"],
            "consumption_anomaly": ["power_analyzer", "laptop", "measurement_tools"],
            "efficiency_issue": ["efficiency_meter", "diagnostic_tools"],
            "maintenance_required": ["maintenance_kit", "inspection_tools"],
            "emergency": ["safety_equipment", "emergency_kit"]
        }
        return tools.get(alert_type, ["basic_tools"])

    def _get_safety_considerations(self, alert_type: str) -> List[str]:
        """Get safety considerations for alert type"""
        safety = {
            "equipment_failure": ["High voltage present", "Use PPE", "Lock out tag out procedures"],
            "consumption_anomaly": ["Standard electrical safety", "Equipment may be energized"],
            "efficiency_issue": ["Standard safety protocols"],
            "maintenance_required": ["Follow maintenance safety procedures"],
            "emergency": ["IMMEDIATE SAFETY RISK", "Follow emergency protocols", "Consider evacuation"]
        }
        return safety.get(alert_type, ["Standard safety protocols"])

    def _assign_field_engineer(self, location_info: Dict, priority: int) -> str:
        """Assign field engineer (simulated)"""
        # In production, this would integrate with workforce management system
        engineers = ["Engineer_A", "Engineer_B", "Engineer_C"]
        return engineers[priority % len(engineers)]

    async def _collect_equipment_data(self, equipment_id: str, period_hours: int) -> Dict:
        """Collect equipment performance data (simulated)"""
        # Simulate realistic equipment data
        import random
        
        base_efficiency = random.uniform(0.85, 0.95)
        base_power_factor = random.uniform(0.85, 0.98)
        base_temperature = random.uniform(45, 75)
        
        return {
            "efficiency": [base_efficiency + random.uniform(-0.05, 0.05) for _ in range(period_hours)],
            "power_factor": [base_power_factor + random.uniform(-0.02, 0.02) for _ in range(period_hours)],
            "temperature": [base_temperature + random.uniform(-5, 10) for _ in range(period_hours)],
            "runtime_hours": period_hours
        }

    async def _analyze_performance_metric(self, metric: str, data: List[float], baseline_comparison: bool) -> Dict:
        """Analyze individual performance metric"""
        if not data:
            return {"status": "no_data", "metric": metric}
        
        current_avg = statistics.mean(data)
        current_std = statistics.stdev(data) if len(data) > 1 else 0
        
        # Baseline comparison (simulated)
        baseline_values = {
            "efficiency": 0.90,
            "power_factor": 0.95,
            "temperature": 60.0
        }
        
        baseline = baseline_values.get(metric, current_avg)
        deviation = ((current_avg - baseline) / baseline) * 100
        
        status = "optimal"
        if abs(deviation) > 15:
            status = "poor"
        elif abs(deviation) > 5:
            status = "degraded"
        
        return {
            "status": status,
            "metric": metric,
            "current_average": current_avg,
            "baseline": baseline,
            "deviation_percent": deviation,
            "variability": current_std,
            "trend": "stable",  # Simplified
            "recommendation": self._get_metric_recommendation(metric, status, deviation)
        }

    def _get_metric_recommendation(self, metric: str, status: str, deviation: float) -> str:
        """Get recommendation for metric performance"""
        if status == "optimal":
            return f"{metric.title()} is performing within optimal range"
        
        recommendations = {
            "efficiency": "Check equipment calibration and operating conditions",
            "power_factor": "Review reactive power compensation and load balance",
            "temperature": "Inspect cooling system and ventilation"
        }
        
        base_rec = recommendations.get(metric, "Review equipment settings")
        
        if deviation > 0:
            return f"{base_rec} - Values are higher than expected"
        else:
            return f"{base_rec} - Values are lower than expected"

    def _calculate_performance_score(self, analysis_results: Dict) -> float:
        """Calculate overall performance score"""
        scores = []
        
        for metric, analysis in analysis_results.items():
            if analysis.get("status") == "optimal":
                scores.append(100)
            elif analysis.get("status") == "degraded":
                scores.append(75)
            else:  # poor
                scores.append(50)
        
        return statistics.mean(scores) if scores else 0

    def _generate_performance_recommendations(self, analysis_results: Dict) -> List[str]:
        """Generate performance improvement recommendations"""
        recommendations = []
        
        for metric, analysis in analysis_results.items():
            if analysis.get("status") in ["degraded", "poor"]:
                recommendations.append(analysis.get("recommendation", f"Review {metric} performance"))
        
        return recommendations

    async def _analyze_pattern_type(self, scope: str, identifier: str, pattern_type: str, time_range: Dict) -> Dict:
        """Analyze specific usage pattern type (simulated)"""
        # Simulate pattern analysis results
        import random
        
        patterns = {
            "daily_profile": {
                "peak_hours": ["09:00", "14:00", "18:00"],
                "base_load": random.uniform(50, 100),
                "peak_load": random.uniform(150, 300),
                "variability": random.uniform(0.1, 0.3)
            },
            "weekly_profile": {
                "weekday_average": random.uniform(100, 200),
                "weekend_average": random.uniform(60, 120),
                "highest_day": "Tuesday",
                "lowest_day": "Sunday"
            },
            "peak_demand": {
                "max_demand_kw": random.uniform(200, 500),
                "demand_charges": random.uniform(1000, 5000),
                "coincident_peak": "15:30",
                "frequency": "Daily"
            }
        }
        
        return patterns.get(pattern_type, {"status": "not_implemented"})

    def _extract_usage_insights(self, patterns_analysis: Dict) -> List[str]:
        """Extract insights from usage pattern analysis"""
        insights = []
        
        if "daily_profile" in patterns_analysis:
            daily = patterns_analysis["daily_profile"]
            if daily.get("variability", 0) > 0.25:
                insights.append("High daily energy variability indicates potential optimization opportunities")
        
        if "weekly_profile" in patterns_analysis:
            weekly = patterns_analysis["weekly_profile"]
            weekday_avg = weekly.get("weekday_average", 0)
            weekend_avg = weekly.get("weekend_average", 0)
            if weekday_avg > weekend_avg * 2:
                insights.append("Significant weekday/weekend usage difference suggests schedule-based optimization potential")
        
        if "peak_demand" in patterns_analysis:
            insights.append("Peak demand analysis shows potential for demand response participation")
        
        return insights

    def _generate_usage_recommendations(self, patterns_analysis: Dict, insights: List[str]) -> List[Dict]:
        """Generate usage optimization recommendations"""
        recommendations = []
        
        if "daily_profile" in patterns_analysis:
            recommendations.append({
                "type": "load_scheduling",
                "priority": "medium",
                "description": "Implement load scheduling to flatten daily demand curve",
                "estimated_savings": "10-15%",
                "implementation": "Schedule non-critical loads during off-peak hours"
            })
        
        if "peak_demand" in patterns_analysis:
            recommendations.append({
                "type": "demand_response",
                "priority": "high",
                "description": "Participate in demand response programs",
                "estimated_savings": "15-25%",
                "implementation": "Install demand response automation system"
            })
        
        return recommendations

    def _calculate_savings_potential(self, patterns_analysis: Dict) -> Dict:
        """Calculate potential energy and cost savings"""
        # Simplified savings calculation
        return {
            "energy_savings_percent": "10-20%",
            "cost_savings_annual": "$15,000-30,000",
            "payback_period": "2-4 years",
            "confidence": "medium"
        }

    def _calculate_efficiency_score(self, patterns_analysis: Dict) -> float:
        """Calculate overall efficiency score"""
        # Simplified efficiency scoring
        import random
        return random.uniform(70, 95)

    async def _calculate_reduction_strategy(self, target_reduction: float, affected_meters: List[str], priority_loads: List[str]) -> Dict:
        """Calculate optimal load reduction strategy"""
        # Simulate load reduction calculation
        available_reduction = len(affected_meters) * 25  # 25kW avg per meter
        achievable_reduction = min(target_reduction, available_reduction)
        
        return {
            "target_reduction": target_reduction,
            "estimated_reduction": achievable_reduction,
            "success_probability": min(100, (achievable_reduction / target_reduction) * 100),
            "participating_meters": len(affected_meters),
            "protected_loads": len(priority_loads),
            "reduction_per_meter": achievable_reduction / len(affected_meters) if affected_meters else 0,
            "implementation_strategy": "Gradual reduction over 15 minutes to minimize impact"
        }

    async def _execute_demand_response(self, strategy: Dict) -> Dict:
        """Execute demand response (simulated)"""
        return {
            "status": "executed",
            "actual_reduction": strategy["estimated_reduction"] * 0.95,  # 95% success rate
            "execution_time": "2024-01-15T15:30:00Z",
            "participants": strategy["participating_meters"]
        }

    def _forecast_compliance(self, strategy: Dict) -> Dict:
        """Forecast demand response compliance"""
        return {
            "expected_compliance_rate": f"{strategy['success_probability']:.0f}%",
            "risk_factors": ["Equipment availability", "Weather conditions"],
            "confidence_level": "high" if strategy["success_probability"] > 80 else "medium"
        }

async def main():
    """Run the Energy Monitoring Agent"""
    agent = EnergyMonitoringAgent()
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())