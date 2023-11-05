import requests
# curl -X POST \
#   -H "Content-Type: application/json" \
#   -d '{"query": "What are the top misconceptions About Bitcoin and why they are missing the big picture. And, what some key reasons to invest in Bitcoin today?"}' \
#   http://18.212.120.215:8000/query

query="What are the top misconceptions about Bitcoin and why they are missing the big picture. And, what some key reasons to invest in Bitcoin today?"

def send_api_request(query):
    # Define the URL for your Flask app
    # or ECS endpoint:  http://18.212.120.215:8000/query
    url = 'http://localhost:5000/query'

    # Define the JSON data to send in the request
    data = {
        'query': query
    }

    # Define the headers
    headers = {
        'Content-Type': 'application/json',
    }

    try:
        # Send a POST request to your Flask app
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()

        # Check the response status code and content
        if response.status_code == 200:
            return {
                'success': True,
                'response_data': response_json
            }
        else:
            return {'success': False, 
                    'error_message': f'Error: {response.status_code}'}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}

def main():
    result = send_api_request(query)
    if result['success']:
        print(f"Response:\n{result['response_data']}")
    else:
        print(result['error_message'])

if __name__ == '__main__':
    main()

