# Use Alpine-based Python image with a specific version for better reproducibility
FROM python:3.10-alpine3.18

# Set timezone
ENV TZ=Europe/Amsterdam
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apk del tzdata

# install fonts
RUN apk add --no-cache \
    fontconfig \
    ttf-dejavu \
    && apk add --no-cache librsvg

# Create the fonts directory if it doesn't exist
RUN mkdir -p /usr/share/fonts/TTF

# Copy your custom font files into the image
COPY NRKSans_Variable.ttf /usr/share/fonts/TTF/
COPY NRKSans_Variable_Italic.ttf /usr/share/fonts/TTF/

# Refresh the font cache
RUN fc-cache -f -v

# Install system dependencies and Python packages
RUN apk add --no-cache bash rsvg-convert jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev librsvg optipng && \
    apk add --no-cache --virtual .build-deps build-base && \
    pip install --no-cache-dir Pillow==9.5.0 pyyaml wget imagequant && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/* /root/.cache

# Set working directory
WORKDIR /app

# Copy configuration files first
COPY config.json color_transform_config.yaml /app/

# Copy fonts
COPY NRKSans_Variable.ttf NRKSans_Variable_Italic.ttf /app/

# Copy script files last (these change most often)
COPY run.sh svg_color_transform.py /app/
COPY meteogram.py /app/

# Make run.sh executable
RUN chmod +x /app/run.sh

# Set the entrypoint to run.sh
CMD ["./run.sh"]
