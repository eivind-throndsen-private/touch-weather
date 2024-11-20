# Touch Weather Meteogram

This is a hobbyist project to display the upcoming weather forecast on a Logitech Squeezebox Touch. The meteogram.py script periodically downloads a meteogram (a infographic that shows the weather forecast) from the website of the Norwegian Weather Service at [yr.no](https://www.yr.no/) and processes it into a PNG image suitable for display on the Squeezebox Touch. 

It should be possible to adapt this approach to generate weather forecast excerpts files for display on screen savers, boards etc. 

## Features

- Downloads weather forecast SVG for your location (location for the SVG URL is configurable).
- Converts the SVG to PNG and crops it to display the next 24 hours.
- Outputs a 480 x 272 PNG image optimized for the Squeezebox Touch screen.
- Runs inside a Docker container for easy deployment.
- Configurable via the `config.json` file.

## Getting Started

### Prerequisites

- Docker installed on your system.
- Optionally, `git` for cloning the repository.
- I am running this inside Container Manager on a Synology NAS. Not tested anywhere else. YMMV.

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

- `svg_url`: The URL to the meteogram SVG from yr.no. You can find the SVG link on the regular weather forecast page on [yr.no](https://www.yr.no/).
- `image_height`: Height of the image during conversion.
- `crop_area`: The area of the image to crop `[x, y, width, height]`. Relative to image_height. 

### Running the Container

To run the container locally:

```bash
make run
```

This command mounts the `output` directory so you can access the generated image on your host machine.

To run the container on your Synology NAS you will need to generate the Docker image, upload it to the Synology Container Manager, and configure a container using the image. The generated meteogram images can then be loaded by the screensaver on your Squeezebox Touch.  


