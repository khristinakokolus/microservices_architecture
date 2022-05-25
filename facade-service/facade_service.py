from flask import request
import logging
import requests
import hazelcast
import random
import uuid
import json


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

logging_services = ["http://localhost:8083/logging_service",
                    "http://localhost:8084/logging_service",
                    "http://localhost:8085/logging_service"]
message_services = ["http://localhost:8081/message_service",
                    "http://localhost:8082/message_service"]

hz_client = hazelcast.HazelcastClient()
distributed_queue = hz_client.get_queue("messages_queue_distributed").blocking()


def random_url(urls):
    url = random.choice(urls)
    return url


def get_data():
    try:
        logging_service = random.choice(logging_services)
        message_service = random.choice(message_services)
        logging.info("Logging service on: " + logging_service)
        logging.info("Message service on: " + message_service)

        logging_service_data = requests.get(logging_service).text
        message_service_data = requests.get(message_service).text
        data = "Logging service messages: " + logging_service_data + "\n" +\
               "Messages service messages: " + message_service_data + "\n"
        return data
    except requests.exceptions.ConnectionError:
        return "Error occurred"


def post_messages_logging(logging_service, data):
    response = requests.post(url=logging_service, data=json.dumps(data),
                             headers={"Content-Type": "application/json"})
    return response


def post_messages_msg_queue(message):
    try:
        distributed_queue.put(message)
        return 200
    except Exception as err:
        logging.error(f'Producer error: {err}')
        return 404


def post_message():
    message = request.json.get("msg", None)
    message_uuid = str(uuid.uuid4())

    data = {
        "message": message,
        "message_uuid": message_uuid
    }

    logging_service = random_url(logging_services)

    response_logging = post_messages_logging(logging_service, data)
    response_msg_queue = post_messages_msg_queue(data)

    return {
        "statusCode": [response_logging.status_code, response_msg_queue]
    }

