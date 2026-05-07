# Use Ubuntu 22.04 as base (best for GIS compatibility)
FROM ubuntu:22.04

# Avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install System Dependencies & QGIS
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    software-properties-common \
    wget \
    gnupg \
    ca-certificates \
    && mkdir -m 755 -p /etc/apt/keyrings \
    && wget -O /etc/apt/keyrings/qgis-archive-keyring.gpg https://download.qgis.org/downloads/qgis-archive-keyring.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/qgis-archive-keyring.gpg] https://qgis.org/ubuntu jammy main" | tee /etc/apt/sources.list.d/qgis.list \
    && apt-get update && apt-get install -y \
    qgis \
    python3-qgis \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set PYTHONPATH and Headless mode for QGIS
ENV PYTHONPATH=/app
ENV QT_QPA_PLATFORM=offscreen

# Expose the port Hugging Face expects
EXPOSE 7860

# Start the server on port 7860
CMD ["uvicorn", "geosi_server.app.main:app", "--host", "0.0.0.0", "--port", "7860"]
