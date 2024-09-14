# Touch Weather Meteogram

This is a hobbyist project to display the upcoming weather forecast on a Logitech Squeezebox Touch. The script periodically downloads a meteogram SVG from [yr.no](https://www.yr.no/) and processes it into a PNG image suitable for display on the Squeezebox Touch. It should be possible to adapt this approach to generate weather forecast excerpts files for display on screen savers, boards etc. Please be gentle on the yr.no servers, it is a great publicly funded resource with no ad funding. This script fetches the SVG once every hour at night and once every 15 minutes during the day.

## Features

- Downloads weather forecast SVG for your location.
- Converts the SVG to PNG and crops it to display the next 24 hours.
- Outputs a 480 x 272 PNG image optimized for the Squeezebox Touch screen.
- Runs inside a Docker container for easy deployment.
- Configurable parameters via a `config.json` file.

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

- `svg_url`: The URL to the meteogram SVG from yr.no. You can usually find the SVG link on the regular weather forecast page on yr.no. 
- `image_height`: Height of the image during conversion.
- `crop_area`: The area of the image to crop `[x, y, width, height]`. Relative to image_height. 

### Running the Container

To run the container:

```bash
make run
```

This command mounts the `output` directory so you can access the generated image on your host machine.

