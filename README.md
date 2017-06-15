# ZeroMQ Broker

A docker container image to run a simple broker based on ZeroMQ.

## Build it

docker build -t <image name> .

## Run it

docker run -d --name broker -p 15554:15554 -p 15555:15555 <image name>
