from flask import Flask

app = Flask(__name__)


@app.route('/facade_service', methods=['GET'])
def get():
    return 'Got data'


@app.route('/facade_service', methods=['POST'])
def post():
    return 'Post Data'


if __name__ == '__main__':
    app.run(port=8080)
