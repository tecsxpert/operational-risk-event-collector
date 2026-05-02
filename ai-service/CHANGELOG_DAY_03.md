# Day 3 - POST /describe Endpoint

## Tasks Completed
- Built routes/describe.py with POST /api/ai/describe
- Input validation: title and description required fields
- HTML sanitisation via bleach, prompt injection detection
- Loads prompts/describe.txt, calls Groq API
- Returns structured JSON: event_type, severity, impact_score, likelihood_score, risk_score, description, root_cause, affected_areas, regulatory_flags, generated_at
- Returns fallback (is_fallback: true) when Groq unavailable
- HTTP 400 on missing/invalid input, 200 on success

