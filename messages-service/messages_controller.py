import threading
from flask import Flask

from messages_service import get_messages, post_messages

app = Flask(__name__)


threading.Thread(target=post_messages, daemon=True).start()


@app.route('/message_service', methods=['GET'])
def get():
    messages = get_messages()
    if len(messages) == 0:
        return "messages service has no messages"
    else:
        return "[" + ", ".join(messages) + "]"
