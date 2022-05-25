import argparse
import consul
import hazelcast
from flask import Flask
from facade_service import get_data, post_message, shutdown_server

app = Flask(__name__)


@app.route('/facade_service', methods=['GET'])
def get():
    return get_data(consul_service)


@app.route('/facade_service', methods=['POST'])
def post():
    return post_message(consul_service, MESSAGES_QUEUE)


@app.route('/facade_service_shutdown', methods=['POST'])
def shutdown():
    shutdown_server(hz_client, consul_service, service_id)
    return 'Server shutting down...'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process port number')
    parser.add_argument('--port', type=int)
    args = parser.parse_args()
    port = args.port
    address = "localhost"
    service_name = "facade_service"
    service_id = service_name + ":" + str(port)
    consul_service = consul.Consul(host='localhost', port=8500)
    consul_service.agent.service.register(name=service_name, service_id=service_id,
                                          address=address, port=port)

    # get configs for Hazelcast
    keys = ['hz_queue_node_1', 'hz_queue_node_2']
    cluster_members = []
    for key in keys:
        cluster_member = consul_service.kv.get(key=key, index=None)[1]['Value'].decode('utf-8')
        cluster_members.append(cluster_member)
    hz_client = hazelcast.HazelcastClient(cluster_members=cluster_members)

    # get configs for Hazelcast Message queue
    distributed_queue_name = consul_service.kv.get(key='message_queue_name', index=None)[1]['Value'].decode('utf-8')
    MESSAGES_QUEUE = hz_client.get_queue(distributed_queue_name).blocking()

    app.run(port=port)
