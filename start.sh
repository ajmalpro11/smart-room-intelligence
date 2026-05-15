#!/bin/bash
# Smart Room Intelligence — Full System Startup Script

echo "🏠 Starting Smart Room Intelligence System..."

# Navigate to project
cd /home/ajmalpro11/smart-room

# Activate virtual environment
source venv/bin/activate

# Set GPIO backend
export GPIOZERO_PIN_FACTORY=lgpio

# Start Docker stack
echo "Starting Docker containers..."
docker compose up -d
sleep 10
echo "✅ Docker containers running"

# Start MQTT subscriber in background
echo "Starting MQTT subscriber..."
python3 mqtt/subscriber.py &
SUBSCRIBER_PID=$!
sleep 2
echo "✅ MQTT subscriber running (PID: $SUBSCRIBER_PID)"

# Start MQTT publisher in background
echo "Starting MQTT publisher..."
python3 mqtt/publisher.py &
PUBLISHER_PID=$!
sleep 5
echo "✅ MQTT publisher running (PID: $PUBLISHER_PID)"

# Start Flask dashboard
echo "Starting Flask dashboard..."
echo ""
echo "========================================"
echo "✅ System fully started!"
echo "🌐 Dashboard: http://192.168.1.101:5000"
echo "📊 Grafana:   http://192.168.1.101:3000"
echo "========================================"
echo ""
python3 dashboard/app.py
