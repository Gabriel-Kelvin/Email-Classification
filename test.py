import requests
import json

url = "http://127.0.0.1:8000/classify-email"
payload = {
    "input_email_body": "Hello, my name is John Doe. My email is johndoe@example.com and my phone number is 123-456-7890. I'm having issues with my subscription."
}
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(json.dumps(response.json(), indent=2))