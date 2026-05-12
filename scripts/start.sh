#!/bin/bash
set -e

# 1. Start Xvfb (Virtual Frame Buffer) on display :99
echo "Starting Xvfb on :99..."
Xvfb :99 -screen 0 1280x800x24 &
sleep 2

# 2. Start Fluxbox (Window Manager)
echo "Starting Fluxbox..."
fluxbox &
sleep 2

# 3. Start x11vnc to share display :99
echo "Starting x11vnc..."
x11vnc -display :99 -forever -shared -nopw -listen localhost -xkb &
sleep 2

# 4. Start noVNC proxy
echo "Starting noVNC proxy on port 6080..."
websockify --web /usr/share/novnc 6080 localhost:5900 &
sleep 2

# 5. Set environment for headless Pygame
export DISPLAY=:99
export SDL_AUDIODRIVER=dummy
export SDL_VIDEODRIVER=x11

# 6. Run the Pygame application inside xterm (restart on crash)
echo "Starting Pygame Visualizer in xterm..."
# Remove 2>/dev/null to see errors in docker logs
while true; do
    echo "Launching application..."
    # Removed -hold so xterm closes on app exit, triggering the loop to restart it
    xterm -fa 'Monospace' -fs 12 -geometry 100x30+10+10 -e "python main.py"
    echo "Application exited. Restarting in 2 seconds..."
    sleep 2
done
