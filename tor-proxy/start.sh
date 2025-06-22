#!/bin/sh

echo "Starting Tor..."
tor -f /etc/tor/torrc &
sleep 15
echo "Tor is ready."

echo "Starting Socat..."
socat -d -d TCP-LISTEN:8080,fork,reuseaddr SOCKS4A:localhost:${ONION_ADDRESS}:80,socksport=9050 &
sleep 5
echo "Socat is ready."

echo "Starting Caddy..."
exec caddy run --config /etc/caddy/Caddyfile --adapter caddyfile
