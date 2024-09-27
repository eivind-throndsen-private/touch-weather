FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        librsvg2-bin \
        wget \
        python3 \
        python3-pip

# Install Python dependencies
RUN pip install --no-cache-dir \
    pillow \
    pyyaml \
    wget

# Copy the application files
COPY run.sh meteogram.py svg_color_transform.py color_transform_config.yaml config.json /app/
WORKDIR /app

# Make run.sh executable
RUN chmod +x run.sh

# Set the entrypoint
CMD ["./run.sh"]
