# ZeroMQ Broker

A docker container image to run a simple message broker based on ZeroMQ.

## Fetch the image

```
docker pull joshuakwan/zmq-broker
```

## Run it

```
docker run -d --name broker -p 15554:15554 -p 15555:15555 joshuakwan/zmq-broker
```

## Run with k8s

Please refer to the YAML files in `k8s-deployment` to launch the broker on k8s.