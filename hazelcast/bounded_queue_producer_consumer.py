import sys
sys.path.insert(0, r"c:\users\user\appdata\local\schrodinger\pymol2\lib\site-packages")

import hazelcast
from multiprocessing import Process


def producer(proc_number):
    print("Starting connecting to the Hazelcast client for producer...")
    client = hazelcast.HazelcastClient()
    print("Connected to the Hazelcast client for producer")
    queue = client.get_queue("distributed_queue").blocking()
    print("Created a distributed queue for producer")

    for i in range(100):
        queue.put(str(i) + " value")
        print("Producing: ", i)

    queue.put(-1)
    print("Producer finished!")


def consumer(proc_number):
    print("Starting connecting to the Hazelcast client for consumer...")
    client = hazelcast.HazelcastClient()
    print("Connected to the Hazelcast client for consumer")
    queue = client.get_queue("distributed_queue").blocking()
    print("Created a distributed queue for consumer")

    while True:
        item = queue.take()
        print("Consumed: ", item, ". Process: ", proc_number)
        if item == -1:
            queue.put(-1)
            break

    print("Consumer finished!")


if __name__ == '__main__':
    functions = [producer, consumer, consumer]

    processes = []
    proc_number = 1
    for func in functions:
        process = Process(target=func, args=(proc_number,))
        process.start()
        processes.append(process)
        proc_number += 1
    for process in processes:
        process.join()
