import time
import json
import logging
from google.cloud import pubsub_v1
from google.api_core.exceptions import PermissionDenied, NotFound
from .config import (
    GOOGLE_APPLICATION_CREDENTIALS,
    GCP_PROJECT_ID,
    PUBSUB_SUBSCRIPTION_NAME,
    TIMEOUT_DURATION,
    OUTPUT_METHOD,
    HTTP_ENDPOINT,
    AUTH_METHOD,
    AUTH_TOKEN,
    API_KEY,
    OUTPUT_DIR,
    LOG_LEVEL
)
from .log_processor import process_log_file

# Global Variables
message_received = False
MAX_RETRIES = 5  # Maximum number of retries for a message

def validate_inputs():
    errors = []

    logging.debug("-----------------------------------------\nEnivronment variables:")
    def validate_string(var_name, var_value):
        logging.debug(f"{var_name}: {var_value}")
        if not var_value or not isinstance(var_value, str) or var_value.strip() == "":
            errors.append(f"{var_name} is required and must be a non-empty string.")

    validate_string("GOOGLE_APPLICATION_CREDENTIALS", GOOGLE_APPLICATION_CREDENTIALS)
    validate_string("GCP_PROJECT_ID", GCP_PROJECT_ID)
    validate_string("PUBSUB_SUBSCRIPTION_NAME", PUBSUB_SUBSCRIPTION_NAME)
    validate_string("OUTPUT_METHOD", OUTPUT_METHOD)

    if OUTPUT_METHOD not in ["http", "files"]:
        errors.append("OUTPUT_METHOD must be either 'http' or 'files'.")

    if OUTPUT_METHOD == "http":
        validate_string("HTTP_ENDPOINT", HTTP_ENDPOINT)
        validate_string("AUTH_METHOD", AUTH_METHOD)
        if AUTH_METHOD not in ["token", "api_key"]:
            errors.append("AUTH_METHOD must be either 'token' or 'api_key' when OUTPUT_METHOD is 'http'.")
        if AUTH_METHOD == "token":
            validate_string("AUTH_TOKEN", AUTH_TOKEN)
        elif AUTH_METHOD == "api_key":
            validate_string("API_KEY", API_KEY)
    elif OUTPUT_METHOD == "files":
        validate_string("OUTPUT_DIR", OUTPUT_DIR)

    if LOG_LEVEL.upper() not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        errors.append("LOG_LEVEL must be one of 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.")

    if errors:
        raise ValueError("Input validation failed with the following errors:\n" + "\n".join(errors))


def is_relevant_event(file_name):
    """Filter relevant file events based on the file name."""
    return "logserv" in file_name


def callback(message):
    global message_received
    logging.debug("Received a message")
    message_received = True

    try:
        message_content = json.loads(message.data.decode("utf-8"))
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON message: {e}")
        message.ack()
        logging.debug("Message acknowledged")
        return

    bucket_name = message_content.get("bucket")
    file_name = message_content.get("name")
    if not bucket_name or not file_name:
        logging.error(f"Missing bucket or file name in message: {message_content}")
        message.ack()
        logging.debug("Message acknowledged")
        return

    # Check for event type and relevant file name
    event_type = message.attributes.get("eventType")
    if event_type != "OBJECT_FINALIZE" or not is_relevant_event(file_name):
        logging.debug(f"Irrelevant message: {event_type}, {file_name}. Skipping message.")
        message.ack()
        logging.debug("Message acknowledged")
        return

    # Retry logic
    retries = 0
    while retries < MAX_RETRIES:
        try:
            process_log_file(bucket_name, file_name)
            logging.info(f"Processed log file from {bucket_name}/{file_name}")
            message.ack()
            logging.debug("Message acknowledged")
            return
        except Exception as e:
            retries += 1
            logging.error(f"Error processing log {bucket_name}/{file_name}: {e}")
            if retries == MAX_RETRIES:
                logging.error(f"Max retries reached for message: {message.data}")
                message.ack()
                logging.debug("Message acknowledged")
                return


def validate_subscription(subscription_path):
    """Check if the Pub/Sub subscription exists and if the service account has access."""
    try:
        # Verify the subscription exists
        subscriber_client = pubsub_v1.SubscriberClient()
        subscriber_client.get_subscription(request={"subscription": subscription_path})
        logging.info(f"Subscription '{subscription_path}' is valid.")
        return True
    except PermissionDenied:
        # Service account does not have 'roles/pubsub.viewer' permission to run 'getSubscription',
        # but it means the subscription exists.
        logging.info(f"Subscription '{subscription_path}' is valid.")
        return True
    except NotFound:
        logging.error(f"Subscription '{subscription_path}' does not exist.")
        return False
    except Exception as e:
        logging.error(f"Unexpected error while validating subscription: {e}")
        return False

def set_log_level():
    """Set the log level based on the LOG_LEVEL environment variable."""
    numeric_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=numeric_level
    )
    logging.info(f"Log level set to {logging.getLevelName(numeric_level)}")

def consume_pub_sub():
    """Main function to consume messages from Pub/Sub."""
    # Set log level
    set_log_level()

    # Validate environment variables
    validate_inputs()

    subscriber_client = pubsub_v1.SubscriberClient()
    subscription_path = subscriber_client.subscription_path(GCP_PROJECT_ID, PUBSUB_SUBSCRIPTION_NAME)

    # Make sure the subscription path is valid
    if not validate_subscription(subscription_path):
        return
    
    # Pull messages from the Pub/Sub subscription
    global message_received
    streaming_pull_future = subscriber_client.subscribe(subscription_path, callback=callback)
    logging.info(f"Listening for messages on {subscription_path}...")

    start_time = time.time()
    try:
        while True:
            elapsed_time = time.time() - start_time
            if TIMEOUT_DURATION and elapsed_time > TIMEOUT_DURATION:
                logging.info("Timeout reached. Exiting.")
                streaming_pull_future.cancel()
                break

            if not message_received:
                logging.info("No messages received. Waiting...")
                time.sleep(20)
            else:
                message_received = False  # Reset flag
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        logging.info("Forwarder stopped by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        streaming_pull_future.cancel()

if __name__ == "__main__":
    consume_pub_sub()
