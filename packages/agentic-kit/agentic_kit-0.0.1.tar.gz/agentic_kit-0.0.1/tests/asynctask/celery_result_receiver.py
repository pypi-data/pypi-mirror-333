import redis


def subscribe_redis():
    r = redis.Redis(host='localhost', port=6379, db=3)
    pubsub = r.pubsub()
    pubsub.subscribe("my_signal_channel")

    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received notification: {message['data'].decode()}")
