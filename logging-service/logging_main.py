from flask import Flask, request
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
messages = dict()


@app.route('/logging_service', methods=['GET'])
def get_data():
    return str(list(messages.values())[::-1])


@app.route('/logging_service', methods=['POST'])
def post_message():
    message_data = request.get_json()
    logging.info(message_data)
    messages[message_data["message_uuid"]] = message_data["message"]

    return {
        "statusCode": 200
    }


if __name__ == '__main__':
    app.run(port=8081)
