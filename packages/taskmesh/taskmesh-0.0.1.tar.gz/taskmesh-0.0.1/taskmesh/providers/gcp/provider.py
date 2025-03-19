import json
import os

from google.cloud import pubsub_v1

from taskmesh.config import Config
from taskmesh.core import process_task
from taskmesh.providers import Provider
from taskmesh.providers.core import BackgroundTask


class GCPProvider(Provider):
    def __init__(self, credential_file=None, project_id=None):
        """
        @credential_file: str
            Path to the GCP credential file
        @project_id: str
            The project id
        """
        self.credential_file = credential_file
        if not credential_file:
            self.credential_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        self.project_id = project_id

        if self.credential_file:
            self.set_credential_file(self.credential_file)

        if self.project_id:
            self.set_project_id(self.project_id)

    def set_credential_file(self, credential_file):
        self.credential_file = credential_file
        self.publisher = pubsub_v1.PublisherClient.from_service_account_file(self.credential_file)

    def set_project_id(self, project_id):
        self.project_id = project_id

    def set_topic_id(self, topic_id):
        self.topic = topic_id
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic)

    def publish_message(self, data: dict) -> str:
        try:
            message_json = json.dumps(data).encode("utf-8")
            future = self.publisher.publish(self.topic_path, message_json)
            message_id = future.result()
            print(f"Published message ID: {message_id}")
            return message_id
        except Exception as e:
            print(f"Failed to publish message: {e}")
            return None

    def run(self, topic, func, config):
        self.set_topic_id(topic)
        return BackgroundTask(provider=self, callback=func, conf=config)


class Subscriber:
    def __init__(
        self,
        provider: GCPProvider,
        config: Config = None,
        subscription_name: str = None,
    ):
        """Initialize the Pub/Sub Subscriber with explicit credentials."""
        self.config = config or Config()
        self.provider = provider
        self.project_id = provider.project_id
        self.credentials_path = provider.credential_file
        self.subscription_name = (
            subscription_name if subscription_name else f"{provider.topic_id}-sub"
        )
        self.subscriber = pubsub_v1.SubscriberClient.from_service_account_file(
            self.credentials_path
        )
        self.subscription_path = self.subscriber.subscription_path(
            self.project_id, self.subscription_name
        )

    def callback(self, message: pubsub_v1.subscriber.message.Message):
        """Process received message and acknowledge it."""
        try:
            data = json.loads(message.data.decode("utf-8"))
            print(f"Received message: {data}")
            process_task(data)
            message.ack()  # Acknowledge message after processing
        except Exception as e:
            print(f"Failed to process message: {e}")
        finally:
            if self.config.ack_message_on_error:
                message.ack()

    def start_listening(self):
        """Start listening for messages on the subscription."""
        print(f"Listening for messages on {self.subscription_path}...")
        streaming_pull_future = self.subscriber.subscribe(
            self.subscription_path, callback=self.callback
        )

        try:
            streaming_pull_future.result()  # Keep the process alive
        except KeyboardInterrupt:
            streaming_pull_future.cancel()
            print("Subscriber stopped.")
