import os
import requests
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

BASE_URL = os.getenv("ANALYTICS_BASE_URL")
USERNAME = os.getenv("ANALYTICS_USERNAME")
PASSWORD = os.getenv("ANALYTICS_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def get_token(base_url, username, password):
    response = requests.post(
        f"{base_url}/auth/token",
        json={"username": username, "password": password}
    )
    return response.json()["token"]


def get_analytics(base_url, token, endpoint, date_from, date_to):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"from": date_from, "to": date_to}
    response = requests.get(f"{base_url}/analytics/{endpoint}", params=params, headers=headers)
    return response.json()


def analyze_data(summary, author_metrics, repository_metrics, api_key):
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": (
                    "Analise os dados das pull requests a seguir. Monte um resumo do que foi feito, quem fez, "
                    "quantos repositórios existem, quem fez mais PRs, quem mais abriu/fechou, se houveram ou não.\n\n"
                    f"Summary:\n{summary}\n\n"
                    f"Author Metrics:\n{author_metrics}\n\n"
                    f"Repository Metrics:\n{repository_metrics}"
                )
            }
        ],
        temperature=1,
        max_completion_tokens=8192,
        top_p=1,
        stream=False,
        stop=None
    )
    return completion.choices[0].message.content

def validation(token_header, date_from, date_to):
    headers = {"Authorization": f"Bearer {token_header}"}
    params = {"from": date_from, "to": date_to}
    response = requests.get(f"{BASE_URL}/analytics/summary", params=params, headers=headers)
    if  response.status_code == 200:
        return True
    else:
        return False

def init(date_from, date_to, token_header):


    if validation(token_header, date_from, date_to):
        token = get_token(BASE_URL, USERNAME, PASSWORD)
        summary = get_analytics(BASE_URL, token, "summary", date_from, date_to)
        author_metrics = get_analytics(BASE_URL, token, "authormetrics", date_from, date_to)
        repository_metrics = get_analytics(BASE_URL, token, "repositorymetrics", date_from, date_to)
        return analyze_data(summary, author_metrics, repository_metrics, GROQ_API_KEY)
    else:
        return "Unauthorized"




