from flask import request

def get_data(messages):
    edited_messages = "[" + ", ".join(list(messages.values())) + "]"
    return edited_messages


def post_message(messages, message_data):
    messages.put(message_data["message_uuid"], message_data["message"])

    return {
        "statusCode": 200
    }


def shutdown_server(hz_client, consul_service, service_id):
    hz_client.shutdown()
    consul_service.agent.service.deregister(service_id)
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
