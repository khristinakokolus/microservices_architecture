from flask import request
import logging
import requests
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


def random_url(urls):
    url = random.choice(urls)
    return url


def get_data():
    try:
        logging_service = random.choice(logging_services)
        message_service = random.choice(message_services)
        logging.info("Logging service: " + logging_service)
        logging.info("Message service: " + message_service)

        logging_service_data = requests.get(logging_service).text
        message_service_data = requests.get(message_service).text
        data = "Logging service messages: " + logging_service_data + "\n" +\
               "Messages service messages: " + message_service_data
        return data
    except requests.exceptions.ConnectionError:
        return "Error occurred"


def post_message():
    message = request.get_json()
    message_uuid = str(uuid.uuid4())

    data = {
        "message": message,
        "message_uuid": message_uuid
    }

    logging_service = random_url(logging_services)
    messages_service = random_url(message_services)

    response_logging = requests.post(url=logging_service, data=json.dumps(data),
                                     headers={"Content-Type": "application/json"})
    response_messages = requests.post(url=messages_service, data=json.dumps(data),
                                      headers={"Content-Type": "application/json"})

    return {
        "statusCode": [response_logging.status_code, response_messages.status_code]
    }

