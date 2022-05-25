## Prerequisites

If you want to work with this project you should firstly write in the command prompt:


```
https://github.com/khristinakokolus/microservices_architecture.git
```

To install requirements:

```
pip install -r requirements.txt
```

## Usage

NOTE: First need to start set up Hazelcast cluster locally

Go here [Getting started with Hazelcast](https://hazelcast.org/imdg/get-started/)

To set up Consul locally:

```
consul agent -dev
```

NOTE: to see all registered services go to http://localhost:8500


Add needed Key/Values:

```
bash consul_config.sh
```

Run facade service:

```
cd facade-service
python3 facade_controller --port {port on which to run}
```

Run logging service: 

```
cd logging-service
python3 logging_controller.py --port {port on which to run}
```

Run messages service:

```
cd messages-service
python3 messages_controller.py --port {port on which to run}
```

NOTE: you can shutdown service using such command (redirect to```{service_name}_service_shutdown```):

```
curl -X POST {URL}

curl -X POST http://127.0.0.1:8080/facade_service_shutdown (example)
```

Requests can be sent using ```requests.http``` or using some other tool such Postman.

## Results

Results are in Lab5_protocol_Kokolus.pdf