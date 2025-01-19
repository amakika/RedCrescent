import requests

# Local server URL
LOGIN_URL = "http://127.0.0.1:8000/api/login/"

# User credentials (use the superuser credentials you created)
USERNAME = "Zalkar2"  # Replace with your superuser username
PASSWORD = "zalkar2"  # Replace with your superuser password

# Payload for the login request
payload = {
    "username": USERNAME,
    "password": PASSWORD
}

# Send the POST request
try:
    response = requests.post(LOGIN_URL, json=payload)
    
    # Print the raw response for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Raw Response Content: {response.text}")  # Print raw response content
    
    # Attempt to parse JSON only if the response is not empty
    if response.text.strip():  # Check if response is not empty
        print(f"Response JSON: {response.json()}")
    else:
        print("Empty response received from the server.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except ValueError as e:
    print(f"Failed to parse JSON response: {e}")