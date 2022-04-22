from flask import Flask
from facade_service import get_data, post_message

app = Flask(__name__)


@app.route('/facade_service', methods=['GET'])
def get():
    return get_data()


@app.route('/facade_service', methods=['POST'])
def post():
    return post_message()


if __name__ == '__main__':
    app.run(port=8080)
