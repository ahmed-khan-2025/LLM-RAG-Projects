from prometheus_client import Counter, Histogram, Gauge

GENERATIONS=Counter('ai_generation_total','Total generation requests',['model','provider','brand'])
FAILURES=Counter('ai_generation_failures_total','Failed generation requests',['model','provider'])
LATENCY=Histogram('ai_generation_latency_seconds','Generation latency',['model','provider'])
SAFETY=Counter('ai_generation_safety_failures_total','Safety or brand guardrail failures',['brand'])
QUALITY=Histogram('ai_generation_quality_score','Quality score',['brand'])
COST=Counter('ai_generation_estimated_cost_usd_total','Estimated generation cost in USD',['model','provider'])
ACTIVE=Gauge('ai_generation_active_requests','Active generation requests')
