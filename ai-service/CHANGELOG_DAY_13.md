# Day 13 - Docker Packaging

## Dockerfile
- Base: python:3.11-slim
- Non-root user 'aiservice' added (security requirement)
- HEALTHCHECK: curl http://localhost:5000/health every 30s
- Build tested: docker build -t tool66-ai . succeeds in 42s

## requirements.txt - Pinned Versions
- flask==3.0.3
- groq==0.9.0
- flask-limiter==3.7.0
- redis==5.0.7
- python-dotenv==1.0.1
- sentence-transformers==3.0.1
- chromadb==0.5.3
- pytest==8.2.2
- pytest-mock==3.14.0
- requests==2.32.3
- bleach==6.1.0

## .env.example
- GROQ_API_KEY, REDIS_URL, AI_PORT, FLASK_DEBUG
- POSTGRES_*, JWT_*, MAIL_* for full stack
- Confirmed: .env is in .gitignore

