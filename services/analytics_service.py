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


def get_analytics(base_url, token, endpoint, from_date, to_date):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"from": from_date, "to": to_date}
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