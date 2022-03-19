from flask import Flask, request
import requests
import uuid
import json

app = Flask(__name__)
logging_service = "http://localhost:8081/logging_service"
message_service = "http://localhost:8082/message_service"


@app.route('/facade_service', methods=['GET'])
def get_data():
    logging_service_data = requests.get(logging_service).text
    message_service_data = requests.get(message_service).text
    data = logging_service_data + ": " + message_service_data
    return data


@app.route('/facade_service', methods=['POST'])
def post_message():
    message = request.get_json()
    message_uuid = str(uuid.uuid4())

    data = {
        "message": message,
        "message_uuid": message_uuid
    }

    response = requests.post(url=logging_service, data=json.dumps(data),
                             headers={"Content-Type": "application/json"})

    return {
        "statusCode": response.status_code
    }


if __name__ == '__main__':
    app.run(port=8080)
