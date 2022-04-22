from flask import request
import requests
import random
import uuid
import json

logging_services = ["http://localhost:8082/logging_service",
                    "http://localhost:8083/logging_service",
                    "http://localhost:8084/logging_service"]
message_service = "http://localhost:8081/message_service"


def get_data():
    logging_service = random.choice(logging_services)
    logging_service_data = requests.get(logging_service).text
    message_service_data = requests.get(message_service).text
    data = logging_service_data + ": " + message_service_data
    return data


def post_message():
    message = request.get_json()
    message_uuid = str(uuid.uuid4())

    data = {
        "message": message,
        "message_uuid": message_uuid
    }

    logging_service = random.choice(logging_services)

    response = requests.post(url=logging_service, data=json.dumps(data),
                             headers={"Content-Type": "application/json"})

    return {
        "statusCode": response.status_code
    }

