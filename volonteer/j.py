import requests

# Server URL
LOGIN_URL = "https://web-production-927a.up.railway.app/api/login/"

USERNAME = "Zalkarbro"  # Replace with your username
PASSWORD = "zalkarbro"  # Replace with your password

# Payload for the login request
payload = {
    "username": USERNAME,
    "password": PASSWORD
}

# Send the POST request
try:
    response = requests.post(LOGIN_URL, json=payload)
    
    # Print the response
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}") 