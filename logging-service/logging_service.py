import hazelcast

hz_client = hazelcast.HazelcastClient()
messages = hz_client.get_map("distributed_logging_map").blocking()


def get_data():
    return messages


def post_message(message_data):
    messages.put(message_data["message_uuid"], message_data["message"])

    return {
        "statusCode": 200
    }

