import copy
import hazelcast
from multiprocessing import Process


# rewritten to Python https://docs.hazelcast.com/imdg/latest/data-structures/map.html#locking-maps
def racy_update_member():
    print("Starting connecting to the Hazelcast client for racy update...")
    client = hazelcast.HazelcastClient()
    print("Connected to the Hazelcast client for racy update")
    hz_map = client.get_map("distributed_map_with_locks").blocking()
    print("Created a distributed map for racy update")

    key = "1"
    hz_map.put_if_absent(key, 0)

    print("Starting racy update...")
    for i in range(0, 1000):
        if i % 100 == 0:
            print("Racy. At: ", i)
        value = hz_map.get(key)
        value += 1
        hz_map.put(key, value)

    print("Finished racy update! Result = ", hz_map.get(key))
    client.shutdown()


def pessimistic_update_member():
    print("Starting connecting to the Hazelcast client for pessimistic update...")
    client = hazelcast.HazelcastClient()
    print("Connected to the Hazelcast client for pessimistic update")
    hz_map = client.get_map("distributed_map_with_locks").blocking()
    print("Created a distributed map for pessimistic update")

    key = "1"
    hz_map.put_if_absent(key, 0)

    print("Starting pessimistic update..")
    for i in range(0, 1000):
        hz_map.lock(key)
        try:
            value = hz_map.get(key)
            value += 1
            hz_map.put(key, value)
        finally:
            hz_map.unlock(key)

    print("Finished for pessimistic update! Result = ", hz_map.get(key))
    client.shutdown()


def optimistic_member():
    print("Starting connecting to the Hazelcast client for optimistic update...")
    client = hazelcast.HazelcastClient()
    print("Connected to the Hazelcast client for optimistic update")
    hz_map = client.get_map("distributed_map_with_locks").blocking()
    print("Created a distributed map for optimistic update")

    key = "1"
    hz_map.put_if_absent(key, 0)

    print("Starting optimistic update...")
    for i in range(0, 1000):
        if i % 10 == 0:
            print("Optimistic. At: ", i)
        while True:
            old_value = hz_map.get(key)
            new_value = copy.deepcopy(old_value)
            new_value += 1
            if hz_map.replace_if_same(key, old_value, new_value):
                break

    print("Finished for optimistic update! Result = ", hz_map.get(key))
    client.shutdown()


if __name__ == '__main__':
    functions = [racy_update_member, pessimistic_update_member, optimistic_member]

    processes = []
    for func in functions:
        process = Process(target=func)
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
