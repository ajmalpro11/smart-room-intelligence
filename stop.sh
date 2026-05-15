#!/bin/bash
echo "Stopping Smart Room Intelligence System..."
cd /home/ajmalpro11/smart-room
docker compose down
pkill -f "mqtt/publisher.py"
pkill -f "mqtt/subscriber.py"
pkill -f "dashboard/app.py"
echo "✅ System stopped"
