# 🔍 github-pr-insights

AI-powered analytics layer for [github-pr-analyzer](https://github.com/tonicostmarco/githubpranalyzer). Consumes the analytics API and uses an LLM to generate natural language insights about pull request data, eliminating the need to interpret raw metrics manually.

![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange?style=flat-square)

---

## 🧭 Why I Built This

The github-pr-analyzer collects and exposes PR data via API, but manually interpreting summary, author metrics, and repository metrics is repetitive work. This service delegates that analysis to AI, so the developer only has to focus on coding.

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| Framework | FastAPI |
| LLM | Groq (LLaMA 3.3 70B) |
| HTTP client | requests |
| Configuration | python-dotenv |

---

## 🔌 API Flow

1. The client authenticates against github-pr-analyzer via `/auth/token` and receives a JWT.
2. The client calls `/insights/` passing the JWT in the `Authorization` header.
3. The API validates the token by forwarding it to github-pr-analyzer. If it returns 401, the analysis is denied.
4. With a valid token, the API fetches data from `/analytics/summary`, `/analytics/authormetrics`, and `/analytics/repositorymetrics`.
5. The data is sent to Groq, which generates a natural language summary.
6. The insight is returned to the client.

---

## 🔐 Authorization

Access to `/insights/` is restricted to users with a valid github-pr-analyzer token. Validation is delegated to the Java API: if it accepts the token, access is granted; if it returns 401, access is denied.

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
ANALYTICS_BASE_URL=http://localhost:8080
ANALYTICS_USERNAME=admin
ANALYTICS_PASSWORD=admin123
GROQ_API_KEY=your_key_here
```

To get a Groq API key, create an account at [console.groq.com](https://console.groq.com), go to the API Keys tab and generate a key.

---

## 🛠️ Running Locally

### Prerequisites

| Tool | Version |
|---|---|
| Python | 3.13+ |
| github-pr-analyzer | running on port 8080 |

Clone and start the github-pr-analyzer first by following the instructions in its [README](https://github.com/tonicostmarco/githubpranalyzer).

### Setup

```bash
git clone https://github.com/tonicostmarco/github-pr-insights
cd github-pr-insights

python -m venv venv
source venv/bin/activate

pip install fastapi uvicorn requests groq python-dotenv
```

### Generating test data

The github-pr-analyzer must be running with `docker compose up -d` before proceeding. Then send a sample webhook:

```bash
curl -X POST "http://localhost:8080/webhook/notify" \
  -H "X-GitHub-Delivery: test-delivery-001" \
  -H "X-Hub-Signature-256: <hmac_signature>" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "opened",
    "number": 42,
    "pull_request": {
      "title": "Fix bug on login",
      "state": "open",
      "merged": true,
      "user": { "login": "tonicostmarco" },
      "created_at": "2026-01-15T10:00:00Z",
      "merged_at": "2025-06-10T14:00:00Z"
    },
    "repository": {
      "full_name": "tonicostmarco/github-pr-analyzer"
    }
  }'
```

### Start the server

```bash
uvicorn main:app --reload
```

Interactive docs available at `http://127.0.0.1:8000/docs`.

---

## 📋 Endpoints

### GET /insights/

Generates a natural language analysis of pull request data for a given date range.

**Query parameters:**

| Parameter | Type | Required | Example |
|---|---|---|---|
| `date_from` | string | ✅ | `2025-01-01T00:00:00` |
| `date_to` | string | ✅ | `2026-12-31T23:59:59` |

**Headers:**

```
Authorization: Bearer <token>
```

**Example request:**

First, obtain a token from the Java API:

```bash
curl -X POST "http://localhost:8080/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Then call the insights endpoint:

```bash
curl -X GET "http://127.0.0.1:8000/insights/?date_from=2025-01-01T00:00:00&date_to=2026-12-31T23:59:59" \
  -H "Authorization: Bearer your_token"
```

**Example response:**

```json
{
  "status": "ok",
  "result": "There is 1 repository with 1 pull request in total. It was opened and merged by tonicostmarco. No pull requests were closed without being merged."
}
```

**Error responses:**

| Code | Meaning |
|---|---|
| `401 Unauthorized` | Missing or invalid token (delegated to Java API) |

---

## 🗺️ Roadmap

- [ ] Expose token retrieval as a dedicated endpoint
- [ ] Support multiple date range presets (last 7 days, last 30 days)
- [ ] Deploy to AWS EC2 alongside github-pr-analyzer

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
