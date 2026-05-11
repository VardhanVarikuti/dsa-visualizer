# Use Python 3.11 slim as base
FROM python:3.11-slim

# Prevent interactive prompts during apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for X11, VNC, and Pygame
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    fluxbox \
    xterm \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    procps \
    libxft2 \
    libxmu6 \
    fonts-liberation \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set display environment variable
ENV DISPLAY=:99

# Make start script executable
RUN chmod +x scripts/start.sh

# Expose noVNC port
EXPOSE 6080

# Start everything via script
CMD ["./scripts/start.sh"]