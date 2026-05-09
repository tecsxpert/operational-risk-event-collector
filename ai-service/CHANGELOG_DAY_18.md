# Day 18 - Demo Day Script (AI Developer 1)

## Demo Script — AI Developer 1 Section (90 seconds)

### Opening (30s)
Say: 'Tool-66 is an AI-powered Operational Risk Event Collector. It replaces manual spreadsheet tracking with automated AI analysis. I will show you three AI features live.'

### Architecture Callout (15s)
Point to diagram: Flask AI microservice on port 5000, connected to Groq LLaMA-3.3-70b, with Redis caching, integrated via AiServiceClient.java into Spring Boot.

### Live Demo — Create Record (45s)
1. Navigate to frontend Create Event form
2. Enter: Title='Core Banking System Timeout', Description='The core banking system experienced a 45-minute timeout during peak trading hours on 1 May 2026, affecting 12,000 customer transactions.'
3. Submit - say: 'The Java backend saves this, then asynchronously calls our Flask AI service'
4. Refresh detail page - show AI description appearing: event_type, severity, risk_score
5. Say: 'The AI classified this as Technology Risk, High severity, risk score 48 - all done in under 2 seconds'

