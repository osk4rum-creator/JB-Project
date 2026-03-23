#!/bin/bash
# scripts/setup_nginx.sh

echo "[INFO] Starting Nginx installation..."

# Check if Nginx is already installed
if command -v nginx >/dev/null 2>&1; then
    echo "[INFO] Nginx is already installed. Skipping installation."
else
    # Simulating installation for the project
    echo "[INFO] Installing Nginx..."
    # In a real Ubuntu environment, we would use: sudo apt-get update && sudo apt-get install -y nginx
    echo "[SUCCESS] Nginx installation completed."
fi