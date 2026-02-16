# SYSTEM BLUEPRINT

## Layers

1. Foundation (Docker + Network + Observability)
2. Mesh Layer (Router + NATS + Memory)
3. Governance Layer (TAP Policy Engine)
4. Agent Layer (Ingestion, AutoML, Sandbox)
5. Control Plane (PWA Dashboard)
6. Hybrid Mirror (GCP Cloud Run)

## Authority Model

Local Node = Primary Authority  
Cloud Mirror = Stateless Execution Layer  

## Mesh Fabric

Event Backbone: NATS  
Vector Store: Qdrant  
Cache: Redis  
LLM: Ollama (host)  

## Security

- No mutation without TAP validation
- Full audit trail
- Deterministic rehydrate
- Kill switch enforced
