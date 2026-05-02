# Day 11 - Sentence Transformers Pre-load + ZAP Active Scan

## Sentence Transformers
- Added services/knowledge_base.py
- Model: all-MiniLM-L6-v2 (384 dims, fast, lightweight)
- Pre-loaded at startup inside create_app() to avoid first-request latency
- ChromaDB collection: 'operational_risk_knowledge'
- Pre-load time: ~3.2s at startup (acceptable)

## ZAP Active Scan
- Full active scan run against http://localhost:5000
- Critical findings: 0
- High findings: 0
- Medium findings: 0 (all resolved Day 8)
- Low: Server header disclosure (accepted risk)
- ZAP report exported to docs/zap_report_day11.html

