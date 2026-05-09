# Tool-66 AI Microservice

**Operational Risk Event Collector — AI Service**  
Flask 3.x · Python 3.11 · Groq LLaMA-3.3-70b · Redis Cache · Docker

---

## Overview

This microservice provides three AI-powered endpoints for the Tool-66 Operational Risk Event Collector:

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/ai/describe` | POST | Analyse a risk event and return structured JSON |
| `/api/ai/recommend` | POST | Generate 3 risk mitigation recommendations |
| `/api/ai/generate-report` | POST | Generate a comprehensive risk report |
| `/health` | GET | Service health, uptime, and Groq model status |

All endpoints are rate-limited to **30 requests/minute per IP**.  
All endpoints return a fallback response (`is_fallback: true`) when Groq is unavailable — the service **never** returns HTTP 500 due to AI unavailability.

---

## Prerequisites

| Requirement | Version | Install |
|---|---|---|
| Python | 3.11+ | python.org |
| pip | latest | bundled with Python |
| Redis | 7.x | docker or redis.io |
| Groq API Key | — | console.groq.com (free, no card) |
| Docker (optional) | 24+ | docker.com |

---

## Setup — Local Development

### 1. Clone and enter directory
```bash
git clone https://github.com/keerthiraju162-bit/Assignment-2.git
cd Assignment-2/ai-service
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp ../.env.example .env
# Edit .env and set GROQ_API_KEY
```

### 5. Start Redis (Docker — simplest method)
```bash
docker run -d -p 6379:6379 --name redis redis:7-alpine
```

### 6. Run the service
```bash
flask --app app run --host=0.0.0.0 --port=5000
```

Service is available at: `http://localhost:5000`

---

## Setup — Docker Compose (Full Stack)

```bash
# From project root:
cp .env.example .env
# Edit .env and set GROQ_API_KEY

docker-compose up --build
```

AI service available at: `http://localhost:5000/health`

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GROQ_API_KEY` | **Yes** | — | API key from console.groq.com |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Redis connection URL for caching |
| `AI_PORT` | No | `5000` | Port to run the Flask service on |
| `FLASK_DEBUG` | No | `false` | Set `true` for development only |

---

## API Reference

### POST /api/ai/describe

Analyse an operational risk event and return a structured risk assessment.

**Request:**
```json
{
  "title": "Payment System Outage",
  "description": "The payment processing system went offline for 2 hours on 14 April 2026 due to a database connection pool exhaustion, affecting 5,000 customer transactions.",
  "event_date": "2026-04-14",
  "department": "Payments"
}
```

**Response (200 OK):**
```json
{
  "event_type": "Technology Risk",
  "severity": "High",
  "impact_score": 8,
  "likelihood_score": 5,
  "risk_score": 40,
  "description": "A critical technology failure caused the payment processing system to become unavailable for two hours, directly impacting customer transaction capability and operational continuity.",
  "root_cause": "Database connection pool exhaustion caused by a surge in concurrent transactions without adequate connection management configuration.",
  "affected_areas": ["Payments", "Customer Services", "Operations"],
  "regulatory_flags": ["Basel III Operational Risk", "PCI DSS"],
  "generated_at": "2026-04-14T09:23:11+00:00",
  "is_fallback": false
}
```

**Error Response (400):**
```json
{
  "error": "Missing required fields: description",
  "code": 400
}
```

---

### POST /api/ai/recommend

Generate exactly 3 risk mitigation recommendations for a given risk event.

**Request:**
```json
{
  "title": "Unauthorised Data Access",
  "description": "A former employee's credentials were not revoked and were used to access confidential customer data.",
  "severity": "Critical",
  "risk_score": 72
}
```

**Response (200 OK):**
```json
{
  "recommendations": [
    {
      "action_type": "Immediate",
      "priority": "Critical",
      "description": "Revoke all active sessions and credentials for the former employee immediately and conduct a full access audit.",
      "owner": "IT Security",
      "estimated_effort": "Low",
      "expected_outcome": "Eliminates ongoing unauthorised access within 24 hours."
    },
    {
      "action_type": "Short-Term",
      "priority": "High",
      "description": "Implement an automated offboarding workflow that revokes all system access on the employee's last working day.",
      "owner": "HR and IT",
      "estimated_effort": "Medium",
      "expected_outcome": "Prevents recurrence of access credential lapses within 30 days."
    },
    {
      "action_type": "Long-Term",
      "priority": "Medium",
      "description": "Deploy a Privileged Access Management (PAM) solution with quarterly access reviews.",
      "owner": "Risk Management",
      "estimated_effort": "High",
      "expected_outcome": "Systematic control over privileged access reducing risk by 80%."
    }
  ],
  "overall_risk_reduction": "Combined implementation reduces the risk score from Critical to Low within 90 days.",
  "generated_at": "2026-04-14T10:15:00+00:00",
  "is_fallback": false
}
```

---

### POST /api/ai/generate-report

Generate a comprehensive operational risk report from a list of events.

**Request:**
```json
{
  "events": [
    {"title": "Payment System Outage", "severity": "High", "risk_score": 40, "event_type": "Technology Risk"},
    {"title": "Data Breach Attempt", "severity": "Critical", "risk_score": 72, "event_type": "External Fraud"},
    {"title": "Process Documentation Gap", "severity": "Low", "risk_score": 8, "event_type": "Process Failure"}
  ],
  "reporting_period": "April 2026",
  "report_title": "Q2 2026 Operational Risk Report"
}
```

**Response (200 OK):**
```json
{
  "title": "Q2 2026 Operational Risk Report",
  "executive_summary": "Three operational risk events were recorded in April 2026, including one Critical severity event (Data Breach Attempt) with a risk score of 72. The overall risk posture requires immediate attention to the external fraud threat vector.",
  "overview": {
    "total_events": 3,
    "critical_count": 1,
    "high_count": 1,
    "medium_count": 0,
    "low_count": 1,
    "average_risk_score": 40.0,
    "reporting_period": "April 2026"
  },
  "key_risk_themes": [
    {"theme": "External Fraud", "event_count": 1, "description": "One critical external fraud event requiring immediate escalation."}
  ],
  "top_events": [
    {"event_id": null, "title": "Data Breach Attempt", "severity": "Critical", "risk_score": 72, "summary": "Unauthorised external access attempt on customer data systems."}
  ],
  "recommendations": [
    "Escalate the Data Breach Attempt to the Risk Committee immediately.",
    "Conduct a full cybersecurity audit within 30 days.",
    "Review and update the Business Continuity Plan for technology failures."
  ],
  "conclusion": "The April 2026 risk profile highlights the need for enhanced cybersecurity controls and proactive monitoring.",
  "generated_at": "2026-04-30T17:00:00+00:00",
  "is_fallback": false
}
```

---

### GET /health

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "Tool-66 AI Microservice",
  "model": "llama-3.3-70b-versatile",
  "avg_response_time_ms": 1247.5,
  "performance_status": "optimal",
  "uptime": "01h 23m 45s",
  "uptime_seconds": 5025,
  "redis_cache": "connected",
  "endpoints": [
    {"method": "POST", "path": "/api/ai/describe"},
    {"method": "POST", "path": "/api/ai/recommend"},
    {"method": "POST", "path": "/api/ai/generate-report"},
    {"method": "GET",  "path": "/health"}
  ],
  "rate_limit": "30 requests/minute per IP"
}
```

---

## Running Tests

Tests run **without live network access** — Groq API is fully mocked.

```bash
cd ai-service
pytest tests/ -v
```

Expected: **8 tests passing**

---

## Security Features

- Input sanitisation via `bleach` (HTML stripping)
- Prompt injection detection (15+ regex patterns)
- Rate limiting: 30 req/min per IP via `flask-limiter`
- Security response headers (X-Content-Type-Options, X-Frame-Options, CSP, HSTS)
- Non-root Docker user
- No PII stored in prompts or logs

See `SECURITY.md` in the project root for the full threat model.

---

## Architecture

```
React Frontend (port 80)
        │
        ▼
Spring Boot Backend (port 8080)
        │
        ├── PostgreSQL 15 (DB)
        ├── Redis 7 (cache)
        └── AiServiceClient.java
                  │
                  ▼
        Flask AI Service (port 5000)
                  │
                  ├── Redis (AI response cache — 15 min TTL)
                  └── Groq API (LLaMA-3.3-70b)
```

---

*Tool-66 Capstone Project · AI Developer 1 · Sprint: 14 April – 9 May 2026*
