import argparse
from flask import Flask, request
import logging

from messages_service import producer, consumer

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)


@app.route('/message_service', methods=['GET'])
def get():
    messages = consumer()
    return "[" + ", ".join(messages) + "]"


@app.route('/message_service', methods=['POST'])
def post():
    message_data = request.get_json()
    logging.info(message_data)
    return producer(message_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process port number')
    parser.add_argument('--port', type=int)
    args = parser.parse_args()
    app.run(port=args.port)
