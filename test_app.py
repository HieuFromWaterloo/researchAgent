import requests

# Define the URL for your Flask app
url = 'http://127.0.0.1:5000/query'

# Define the JSON data to send in the request
data = {
    'query': 'How to train an LLM with RLHF?'
}

# Send a POST request to your Flask app
response = requests.post(url, json=data)

# Check the response status code and content
if response.status_code == 200:
    print('Response:', response.json())
else:
    print('Error:', response.status_code)
