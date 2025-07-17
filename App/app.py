from google.cloud import pubsub_v1
import json

project_id = os.environ.get("GCP_PROJECT")  # or hardcode your project ID
topic_id = "stream-topic"  # your Pub/Sub topic name

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

@app.route('/')
def hello():
    message_dict = {
        "user_id": "user_123",
        "action": "click",
        "timestamp": "2025-07-17T21:00:00Z"
    }
    message_json = json.dumps(message_dict).encode("utf-8")
    future = publisher.publish(topic_path, message_json)
    future.result()  # Wait for publish confirmation

    branch = os.environ.get('BRANCH_NAME', 'unknown')
    return f"Hello World from {branch} branch! Message published to Pub/Sub."
