import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Server URL
LOGIN_URL = "https://web-production-927a.up.railway.app/token"

USERNAME = "Zalkar2"  # Replace with your username
PASSWORD = "zalkar2"  # Replace with your password

# Configure retry strategy
retry_strategy = Retry(
    total=3,  # Retry 3 times
    backoff_factor=1,  # Wait 1 second between retries
    status_forcelist=[500, 502, 503, 504],  # Retry on these status codes
)

# Create a session with retry logic
session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Payload for the token request (form data)
payload = {
    "username": USERNAME,
    "password": PASSWORD
}

try:
    # Send the request as form data
    response = session.post(LOGIN_URL, data=payload, timeout=10)
    response.raise_for_status()  # Raise an error for bad status codes
    print(f"Status Code: {response.status_code}")
    print("Token Response:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
   