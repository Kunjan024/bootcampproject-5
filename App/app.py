import os
import json
from flask import Flask
from google.cloud import pubsub_v1

app = Flask(__name__)

# Set your actual project ID and topic name
project_id = "bootcampproject-5-465900"
topic_id = "stream-topic"

# Pub/Sub client setup
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
    future.result()

    branch = os.environ.get('BRANCH_NAME', 'unknown')
    return f"Hello World from {branch} branch! Message published to Pub/Sub."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
