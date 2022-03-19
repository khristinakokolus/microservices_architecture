from flask import Flask, request


app = Flask(__name__)


@app.route('/message_service', methods=['GET'])
def get_data():
    return "messages-service is not implemented yet"


if __name__ == '__main__':
    app.run(port=8082)
