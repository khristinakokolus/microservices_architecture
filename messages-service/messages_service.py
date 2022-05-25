import hazelcast
import logging


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

hz_client = hazelcast.HazelcastClient()
distributed_queue = hz_client.get_queue("messages_queue_distributed").blocking()
messages = []


def get_messages():
    return messages



def post_messages():
    while True:
        message = distributed_queue.take()
        logging.info(message)
        messages.append(message["message"])
