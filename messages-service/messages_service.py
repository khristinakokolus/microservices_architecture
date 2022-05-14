import hazelcast

hz_client = hazelcast.HazelcastClient()
queue = hz_client.get_queue("distributed_messages_queue").blocking()


def consumer():
    items = []
    while not queue.is_empty():
        item = queue.take()
        items.append(item["message"])
    return items


def producer(message):
    queue.put(message)

    return {
        "statusCode": 200
    }

