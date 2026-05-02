# Day 6 - POST /generate-report Endpoint

## Tasks Completed
- Built routes/report.py with POST /api/ai/generate-report
- Accepts events[] array + reporting_period + report_title
- Returns: title, executive_summary, overview (total/critical/high/medium/low counts, avg_risk_score), key_risk_themes, top_events (up to 5), recommendations (3), conclusion, generated_at
- Cap at 50 events for token budget, max 100 events per request
- Fallback report returned when Groq unavailable (is_fallback: true)
- Prompt loaded from prompts/generate_report.txt
- AiServiceClient.java generateReport() method added

