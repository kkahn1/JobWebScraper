# Base image
FROM python:3.11-slim

# Environment Variables
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV DEBIAN_FRONTEND=noninteractive

# System Packages
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxkbcommon0 \
    libgbm1 \
    libpango-1.0-0 \
    libasound2 \
    libwayland-client0 \
    libwayland-cursor0 \
    libwayland-egl1 \
    libxshmfence1 \
    libnss3 \
    libdrm2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Playwright
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps

# Copy the script to Docker Container
COPY . /app

# Set the working directory
WORKDIR /app

# Run the scraper
CMD ["python", "main.py"]
