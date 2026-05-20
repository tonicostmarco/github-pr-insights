import os
import requests
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("ANALYTICS_BASE_URL")

username = os.getenv("ANALYTICS_USERNAME")

password = os.getenv("ANALYTICS_PASSWORD")

def get_token(urlBase, username, password):
    response = requests.post(f'{urlBase}/auth/token',
                             json={'username': username, 'password': password})
    return response.json()['token']


token = get_token(base_url, username, password)

print(token)

def get_summary(base_url, token):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"from": "2025-01-01T00:00:00", "to": "2026-12-31T23:59:59"}
    response = requests.get(f'{base_url}/analytics/summary',
                            params=params, headers=headers)

    return response.json()

summary = get_summary(base_url, token)
print(summary)
def get_authormetrics(base_url, token):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"from": "2025-01-01T00:00:00", "to": "2026-12-31T23:59:59"}
    response = requests.get(f'{base_url}/analytics/authormetrics?',
                            params=params, headers=headers)

    return response.json()

authormetrics = get_authormetrics(base_url, token)
print(authormetrics)
def get_repositorymetrics(base_url, token):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"from": "2025-01-01T00:00:00", "to": "2026-12-31T23:59:59"}
    response = requests.get(f'{base_url}/analytics/repositorymetrics?',
                            params=params, headers=headers)

    return response.json()

repositorymetrics = get_repositorymetrics(base_url, token)
print(repositorymetrics)