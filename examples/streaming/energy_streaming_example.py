#!/usr/bin/env python3
"""
Energy Streaming Example
========================

Demonstrates IoT stream processing for energy meter data.
Shows how to process 12k+ energy meters with 48k+ data points per hour.
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from redaptive.streaming import EnergyStreamManager, StreamBackend
from redaptive.streaming.data_models import MeterReading, MeterType, MessageType


async def simulate_meter_data_producer(stream_manager: EnergyStreamManager, 
                                     num_meters: int = 100, 
                                     duration_seconds: int = 60):
    """
    Simulate energy meter data production.
    
    Args:
        stream_manager: The stream manager instance
        num_meters: Number of meters to simulate
        duration_seconds: How long to run the simulation
    """
    print(f"🏭 Starting meter data simulation for {num_meters} meters over {duration_seconds} seconds...")
    
    # Generate meter configurations
    meters = []
    for i in range(num_meters):
        meter = {
            "meter_id": f"meter_{i:04d}",
            "building_id": f"building_{i // 10:03d}",  # 10 meters per building
            "meter_type": random.choice(list(MeterType)),
            "baseline_consumption": random.uniform(50, 500),
            "location": f"Floor {(i % 5) + 1}"
        }
        meters.append(meter)
    
    start_time = datetime.now()
    message_count = 0
    
    # Production loop
    while (datetime.now() - start_time).total_seconds() < duration_seconds:
        # Generate readings for all meters
        for meter in meters:
            # Generate realistic meter reading
            base_value = meter["baseline_consumption"]
            # Add some variance (±20%)
            variance = random.uniform(-0.2, 0.2)
            # Add time-of-day effect
            hour = datetime.now().hour
            time_factor = 1.0 + (0.3 * (hour - 12) / 12)  # Peak during day
            
            value = base_value * (1 + variance) * time_factor
            
            # Create meter reading
            reading = MeterReading(
                meter_id=meter["meter_id"],
                building_id=meter["building_id"],
                meter_type=meter["meter_type"],
                timestamp=datetime.now(),
                value=max(0, value),  # Ensure positive values
                unit="kWh" if meter["meter_type"] == MeterType.ELECTRICITY else "BTU",
                quality_score=random.uniform(0.95, 1.0),
                metadata={
                    "location": meter["location"],
                    "baseline": meter["baseline_consumption"]
                }
            )
            
            # Publish reading
            success = await stream_manager.publish_meter_reading(reading)
            if success:
                message_count += 1
            
            # Small delay to prevent overwhelming
            await asyncio.sleep(0.01)
        
        # Brief pause between rounds
        await asyncio.sleep(1)
    
    print(f"📊 Simulation complete: {message_count} messages produced")


async def simulate_anomaly_detection(stream_manager: EnergyStreamManager):
    """Simulate anomaly detection and alerting."""
    print("🚨 Starting anomaly detection simulation...")
    
    # Simulate finding anomalies periodically
    for i in range(5):
        await asyncio.sleep(10)  # Wait 10 seconds between anomalies
        
        # Generate anomaly
        anomaly_data = {
            "type": "consumption_spike",
            "meter_id": f"meter_{random.randint(0, 99):04d}",
            "building_id": f"building_{random.randint(0, 9):03d}",
            "severity": random.choice(["low", "medium", "high"]),
            "description": f"Consumption spike detected at {datetime.now().strftime('%H:%M:%S')}",
            "threshold_exceeded": random.uniform(1.5, 3.0),
            "recommended_action": "Investigate equipment status"
        }
        
        # Publish anomaly
        success = await stream_manager.publish_anomaly(anomaly_data)
        if success:
            print(f"🔍 Anomaly detected: {anomaly_data['description']}")
        
        # Generate alert if high severity
        if anomaly_data["severity"] == "high":
            alert_data = {
                "type": "critical_anomaly",
                "meter_id": anomaly_data["meter_id"],
                "building_id": anomaly_data["building_id"],
                "message": f"Critical anomaly in {anomaly_data['meter_id']}",
                "priority": "high",
                "created_at": datetime.now().isoformat()
            }
            
            await stream_manager.publish_alert(alert_data)
            print(f"🚨 High priority alert sent for {anomaly_data['meter_id']}")


async def demonstrate_streaming_processing():
    """Main demonstration of streaming processing."""
    print("🔋 Redaptive Energy Streaming Demo")
    print("=" * 50)
    
    # Initialize stream manager
    # Try Redis first, fallback to in-memory simulation
    try:
        stream_manager = EnergyStreamManager(StreamBackend.AUTO)
        print(f"📡 Initialized stream manager with {stream_manager.backend.value} backend")
    except Exception as e:
        print(f"⚠️  Streaming backend not available: {e}")
        print("💡 To enable streaming, install dependencies:")
        print("   pip install redis aiokafka")
        print("   Or run: pip install -e .[streaming]")
        return
    
    try:
        # Start stream manager
        success = await stream_manager.start()
        if not success:
            print("❌ Failed to start stream manager")
            return
        
        # Setup energy streams
        print("🏗️  Setting up energy streams...")
        success = await stream_manager.setup_energy_streams()
        if not success:
            print("❌ Failed to setup energy streams")
            return
        
        # Start consumers
        print("👥 Starting stream consumers...")
        success = await stream_manager.start_energy_consumers()
        if not success:
            print("❌ Failed to start consumers")
            return
        
        print("✅ Stream processing infrastructure ready!")
        print()
        
        # Start data production and anomaly detection
        print("🚀 Starting data production and processing...")
        
        # Run producer and anomaly detector concurrently
        await asyncio.gather(
            simulate_meter_data_producer(stream_manager, num_meters=50, duration_seconds=30),
            simulate_anomaly_detection(stream_manager)
        )
        
        # Wait a bit for processing to complete
        await asyncio.sleep(5)
        
        # Show metrics
        print("\n📊 Final Metrics:")
        print("-" * 30)
        metrics = stream_manager.get_metrics()
        for key, value in metrics.items():
            print(f"{key}: {value}")
        
        # Health check
        health = await stream_manager.health_check()
        print(f"\n🏥 Health Status: {health['stream_manager']['status']}")
        
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        await stream_manager.stop()
        print("✅ Stream manager stopped")


async def demonstrate_high_throughput_simulation():
    """Demonstrate high throughput simulation (12k+ meters)."""
    print("\n🚀 High Throughput Simulation (12k+ meters)")
    print("=" * 50)
    
    # Calculate target throughput
    target_meters = 12000
    target_points_per_hour = 48000
    readings_per_meter_per_hour = target_points_per_hour / target_meters
    
    print(f"Target: {target_meters} meters")
    print(f"Target: {target_points_per_hour} data points/hour")
    print(f"Rate: {readings_per_meter_per_hour:.2f} readings/meter/hour")
    print(f"Rate: {target_points_per_hour / 3600:.2f} readings/second")
    
    # This would be the actual implementation for production
    print("\n💡 Production Implementation Notes:")
    print("- Deploy multiple stream processors for horizontal scaling")
    print("- Use Kafka partitioning for meter data distribution")
    print("- Implement consumer groups for parallel processing")
    print("- Add monitoring and alerting for stream health")
    print("- Use Redis for low-latency alerting")
    print("- Implement circuit breakers for fault tolerance")


async def main():
    """Run the streaming demonstration."""
    try:
        await demonstrate_streaming_processing()
        await demonstrate_high_throughput_simulation()
        
        print("\n🎉 Streaming demo completed successfully!")
        print("\nNext steps:")
        print("1. Install Redis: brew install redis (macOS) or apt-get install redis (Linux)")
        print("2. Install Kafka: brew install kafka (macOS)")
        print("3. Run: pip install -e .[streaming] to install streaming dependencies")
        print("4. Start Redis: redis-server")
        print("5. Start Kafka: kafka-server-start /usr/local/etc/kafka/server.properties")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())