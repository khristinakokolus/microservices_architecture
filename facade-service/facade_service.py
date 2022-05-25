from flask import request
import logging
import requests
import random
import uuid
import json


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


logging_service_name = "logging_service"
message_service_name = "message_service"
HTTP_START = "http://"


def get_service_address(consul_service, service_name):
    registered_servers = consul_service.agent.services()
    registered_servers_names = [key for key in registered_servers.keys()] # get_list(registered_servers)
    services_names = [server for server in registered_servers_names if server.startswith(service_name)]
    random_service = random.choice(services_names)
    service_address = HTTP_START + registered_servers[random_service]['Address'] + \
                      ":" + str(registered_servers[random_service]['Port']) + "/" + service_name
    return service_address


def get_data(consul_service):
    try:
        logging_service = get_service_address(consul_service, logging_service_name)
        message_service = get_service_address(consul_service, message_service_name)
        logging.info("Logging service on: " + logging_service)
        logging.info("Message service on: " + message_service)

        logging_service_data = requests.get(logging_service).text
        message_service_data = requests.get(message_service).text
        data = "Logging service messages: " + logging_service_data + "\n" +\
               "Messages service messages: " + message_service_data + "\n"
        return data
    except requests.exceptions.ConnectionError:
        return "Error occurred"


def post_messages_logging(logging_service, data):
    response = requests.post(url=logging_service, data=json.dumps(data),
                             headers={"Content-Type": "application/json"})
    return response


def post_messages_msg_queue(distributed_queue, message):
    try:
        distributed_queue.put(message)
        return 200
    except Exception as err:
        logging.error(f'Producer error: {err}')
        return 404


def post_message(consul_service, distributed_queue):
    message = request.json.get("msg", None)
    message_uuid = str(uuid.uuid4())

    data = {
        "message": message,
        "message_uuid": message_uuid
    }

    logging_service = get_service_address(consul_service, logging_service_name)

    response_logging = post_messages_logging(logging_service, data)
    response_msg_queue = post_messages_msg_queue(distributed_queue, data)

    return {
        "statusCode": [response_logging.status_code, response_msg_queue]
    }


def shutdown_server(hz_client, consul_service, service_id):
    hz_client.shutdown()
    consul_service.agent.service.deregister(service_id)
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

