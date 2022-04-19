# Second Lab: Hazelcast Basics


## Prerequisites

If you want to work with this project you should firstly write in the command prompt:


```
https://github.com/khristinakokolus/microservices_architecture.git
```

To install requirements:

```
cd hazelcast
pip install -r requirements.txt
```

In addition to this, you need to create cluster and connect to management center.
To make this go here: [Hazelcast Getting started](https://hazelcast.org/imdg/get-started/)

Cluster config file is ```hazelcast.yaml```

## Usage

Run example with distributed map:

```
python3 distributed_map.py
```

Run example with distributed map with locks:

```
python3 distributed_map_with_locks.py
```


Run example with bounded queue:

```
python3 bounded_queue_producer_consumer.py
```

## Results

Results are in Lab2_protocol_Kokolus.pdf