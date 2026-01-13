import os
import json
import logging
from datetime import datetime
from google.cloud import pubsub_v1

PROJECT_ID = os.getenv("PROJECT_ID", "carbon-hulling-480701-e8")
TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "sensor-topic")

class PubSub:
    def __init__(self, project_id=PROJECT_ID, topic_id=TOPIC_ID):
        self.project_id = project_id
        self.topic_id = topic_id
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

    def publish(self, data):
        try:
            data_bytes = json.dumps(data).encode('utf-8')
            future = self.publisher.publish(self.topic_id, data_bytes) 
            return future
        
        except ValueError as e:
            logging.error(e)
            raise e