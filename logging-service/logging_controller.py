import argparse
import consul
import hazelcast
from flask import Flask, request
import logging

from logging_service import get_data, post_message, shutdown_server

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)


@app.route('/logging_service', methods=['GET'])
def get():
    return get_data(MESSAGES)


@app.route('/logging_service', methods=['POST'])
def post():
    message_data = request.get_json()
    logging.info(message_data)
    return post_message(MESSAGES, message_data)


@app.route('/logging_service_shutdown', methods=['POST'])
def shutdown():
    shutdown_server(hz_client, consul_service, service_id)
    return 'Server shutting down...'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process port number')
    parser.add_argument('--port', type=int)
    args = parser.parse_args()
    port = args.port
    address = "localhost"
    service_name = "logging_service"
    service_id = service_name + ":" + str(port)
    consul_service = consul.Consul(host='localhost', port=8500)
    consul_service.agent.service.register(name=service_name, service_id=service_id, address=address, port=port)

    # get configs for Hazelcast
    keys = ['hz_map_node_1', 'hz_map_node_2', 'hz_map_node_3']
    cluster_members = []
    for key in keys:
        cluster_member = consul_service.kv.get(key=key, index=None)[1]['Value'].decode('utf-8')
        cluster_members.append(cluster_member)
    hz_client = hazelcast.HazelcastClient(cluster_members=cluster_members)

    distributed_map_name = consul_service.kv.get(key='distributed_map_name', index=None)[1]['Value'].decode('utf-8')
    MESSAGES = hz_client.get_map(distributed_map_name).blocking()

    app.run(port=port)
