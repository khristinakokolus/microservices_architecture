import argparse
import hazelcast
import consul
import threading
from flask import Flask
import logging

from messages_service import get_messages, post_messages, shutdown_server

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)


@app.route('/message_service', methods=['GET'])
def get():
    messages = get_messages()
    if len(messages) == 0:
        return "messages service has no messages"
    else:
        return "[" + ", ".join(messages) + "]"


@app.route('/message_service_shutdown', methods=['POST'])
def shutdown():
    shutdown_server(hz_client, consul_service, service_id)
    return 'Server shutting down...'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process port number')
    parser.add_argument('--port', type=int)
    args = parser.parse_args()
    port = args.port

    address = "localhost"
    service_name = "message_service"
    service_id = service_name + ":" + str(port)
    consul_service = consul.Consul(host='localhost', port=8500)
    consul_service.agent.service.register(name=service_name, service_id=service_id, address=address, port=port)

    # get configs for Hazelcast
    keys = ['hz_queue_node_1', 'hz_queue_node_2']
    cluster_members = []
    for key in keys:
        cluster_member = consul_service.kv.get(key=key, index=None)[1]['Value'].decode('utf-8')
        cluster_members.append(cluster_member)
    hz_client = hazelcast.HazelcastClient(cluster_members=cluster_members)

    threading.Thread(target=post_messages, args=(consul_service, hz_client), daemon=True).start()

    app.run(port=port)
