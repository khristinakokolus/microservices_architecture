import sys
sys.path.append(r"c:\users\user\appdata\local\schrodinger\pymol2\lib\site-packages")
from flask import Flask, request
import logging

from logging_service import get_data, post_message

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)


@app.route('/logging_service', methods=['GET'])
def get():
    messages = get_data()
    print(type(messages))
    return "[" + ", ".join(list(messages.values())) + "]"


@app.route('/logging_service', methods=['POST'])
def post():
    message_data = request.get_json()
    logging.info(message_data)
    return post_message(message_data)


if __name__ == '__main__':
    #app.run(port=int(sys.argv[1]))
    app.run(port=8082)
