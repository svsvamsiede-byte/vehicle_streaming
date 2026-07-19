# Working Context

> Auto-generated from PROJECT_STATE.md

---

## Task

M1-E1-T01 — Create `.env` Environment File

## Acceptance Criteria

All services reference variables from `.env`; No hardcoded secrets in `docker-compose.yml`; `source .env && echo $KAFKA_PORT` returns expected value

## Dependencies

None

## Branch

N/A

## Relevant Files

`.env`

## Relevant Architecture Decisions

| Decision ID | Date | Decision | Reason | Impact |
|-------------|------|----------|--------|--------|
| AD-001 | 2026-07-19 | Kafka before Flink | Events must land in Kafka before Flink consumes them; the simulator is independent of the processor | Decouples ingestion from processing; enables replay |
| AD-002 | 2026-07-19 | Event Time over Processing Time | Timestamps are extracted from payload `timestamp` fields, not wall-clock time, to handle out-of-order and late events correctly | Correct semantics for late and out-of-order data |
| AD-003 | 2026-07-19 | Watermarks | Bounded out-of-orderness of 5 seconds with 30-second idle timeout | Balances latency and correctness |
| AD-004 | 2026-07-19 | Dead Letter Queue | Invalid records are routed to `vehicle.deadletter` rather than dropped, preserving auditability | Preserves invalid data for debugging; prevents silent data loss |
| AD-005 | 2026-07-19 | Exactly-Once Semantics | Enabled via Flink checkpointing, Kafka transactional producers, and Iceberg two-phase commit sink | Guarantees no duplicates and no data loss |
| AD-006 | 2026-07-19 | Iceberg as Lakehouse Format | Chosen for schema evolution, time travel, snapshot isolation, and hidden partitioning without full rewrites | Enables analytics without locking; supports historical queries |
| AD-007 | 2026-07-19 | Docker Compose for Local Deployment | All services containerized for reproducibility; no cloud dependencies | Simplifies onboarding; eliminates cloud costs for development |
| AD-008 | 2026-07-19 | RocksDB State Backend | Supports large state, incremental checkpoints, and local recovery | Enables stateful processing at scale |
| AD-009 | 2026-07-19 | Incremental Checkpointing | Checkpoint interval 30 seconds; incremental to minimize I/O | Reduces checkpoint overhead and storage costs |
| AD-010 | 2026-07-19 | REST Catalog for Iceberg | Provides a standard metadata interface shared by Flink and Trino | Unifies catalog access across compute engines |
| AD-011 | 2026-07-19 | MinIO as Object Storage | S3-compatible API for Iceberg warehouse without cloud lock-in | Cost-free local development; cloud-agnostic design |
| AD-012 | 2026-07-19 | Partitioning Strategy | Time-based partitioning (`days(event_time)`) for all Iceberg tables to optimize time-range queries | Improves query performance for time-series analytics |
| AD-013 | 2026-07-19 | Alert Deduplication | Same rule + vehicle alerts suppressed within a 1-minute window using Flink state | Prevents alert spam and reduces noise |
| AD-014 | 2026-07-19 | State TTL | GPS state 1 hour, alert dedup state 10 minutes, trip state 24 hours | Prevents unbounded state growth |
| AD-015 | 2026-07-19 | Auto-Provisioning | Grafana datasources and dashboards auto-load from provisioning directories | Eliminates manual setup on every startup |
| AD-016 | 2026-07-19 | Prometheus Reporter | Flink metrics exposed directly to Prometheus without PushGateway | Simplifies metrics pipeline; reduces infrastructure |
