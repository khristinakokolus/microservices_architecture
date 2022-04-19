import hazelcast


def main():
    # Start Hazelcast client
    print("Starting connecting to the Hazelcast client...")
    hz = hazelcast.HazelcastClient()
    print("Connected to the Hazelcast client")
    # Get the Distributed Map from Cluster.
    hz_map = hz.get_map("distributed_map").blocking()
    print("Created a distributed map")
    # Standard Put and Get
    for i in range(1, 1001):
        print(str(i) + " value")
        hz_map.put(i, str(i) + " value")
    # Shutdown this Hazelcast Client
    hz.shutdown()
    print("Shutdown Hazelcast client")


if __name__ == "__main__":
    main()
