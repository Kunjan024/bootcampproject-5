from google.cloud import pubsub_v1
import json, time, random

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("bootcampproject-5-465900", "stream-topic")

max_messages = 50
count = 0

while count < max_messages:
    data = {
        "user_id": f"user_{random.randint(1,100)}",
        "action": random.choice(["click", "purchase", "view"]),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    publisher.publish(topic_path, json.dumps(data).encode("utf-8"))
    print(f"Published: {data}")
    time.sleep(2)
    count += 1
