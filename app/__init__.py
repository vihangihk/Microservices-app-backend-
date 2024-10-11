from flask import Flask
from flask_cors import CORS
import threading
from google.cloud import pubsub_v1

def create_app():
    app = Flask(__name__)
    CORS(app)

    # PubSub configuration
    project_id = "quantum-star-435523-g9"
    subscription_id = "my-sub"
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        message_data = message.data.decode("utf-8")
        print(f"Received message: {message_data}")
        
        with app.app_context():
            from .routes import insert_message
            insert_message(message_data)
        
        message.ack()

    def start_subscriber():
        with subscriber:
            streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
            print(f"Listening for messages on {subscription_path}..\n")
            try:
                streaming_pull_future.result()
            except Exception as e:
                print(f"Subscriber error: {e}")

    # Start the subscriber in a separate thread
    subscriber_thread = threading.Thread(target=start_subscriber)
    subscriber_thread.start()

    # Import routes
    with app.app_context():
        from . import routes

    return app