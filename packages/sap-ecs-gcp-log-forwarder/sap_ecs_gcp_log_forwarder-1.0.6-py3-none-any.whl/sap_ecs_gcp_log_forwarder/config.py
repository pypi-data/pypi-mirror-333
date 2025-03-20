import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file in the directory you are running the script from
# If a .env file is not found, the script reads from the system environment variables (exported variables)

# Load from .env file only if environment variables are not set
if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    dotenv_path = find_dotenv(filename=".env", raise_error_if_not_found=False, usecwd=True)
    if dotenv_path:
        load_dotenv(dotenv_path)
        print(f"Loaded .env from: {dotenv_path}")
    else:
        print(f"No .env file found in {dotenv_path}")

# Of the external project (Required)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Of the CLZ project where the files are (Required)
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
PUBSUB_SUBSCRIPTION_NAME = os.getenv('PUBSUB_SUBSCRIPTION_NAME')

# Optional
TIMEOUT_DURATION = int(os.getenv('TIMEOUT_DURATION', 0)) or None  # Convert to int if not None

# Output method (Required)
OUTPUT_METHOD = os.getenv('OUTPUT_METHOD', 'http') # 'http' or 'files'

# For HTTP output method
HTTP_ENDPOINT = os.getenv('HTTP_ENDPOINT')
TLS_CERT_PATH = os.getenv('TLS_CERT_PATH') # Optional
TLS_KEY_PATH = os.getenv('TLS_KEY_PATH') # Optional
AUTH_METHOD = os.getenv('AUTH_METHOD', 'token') # 'token' or 'api_key'
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
API_KEY = os.getenv('API_KEY')

# For files output method
OUTPUT_DIR = os.getenv('OUTPUT_DIR')

# Optional
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO') # 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'