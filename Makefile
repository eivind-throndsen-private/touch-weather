# Define variables for docker image name and tag
IMAGE_NAME=touch-weather
TAG=latest
TAR_NAME=touch-weather.tar

# Default target
all: build

# Build the Docker image
build:
	docker build --platform linux/amd64 -t $(IMAGE_NAME):$(TAG) .

# Run the container
run: clean
	docker run --name $(IMAGE_NAME) -it -v $(PWD)/output:/app/output $(IMAGE_NAME):$(TAG)

# Save the docker image to a tar file
save: build $(TAR_NAME)

$(TAR_NAME): build
	docker save $(IMAGE_NAME):$(TAG) > $(TAR_NAME)

# Load the docker image from a tar file
load:
	docker load < $(TAR_NAME)

# Push the docker image to a registry
push:
	docker push $(IMAGE_NAME):$(TAG)

# Clean up dangling images
clean:
	-docker rm -f touch-weather || true
	docker image prune -f
	$(MAKE) clean-tar

# Remove the generated tar file
clean-tar:
	rm -f $(TAR_NAME)
