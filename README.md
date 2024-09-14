# Touch Weather Meteogram

This is a hobbyist project to display the upcoming weather forecast on a Logitech Squeezebox Touch. The script periodically downloads a meteogram SVG from [yr.no](https://www.yr.no/) and processes it into a PNG image suitable for display on the device.

## Features

- Downloads weather forecast SVG for your location.
- Converts the SVG to PNG and crops it to display the next 24 hours.
- Outputs a 480 x 272 PNG image optimized for the Squeezebox Touch screen.
- Runs inside a Docker container for easy deployment.
- Configurable parameters via a `config.json` file.
- Debug mode to assist with cropping adjustments.

## Getting Started

### Prerequisites

- Docker installed on your system.
- Optionally, `git` for cloning the repository.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/eivind-throndsen-private/touch-weather.git
   cd touch-weather
   ```

2. **Build the Docker Image**

   Use the provided `Makefile`:

   ```bash
   make build
   ```

### Configuration

Edit the `config.json` file to customize:

- `svg_url`: The URL to the meteogram SVG from yr.no.
- `image_height`: Height of the image during conversion.
- `crop_area`: The area of the image to crop `[x, y, width, height]`.

### Running the Container

To run the container:

```bash
make run
```

This command mounts the `output` directory so you can access the generated image on your host machine.

### Debug Mode

To run the script in debug mode and draw a red rectangle on the image, pass four parameters representing the rectangle's position and size:

```bash
./run.sh 50 50 100 100
```

- `50 50`: Starting x and y coordinates from the lower-left corner.
- `100 100`: Width and height of the rectangle.

