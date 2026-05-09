# Day 20 - Demo Day Final

## Live Demo Results
- Tool started: docker-compose up (48s boot time)
- 30 seeded demo records visible

## AI Features Demonstrated
### 1. POST /api/ai/describe
Input: Core Banking System Timeout
Output: Technology Risk, High severity, risk_score=48, affected_areas=[Core Banking, Operations]
Response time: 1,312ms

### 2. POST /api/ai/recommend
Input: Same event
3 recommendations returned:
- Immediate: Isolate and restart affected connection pools
- Short-Term: Implement circuit breaker pattern
- Long-Term: Deploy active-active HA architecture
Response time: 1,445ms

### 3. POST /api/ai/generate-report
Input: 30 demo records
Output: Full board-level report with executive summary, KPI overview, 4 risk themes, top 5 events, 3 recommendations
Response time: 1,876ms

## Panel Questions Answered
Q: What AI model? A: Groq LLaMA-3.3-70b-versatile, free tier, <2s response time
Q: What if Groq is down? A: Fallback templates - service never returns 500
Q: How is it secured? A: Rate limiting, prompt injection detection, security headers, non-root Docker user

## Sprint Complete

