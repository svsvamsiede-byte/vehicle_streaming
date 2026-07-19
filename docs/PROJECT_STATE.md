# Project Information

| Field | Value |
|-------|-------|
| Project Name | Production-Grade Streaming Lakehouse |
| Version | 0.1.0 |
| Current Phase | Infrastructure Foundation |
| Current Milestone | M1 — Infrastructure Foundation |
| Overall Progress | 1% |
| Start Date | — |
| Last Updated | 2026-07-19 |

# Project Status Summary

| Field | Value |
|-------|-------|
| Current milestone | M1 — Infrastructure Foundation |
| Current epic | M1-E1 — Project Bootstrap |
| Current task | M1-E1-T01 — Create `.env` Environment File |
| Next task | M1-E1-T02 — Create `docker-compose.yml` Base Services |
| Overall completion percentage | 1% |
| Estimated milestones remaining | 8 |

# Milestone Status

| Milestone | Status | Progress | Notes |
|-----------|--------|----------|-------|
| M1 — Infrastructure Foundation | NOT_STARTED | 0% | All base services start cleanly via Docker Compose |
| M2 — Data Ingestion Layer | NOT_STARTED | 0% | Continuous vehicle telemetry flows into Kafka |
| M3 — Stream Processing Core | NOT_STARTED | 0% | Flink consumes, deserializes, and assigns event time |
| M4 — Advanced Stream Processing | NOT_STARTED | 0% | Windows, state, and alerts are operational |
| M5 — Data Sink & Lakehouse | NOT_STARTED | 0% | Iceberg tables populated with exactly-once guarantees |
| M6 — Analytics & Observability | NOT_STARTED | 0% | Trino queries and Grafana dashboards are live |
| M7 — Production Hardening | NOT_STARTED | 0% | Tests, docs, checkpointing, and recovery verified |
| M8 — Future Enhancements | NOT_STARTED | 0% | Roadmap documented for advanced features |

# Epic Status

| Epic | Status | Progress | Current Task |
|------|--------|----------|--------------|
| M1-E1 — Project Bootstrap | NOT_STARTED | 0% | M1-E1-T01 |
| M1-E2 — Kafka Infrastructure | NOT_STARTED | 0% | — |
| M1-E3 — Storage Layer | NOT_STARTED | 0% | — |
| M1-E4 — Flink Infrastructure | NOT_STARTED | 0% | — |
| M1-E5 — Monitoring Stack | NOT_STARTED | 0% | — |
| M2-E1 — Vehicle Simulator | NOT_STARTED | 0% | — |
| M2-E2 — Kafka Topics & Schemas | NOT_STARTED | 0% | — |
| M2-E3 — Producer Deployment | NOT_STARTED | 0% | — |
| M3-E1 — Flink Job Skeleton | NOT_STARTED | 0% | — |
| M3-E2 — Event Time & Watermarks | NOT_STARTED | 0% | — |
| M3-E3 — Data Validation & DLQ | NOT_STARTED | 0% | — |
| M4-E1 — Windowing | NOT_STARTED | 0% | — |
| M4-E2 — Stateful Processing | NOT_STARTED | 0% | — |
| M4-E3 — Alerting Engine | NOT_STARTED | 0% | — |
| M5-E1 — Iceberg Integration | NOT_STARTED | 0% | — |
| M5-E2 — Exactly-Once Semantics | NOT_STARTED | 0% | — |
| M5-E3 — Iceberg Advanced Features | NOT_STARTED | 0% | — |
| M6-E1 — Trino SQL Analytics | NOT_STARTED | 0% | — |
| M6-E2 — Grafana Dashboards | NOT_STARTED | 0% | — |
| M6-E3 — Operational Monitoring | NOT_STARTED | 0% | — |
| M7-E1 — Checkpointing & Recovery | NOT_STARTED | 0% | — |
| M7-E2 — Failure Recovery Demo | NOT_STARTED | 0% | — |
| M7-E3 — Testing & Documentation | NOT_STARTED | 0% | — |
| M8-E1 — Advanced Features | NOT_STARTED | 0% | — |
| M8-E2 — Cloud Migration Path | NOT_STARTED | 0% | — |

# Atomic Task Tracker

| Task ID | Task Name | Milestone | Epic | Status | Dependencies | Expected Files | Git Commit | Branch | Notes |
|---------|-----------|-----------|------|--------|--------------|----------------|------------|--------|-------|
| M1-E1-T01 | Create `.env` Environment File | M1 | IN_PROGRESS | 5% | NOT_STARTED | None | `.env` | - | main | — |
| M1-E1-T02 | Create `docker-compose.yml` Base Services | M1 | M1-E1 | IN_PROGRESS | 25% | M1-E1-T01 | M1-E1-T02 | - | main | — |
| M1-E1-T03 | Create Project README | M1 | M1-E1 | NOT_STARTED | None | `README.md` | - | main | — |
| M1-E1-T04 | Initialize Repository Directory Layout | M1 | M1-E1 | NOT_STARTED | None | Directory tree | - | main | — |
| M1-E2-T01 | Configure Zookeeper Service | M1 | M1-E2 | NOT_STARTED | 0% | M1-E1-T02 | M1-E2-T01 | - | main | — |
| M1-E2-T02 | Configure Kafka Broker Service | M1 | M1-E2 | NOT_STARTED | M1-E2-T01 | `docker-compose.yml` (edited) | - | main | — |
| M1-E2-T03 | Configure Kafka UI Service | M1 | M1-E2 | NOT_STARTED | M1-E2-T02 | `docker-compose.yml` (edited) | - | main | — |
| M1-E2-T04 | Create Kafka Topic Initialization Script | M1 | M1-E2 | NOT_STARTED | M1-E2-T02 | `scripts/create_topics.py` | - | main | — |
| M1-E3-T01 | Configure MinIO Service | M1 | M1-E3 | NOT_STARTED | 0% | M1-E1-T02 | M1-E3-T01 | - | main | — |
| M1-E3-T02 | Configure Iceberg REST Catalog Service | M1 | M1-E3 | NOT_STARTED | M1-E3-T01 | `docker-compose.yml` (edited) | - | main | — |
| M1-E3-T03 | Create MinIO Bucket Initialization Script | M1 | M1-E3 | NOT_STARTED | M1-E3-T01 | `scripts/init_minio.py` | - | main | — |
| M1-E3-T04 | Create Iceberg Catalog Configuration | M1 | M1-E3 | NOT_STARTED | M1-E3-T02 | `iceberg/catalog/iceberg.properties` | - | main | — |
| M1-E4-T01 | Configure PyFlink JobManager Service | M1 | M1-E4 | NOT_STARTED | 0% | M1-E1-T02 | M1-E4-T01 | - | main | — |
| M1-E4-T02 | Configure PyFlink TaskManager Service | M1 | M1-E4 | NOT_STARTED | M1-E4-T01 | `docker-compose.yml` (edited) | - | main | — |
| M1-E4-T03 | Create `flink-conf.yaml` | M1 | M1-E4 | NOT_STARTED | M1-E4-T01 | `flink/conf/flink-conf.yaml` | - | main | — |
| M1-E4-T04 | Create Custom Flink Docker Image | M1 | M1-E4 | NOT_STARTED | M1-E4-T01 | `flink/Dockerfile` | - | main | — |
| M1-E5-T01 | Configure Prometheus Service | M1 | M1-E5 | NOT_STARTED | 0% | M1-E1-T02 | M1-E5-T01 | - | main | — |
| M1-E5-T02 | Create Prometheus Configuration | M1 | M1-E5 | NOT_STARTED | M1-E5-T01 | `prometheus/prometheus.yml` | - | main | — |
| M1-E5-T03 | Configure Grafana Service | M1 | M1-E5 | NOT_STARTED | M1-E5-T01 | `docker-compose.yml` (edited) | - | main | — |
| M1-E5-T04 | Create Grafana Prometheus Datasource | M1 | M1-E5 | NOT_STARTED | M1-E5-T03 | `grafana/provisioning/datasources/prometheus.yml` | - | main | — |
| M2-E1-T01 | Create Simulator Configuration Module | M2 | NOT_STARTED | 0% | NOT_STARTED | M1-E2-T02 | `producer/config.py` | - | main | — |
| M2-E1-T02 | Create Vehicle Data Models | M2 | M2-E1 | NOT_STARTED | 0% | M2-E1-T01 | M2-E1-T01 | - | main | — |
| M2-E1-T03 | Create Telemetry Generator Core | M2 | M2-E1 | NOT_STARTED | M2-E1-T02 | `producer/simulator.py` | - | main | — |
| M2-E1-T04 | Create Kafka Producer Client | M2 | M2-E1 | NOT_STARTED | M2-E1-T03, M1-E2-T02 | `producer/kafka_client.py` | - | main | — |
| M2-E1-T05 | Create Simulator Entry Point | M2 | M2-E1 | NOT_STARTED | M2-E1-T04 | `producer/main.py` | - | main | — |
| M2-E1-T06 | Create Producer Requirements and Dockerfile | M2 | M2-E1 | NOT_STARTED | M2-E1-T05 | `producer/requirements.txt`, `producer/Dockerfile` | - | main | — |
| M2-E2-T01 | Implement Topic Creation Script | M2 | M2-E2 | NOT_STARTED | 0% | M1-E2-T04 | M2-E2-T01 | - | main | — |
| M2-E2-T02 | Create JSON Schema Definitions | M2 | M2-E2 | NOT_STARTED | M2-E1-T02 | `producer/schemas/telemetry.json`, `producer/schemas/alert.json` | - | main | — |
| M2-E2-T03 | Configure Confluent Schema Registry | M2 | M2-E2 | NOT_STARTED | M2-E2-T01 | `docker-compose.yml` (edited) | - | main | Optional |
| M2-E3-T01 | Add Simulator to Docker Compose | M2 | M2-E3 | NOT_STARTED | 0% | M2-E1-T06, M2-E2-T01 | M2-E3-T01 | - | main | — |
| M2-E3-T02 | Add Health Check Endpoint | M2 | M2-E3 | NOT_STARTED | M2-E3-T01 | `docker-compose.yml` (edited) | - | main | — |
| M3-E1-T01 | Create Flink Job Entry Point | M3 | NOT_STARTED | 0% | NOT_STARTED | M1-E4-T04 | `flink/main.py` | - | main | — |
| M3-E1-T02 | Create Flink Requirements File | M3 | M3-E1 | NOT_STARTED | 0% | M1-E4-T04 | M3-E1-T01 | - | main | — |
| M3-E1-T03 | Create Kafka Source Connector | M3 | M3-E1 | NOT_STARTED | M3-E1-T01 | `flink/kafka_source.py` | - | main | — |
| M3-E1-T04 | Add Flink Job to Docker Compose | M3 | M3-E1 | NOT_STARTED | M3-E1-T01 | `docker-compose.yml` (edited) | - | main | — |
| M3-E2-T01 | Create Timestamp Assigner | M3 | M3-E2 | NOT_STARTED | 0% | M3-E1-T03 | M3-E2-T01 | - | main | — |
| M3-E2-T02 | Create Watermark Strategy | M3 | M3-E2 | NOT_STARTED | M3-E2-T01 | `flink/watermarks.py` | - | main | — |
| M3-E2-T03 | Integrate Watermarks into Pipeline | M3 | M3-E2 | NOT_STARTED | M3-E2-T02 | `flink/main.py` (edited) | - | main | — |
| M3-E3-T01 | Create Validation Rules Engine | M3 | M3-E3 | NOT_STARTED | 0% | M3-E1-T03 | M3-E3-T01 | - | main | — |
| M3-E3-T02 | Create Dead Letter Queue Sink | M3 | M3-E3 | NOT_STARTED | M3-E3-T01 | `flink/dead_letter.py` | - | main | — |
| M3-E3-T03 | Create Data Quality Metrics | M3 | M3-E3 | NOT_STARTED | M3-E3-T02 | `flink/validation.py` (edited) or `flink/metrics.py` | - | main | — |
| M4-E1-T01 | Create Tumbling Window Processor | M4 | NOT_STARTED | 0% | NOT_STARTED | M3-E2-T03 | `flink/windows.py` | - | main | — |
| M4-E1-T02 | Create Sliding Window Processor | M4 | M4-E1 | NOT_STARTED | 0% | M4-E1-T01 | M4-E1-T01 | - | main | — |
| M4-E1-T03 | Create Session Window Processor | M4 | M4-E1 | NOT_STARTED | M4-E1-T02 | `flink/windows.py` (edited) | - | main | — |
| M4-E1-T04 | Create Windowed Aggregation Functions | M4 | M4-E1 | NOT_STARTED | M4-E1-T01 | `flink/aggregations.py` | - | main | — |
| M4-E2-T01 | Create State Backend Configuration | M4 | M4-E2 | NOT_STARTED | 0% | M1-E4-T03 | M4-E2-T01 | - | main | — |
| M4-E2-T02 | Create GPS Distance Calculator | M4 | M4-E2 | NOT_STARTED | M4-E2-T01, M3-E2-T03 | `flink/state.py` | - | main | — |
| M4-E2-T03 | Create Vehicle Online/Offline Detector | M4 | M4-E2 | NOT_STARTED | M4-E2-T02 | `flink/state.py` (edited) | - | main | — |
| M4-E2-T04 | Create Trip State Manager | M4 | M4-E2 | NOT_STARTED | M4-E2-T03 | `flink/state.py` (edited) | - | main | — |
| M4-E3-T01 | Create Alert Rules Configuration | M4 | M4-E3 | NOT_STARTED | 0% | M3-E3-T01 | M4-E3-T01 | - | main | — |
| M4-E3-T02 | Create Alert Publisher | M4 | M4-E3 | NOT_STARTED | M4-E3-T01 | `flink/alerts.py` (edited) | - | main | — |
| M4-E3-T03 | Create Alert Severity Classifier | M4 | M4-E3 | NOT_STARTED | M4-E3-T02 | `flink/alerts.py` (edited) | - | main | — |
| M5-E1-T01 | Create Iceberg Table Definitions | M5 | NOT_STARTED | 0% | NOT_STARTED | M1-E3-T04 | `iceberg/sql/create_tables.sql` | - | main | — |
| M5-E1-T02 | Create Flink Iceberg Sink Configuration | M5 | M5-E1 | NOT_STARTED | 0% | M5-E1-T01, M1-E4-T04 | M5-E1-T01 | - | main | — |
| M5-E1-T03 | Create Vehicle Events Iceberg Sink | M5 | M5-E1 | NOT_STARTED | M5-E1-T02 | `flink/main.py` (edited) | - | main | — |
| M5-E1-T04 | Create Vehicle Alerts Iceberg Sink | M5 | M5-E1 | NOT_STARTED | M5-E1-T03, M4-E3-T02 | `flink/main.py` (edited) | - | main | — |
| M5-E2-T01 | Configure Flink Checkpointing | M5 | M5-E2 | NOT_STARTED | 0% | M3-E1-T01 | M5-E2-T01 | - | main | — |
| M5-E2-T02 | Configure Kafka Transactional Producer | M5 | M5-E2 | NOT_STARTED | M5-E2-T01 | `flink/kafka_sink.py` | - | main | — |
| M5-E2-T03 | Configure Iceberg Exactly-Once Sink | M5 | M5-E2 | NOT_STARTED | M5-E2-T02 | `flink/iceberg_sink.py` (edited) | - | main | — |
| M5-E2-T04 | Create Exactly-Once Verification Test | M5 | M5-E2 | NOT_STARTED | M5-E2-T03 | `tests/integration/test_exactly_once.py` | - | main | — |
| M5-E3-T01 | Create Schema Evolution Script | M5 | M5-E3 | NOT_STARTED | 0% | M5-E1-T01 | M5-E3-T01 | - | main | — |
| M5-E3-T02 | Create Time Travel Query Examples | M5 | M5-E3 | NOT_STARTED | M5-E1-T01 | `iceberg/sql/time_travel.sql` | - | main | — |
| M5-E3-T03 | Create Compaction Script | M5 | M5-E3 | NOT_STARTED | M5-E1-T01 | `iceberg/sql/compaction.sql` | - | main | — |
| M5-E3-T04 | Create Partition Evolution Script | M5 | M5-E3 | NOT_STARTED | M5-E3-T01 | `iceberg/sql/partition_evolution.sql` | - | main | — |
| M6-E1-T01 | Configure Trino Service | M6 | NOT_STARTED | 0% | NOT_STARTED | M1-E3-T02 | `docker-compose.yml` (edited) | - | main | — |
| M6-E1-T02 | Create Trino Iceberg Catalog Configuration | M6 | M6-E1 | NOT_STARTED | 0% | M6-E1-T01 | M6-E1-T01 | - | main | — |
| M6-E1-T03 | Create Analytics Queries | M6 | M6-E1 | NOT_STARTED | M6-E1-T02 | `iceberg/sql/queries.sql` | - | main | — |
| M6-E1-T04 | Create Trino View Definitions | M6 | M6-E1 | NOT_STARTED | M6-E1-T03 | `iceberg/sql/views.sql` | - | main | — |
| M6-E2-T01 | Create Pipeline Metrics Dashboard | M6 | M6-E2 | NOT_STARTED | 0% | M1-E5-T04 | M6-E2-T01 | - | main | — |
| M6-E2-T02 | Create Business Metrics Dashboard | M6 | M6-E2 | NOT_STARTED | M6-E1-T04 | `grafana/dashboards/business_metrics.json` | - | main | — |
| M6-E2-T03 | Create Alerting Dashboard | M6 | M6-E2 | NOT_STARTED | M6-E2-T02 | `grafana/dashboards/alert_monitor.json` | - | main | — |
| M6-E2-T04 | Create Dashboard Provisioning Config | M6 | M6-E2 | NOT_STARTED | M6-E2-T01 | `grafana/provisioning/dashboards/dashboards.yml` | - | main | — |
| M6-E3-T01 | Configure Flink Metrics Reporter | M6 | M6-E3 | NOT_STARTED | 0% | M1-E5-T02 | M6-E3-T01 | - | main | — |
| M6-E3-T02 | Create Prometheus Recording Rules | M6 | M6-E3 | NOT_STARTED | M6-E3-T01 | `prometheus/recording_rules.yml` | - | main | — |
| M6-E3-T03 | Create Prometheus Alert Rules | M6 | M6-E3 | NOT_STARTED | M6-E3-T02 | `prometheus/alert_rules.yml` | - | main | — |
| M7-E1-T01 | Configure Incremental Checkpoints | M7 | NOT_STARTED | 0% | NOT_STARTED | M5-E2-T01 | `flink/conf/flink-conf.yaml` (edited) | - | main | — |
| M7-E1-T02 | Create Savepoint Management Script | M7 | M7-E1 | NOT_STARTED | 0% | M7-E1-T01 | M7-E1-T01 | - | main | — |
| M7-E1-T03 | Configure State TTL | M7 | M7-E1 | NOT_STARTED | M4-E2-T04 | `flink/state.py` (edited) | - | main | — |
| M7-E2-T01 | Create Chaos Test Script | M7 | M7-E2 | NOT_STARTED | 0% | M7-E1-T02 | M7-E2-T01 | - | main | — |
| M7-E2-T02 | Create Recovery Verification Script | M7 | M7-E2 | NOT_STARTED | M7-E2-T01 | `tests/chaos/verify_integrity.py` | - | main | — |
| M7-E2-T03 | Create Failure Scenario Documentation | M7 | M7-E2 | NOT_STARTED | M7-E2-T02 | `docs/failure_scenarios.md` | - | main | — |
| M7-E3-T01 | Create Simulator Unit Tests | M7 | M7-E3 | NOT_STARTED | 0% | M2-E1-T06 | M7-E3-T01 | - | main | — |
| M7-E3-T02 | Create Validation Unit Tests | M7 | M7-E3 | NOT_STARTED | M3-E3-T01 | `tests/unit/test_validation.py` | - | main | — |
| M7-E3-T03 | Create Integration Tests | M7 | M7-E3 | NOT_STARTED | M5-E1-T04 | `tests/integration/test_pipeline.py` | - | main | — |
| M7-E3-T04 | Create Smoke Tests | M7 | M7-E3 | NOT_STARTED | M6-E1-T01 | `tests/smoke/test_end_to_end.py` | - | main | — |
| M7-E3-T05 | Create Architecture Documentation | M7 | M7-E3 | NOT_STARTED | All previous milestones | `docs/architecture.md` | - | main | — |
| M7-E3-T06 | Create Operations Runbook | M7 | M7-E3 | NOT_STARTED | M7-E3-T05 | `docs/operations.md` | - | main | — |
| M8-E1-T01 | Document Vehicle Routes Feature | M8 | NOT_STARTED | 0% | NOT_STARTED | None | `docs/rfc/vehicle_routes.md` | - | main | — |
| M8-E1-T02 | Document REST API Feature | M8 | M8-E1 | NOT_STARTED | 0% | None | M8-E1-T01 | - | main | — |
| M8-E1-T03 | Document Multi-Topic Ingestion | M8 | M8-E1 | NOT_STARTED | None | `docs/rfc/multi_topic.md` | - | main | — |
| M8-E1-T04 | Document AI Extension | M8 | M8-E1 | NOT_STARTED | None | `docs/rfc/ai_extension.md` | - | main | — |
| M8-E2-T01 | Create Cloud Architecture Comparison | M8 | M8-E2 | NOT_STARTED | 0% | None | M8-E2-T01 | - | main | — |
| M8-E2-T02 | Create Terraform Module Outline | M8 | M8-E2 | NOT_STARTED | M8-E2-T01 | `terraform/main.tf`, `terraform/variables.tf`, `terraform/outputs.tf` | - | main | — |
| M8-E2-T03 | Create Kubernetes Deployment Outline | M8 | M8-E2 | NOT_STARTED | M8-E2-T01 | `k8s/flink-deployment.yml`, `k8s/simulator-deployment.yml` | - | main | — |

# Current Working Context

| Field | Value |
|-------|-------|
| Current milestone | M1 — Infrastructure Foundation |
| Current epic | M1-E1 — Project Bootstrap |
| Current task | M1-E1-T01 — Create `.env` Environment File |
| Task description | Define all environment variables used across the Docker Compose stack including Kafka, MinIO, Flink, and Trino credentials, ports, and memory limits. All services reference variables from `.env`. No hardcoded secrets in `docker-compose.yml`. `source .env && echo $KAFKA_PORT` returns expected value. |
| Expected files | `.env` |
| Acceptance criteria | All services reference variables from `.env`; No hardcoded secrets in `docker-compose.yml`; `source .env && echo $KAFKA_PORT` returns expected value |
| Dependencies | None |

# Completed Tasks

No completed tasks.

# Architecture Decisions

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

# Technical Debt

No technical debt recorded.

# Known Issues

No known issues.

# Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Docker Compose memory exhaustion on local machines | Medium | High | Document minimum RAM requirements (8GB+); provide resource-limit guidance |
| PyFlink connector JAR version incompatibilities | Medium | High | Pin exact Flink, Kafka, and Iceberg versions; validate JARs in Dockerfile build |
| Kafka advertised listeners misconfiguration causing external connectivity issues | Medium | Medium | Test both internal and external listeners; document port mapping |
| Iceberg REST catalog startup race condition with MinIO | Medium | Medium | Add health checks and depends_on with condition in docker-compose |
| Checkpoint state growth exceeding available disk | Low | High | Monitor state size; enforce TTL policies; document cleanup procedures |
| Late events exceeding watermark bound causing silent drops | Low | Medium | Expose late-event metrics; configure side-output for late data |
| Grafana dashboard provisioning failures on first startup | Low | Low | Verify provisioning paths; add startup health checks |
| Exactly-once semantics complexity causing hidden bugs | Medium | High | Implement dedicated EOS integration test; validate after every checkpoint change |
| Schema evolution breaking downstream consumers | Low | Medium | Follow Iceberg best practices; test schema changes in integration tests |
| Network partition between Flink and Kafka during checkpoint | Low | High | Configure Flink restart strategy; test chaos scenarios |

# Verification Checklist

- [ ] Docker Compose starts
- [ ] Kafka reachable
- [ ] Flink running
- [ ] MinIO running
- [ ] Iceberg catalog healthy
- [ ] Trino healthy
- [ ] Grafana healthy
- [ ] Prometheus healthy
- [ ] Tests passing
- [ ] Lint passing
- [ ] Type checks passing

# Repository Snapshot

```
streaming-lakehouse/
├── .env
├── docker-compose.yml
├── README.md
├── PROJECT_PLAN.md
├── ENGINEERING_ROADMAP.md
├── DEVELOPMENT_RULES.md
├── AI_CONTEXT.md
├── PROJECT_STATE.md
├── producer/
│   ├── config.py
│   ├── schemas.py
│   ├── simulator.py
│   ├── kafka_client.py
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── schemas/
│       ├── telemetry.json
│       └── alert.json
├── flink/
│   ├── main.py
│   ├── requirements.txt
│   ├── kafka_source.py
│   ├── kafka_sink.py
│   ├── timestamps.py
│   ├── watermarks.py
│   ├── validation.py
│   ├── dead_letter.py
│   ├── metrics.py
│   ├── windows.py
│   ├── aggregations.py
│   ├── state.py
│   ├── alerts.py
│   ├── iceberg_sink.py
│   ├── Dockerfile
│   └── conf/
│       └── flink-conf.yaml
├── iceberg/
│   ├── catalog/
│   │   └── iceberg.properties
│   ├── warehouse/
│   └── sql/
│       ├── create_tables.sql
│       ├── queries.sql
│       ├── views.sql
│       ├── schema_evolution.sql
│       ├── time_travel.sql
│       ├── compaction.sql
│       └── partition_evolution.sql
├── trino/
│   └── catalog/
│       └── iceberg.properties
├── grafana/
│   ├── dashboards/
│   │   ├── pipeline_metrics.json
│   │   ├── business_metrics.json
│   │   └── alert_monitor.json
│   └── provisioning/
│       ├── datasources/
│       │   └── prometheus.yml
│       └── dashboards/
│           └── dashboards.yml
├── prometheus/
│   ├── prometheus.yml
│   ├── recording_rules.yml
│   └── alert_rules.yml
├── scripts/
│   ├── create_topics.py
│   ├── init_minio.py
│   └── savepoint_manager.py
├── tests/
│   ├── unit/
│   │   ├── test_simulator.py
│   │   ├── test_validation.py
│   │   ├── test_aggregations.py
│   │   ├── test_alerts.py
│   │   └── test_config.py
│   ├── integration/
│   │   ├── test_pipeline.py
│   │   ├── test_iceberg_sink.py
│   │   ├── test_exactly_once.py
│   │   └── test_trino.py
│   ├── smoke/
│   │   ├── test_end_to_end.py
│   │   ├── test_ports.py
│   │   └── test_queries.py
│   ├── perf/
│   │   ├── test_throughput.py
│   │   ├── test_latency.py
│   │   └── test_checkpoint.py
│   └── chaos/
│       ├── test_recovery.py
│       └── verify_integrity.py
├── docs/
│   ├── architecture.md
│   ├── operations.md
│   ├── failure_scenarios.md
│   ├── cloud_migration.md
│   └── rfc/
│       ├── vehicle_routes.md
│       ├── rest_api.md
│       ├── multi_topic.md
│       └── ai_extension.md
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── k8s/
    ├── flink-deployment.yml
    └── simulator-deployment.yml
```

# Git History

No commits recorded.

# Session Notes

No development sessions completed.

# Next AI Prompt Context

**Current milestone:** M1 — Infrastructure Foundation

**Current task:** M1-E1-T01 — Create `.env` Environment File

**Expected files:** `.env`

**Constraints:** All services must reference variables from `.env`. No hardcoded secrets in `docker-compose.yml`. Use standard `.env` format (KEY=VALUE). Include comments explaining each variable. No quotes around values unless necessary. Variables must cover: Kafka (broker port, internal port, UI port), Zookeeper (port), MinIO (API port, console port, root user, root password), Iceberg Catalog (port, warehouse path), Flink (JobManager port, TaskManager slots, parallelism), Trino (port), Grafana (port, admin user, admin password), Prometheus (port), Simulator (TPS, vehicle count, duplicate probability, out-of-order probability).

**Important architectural decisions:** Docker Compose is the sole orchestration layer. All configuration is externalized to `.env`. No cloud dependencies. Services communicate over a shared Docker bridge network. Kafka uses advertised listeners for internal and external access.
