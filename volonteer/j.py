import requests

# Server URL
LOGIN_URL = "https://web-production-927a.up.railway.app/api/login"

USERNAME = "Zalkar2"  # Replace with your username
PASSWORD = "venvvenvvenv"  # Replace with your password

# Payload for the token request (form data)
payload = {
    "username": USERNAME,
    "password": PASSWORD
}

try:
    # Send the request as form data
    response = requests.post(LOGIN_URL, data=payload, timeout=10)
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)  # Print raw response content
    response.raise_for_status()
    print("Response JSON:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
   