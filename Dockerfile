# Use a lightweight Python image
FROM python:3.9-slim

# Install required packages
RUN apt-get update && \
    apt-get install -y wget librsvg2-bin imagemagick && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
RUN pip install pillow wget

# Copy the necessary files into the container
COPY meteogram.py .
COPY run.sh .
COPY config.json .

# Make scripts executable
RUN chmod +x run.sh meteogram.py

# Create output directory
RUN mkdir -p /app/output

# Expose the output directory as a volume
VOLUME ["/app/output"]

# Run the script when the container launches
CMD ["./run.sh"]
