# Day 5 - @Async AI Integration

## Tasks Completed
- Integrated AiServiceClient.java into RiskEventService.java
- AI describe() called @Async on every new risk event creation
- ai_description, ai_severity, ai_risk_score fields attached to entity
- Null handling: if AI returns null, event saved with ai_description=null
- No HTTP 500 thrown due to AI unavailability
- Confirmed async - create endpoint returns immediately, AI fills in background
- RestTemplate configured with 10-second connect + read timeout

