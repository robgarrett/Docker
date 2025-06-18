# Base image
FROM debian:bullseye

RUN apt-get update && apt-get install -qqy curl nginx tor && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install tini for proper signal handling
RUN apt-get update && apt-get install -qqy tini

# Configure Tor and Nginx to run in the foreground using a shell with tini as the entrypoint
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/bin/sh", "-c", "tor & nginx -g 'daemon off;'"]