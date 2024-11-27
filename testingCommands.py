import requests
import json

BASE_URL = 'http://localhost:3000/api'

def create_user(name, email):
    url = f'{BASE_URL}/users'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'name': name,
        'email': email
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 201:
        print('User created successfully:')
        print(response.json())
        return response.json().get('id')
    else:
        print('Failed to create user:')
        print(response.status_code, response.text)
        return None

def get_user(user_id):
    url = f'{BASE_URL}/users/{user_id}'
    response = requests.get(url)
    
    if response.status_code == 200:
        print('User retrieved successfully:')
        print(response.json())
    elif response.status_code == 404:
        print('User not found:')
        print(response.text)
    else:
        print('Failed to retrieve user:')
        print(response.status_code, response.text)