# 4 lab: Microservices using the Messaging queue


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
Here you can run three instances using 8083, 8084, 8085 ports.


Running messages service:

```
cd messages-service
python3 messages_service.py --port {port on which to run}
```

Here you can run two instances using 8081, 8082 ports.


Requests can be sent using ```requests.http``` or using some other tool such Postman.

## Results

Results are in Lab4_protocol_Kokolus.pdf