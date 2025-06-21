# Use Alpine-based Node.js image
FROM node:alpine

# Set working directory
VOLUME /app/src
WORKDIR /app/src

# Install dependencies
RUN apk update && apk add --no-cache \
    bash \
    make \
    py3-pip \
    gcc \
    libffi-dev \
    musl-dev \
    openssl-dev \
    python3-dev \
    curl \
    git

RUN pip install --break-system-packages --upgrade pip setuptools
RUN pip install --break-system-packages azure-cli

# Install Azure Functions Core Tools
RUN npm install -g azure-functions-core-tools@latest --unsafe-perm

ENTRYPOINT [ "/bin/bash" ]
