# Third lab: Microservices using Hazelcast Distributed Map


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

NOTE: First need to start set up Hazelcast client locally

Go here [Getting started with Hazelcast](https://hazelcast.org/imdg/get-started/)

Running facade service:

```
cd facade-service
python3 facade_controller.py
```
Here default port is 8080.


Running logging service: 

```
cd logging-service
python3 logging_controller.py --port {port on which to run}
```
Here you can run three instances using 8082, 8083, 8084 ports.


Running messages service:

```
cd messages-service
python3 messages_service.py
```

Here default port is 8081.


Requests can be sent using ```requests.http``` or using some other tool such Postman.

## Results

Results are in Lab3_protocol_Kokolus.pdf
