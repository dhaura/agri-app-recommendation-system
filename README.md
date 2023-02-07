# agri-app-recommendation-system

Use below command to build docker image for the base (wheels for pytorch and torchvision) compatible with RPI
```
docker build --platform=linux/arm/v7 -t dhaura/agri-app-rs-base:latest -f Dockerfile1 .
```

Push to the DockerHub repo
```
docker push dhaura/agri-app-rs-base:latest
```

Use below command to build docker image for RS compatible with RPI
```
docker build --platform=linux/arm/v7 -t dhaura/agri-app-rs:latest -f Dockerfile .
```

Push to the DockerHub repo
```
docker push dhaura/agri-app-rs:latest
```
