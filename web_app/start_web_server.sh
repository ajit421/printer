#!/usr/bin/env bash
# Start GlassyPrint Hub on Raspberry Pi 4
cd "$(dirname "$0")"
echo "Starting GlassyPrint Hub on port 5000..."
python3 app.py
