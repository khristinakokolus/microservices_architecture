import logging
from flask import request


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
messages = []


def get_messages():
    return messages


def initialize_queue(consul_service, hz_client):
    distributed_queue_name = consul_service.kv.get(key='message_queue_name', index=None)[1]['Value'].decode('utf-8')
    distributed_queue = hz_client.get_queue(distributed_queue_name).blocking()
    return distributed_queue


def post_messages(consul_service, hz_client):
    distributed_queue = initialize_queue(consul_service, hz_client)
    while True:
        message = distributed_queue.take()
        logging.info(message)
        messages.append(message["message"])


def shutdown_server(hz_client, consul_service, service_id):
    hz_client.shutdown()
    consul_service.agent.service.deregister(service_id)
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()