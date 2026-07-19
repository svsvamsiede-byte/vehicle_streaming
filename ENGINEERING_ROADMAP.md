# Production-Grade Streaming Lakehouse
## Executable Engineering Roadmap
### Kafka · PyFlink · Apache Iceberg · MinIO · Trino · Grafana · Prometheus

---

# 1 Project Overview

## Architecture Summary

A containerized, production-inspired streaming data platform that ingests vehicle telemetry from a simulator, processes it in real-time using PyFlink with event-time semantics, persists results into Apache Iceberg tables backed by MinIO S3-compatible storage, and exposes SQL analytics via Trino. Operational health is monitored through Grafana dashboards fed by Prometheus metrics.

## Technologies

| Layer | Technology | Version Target |
|-------|-----------|----------------|
| Language | Python | 3.12 |
| Message Broker | Apache Kafka | 7.5+ (Confluent) |
| Stream Processing | Apache Flink (PyFlink) | 1.18+ |
| Lakehouse Format | Apache Iceberg | 1.4+ |
| Object Storage | MinIO | RELEASE.2024+ |
| SQL Analytics | Trino | 432+ |
| Visualization | Grafana | 10.2+ |
| Metrics | Prometheus | 2.47+ |
| Orchestration | Docker Compose | v2+ |

## Objectives

1. Demonstrate end-to-end stream processing with event-time watermarks and windowing
2. Implement exactly-once semantics from Kafka → Flink → Iceberg
3. Showcase stateful processing with fault-tolerant checkpointing
4. Provide production-grade data validation with dead-letter queues
5. Enable time-travel analytics and schema evolution via Iceberg
6. Deliver operational observability through metrics and dashboards
7. Prove failure recovery without data loss or duplication

## Expected Deliverables

- `docker-compose.yml` — complete local infrastructure
- `producer/` — vehicle telemetry simulator
- `flink/` — PyFlink stream processing application
- `iceberg/sql/` — table definitions and analytics queries
- `grafana/` — dashboard provisioning and JSON models
- `prometheus/` — scrape configuration and recording rules
- `tests/` — unit, integration, smoke, and chaos tests
- `docs/` — architecture diagrams and operations runbooks

---

# 2 Milestones

| ID | Milestone | Goal | Est. Duration |
|----|-----------|------|---------------|
| M1 | Infrastructure Foundation | All base services start cleanly via Docker Compose | 2 days |
| M2 | Data Ingestion Layer | Continuous vehicle telemetry flows into Kafka | 2 days |
| M3 | Stream Processing Core | Flink consumes, deserializes, and assigns event time | 2 days |
| M4 | Advanced Stream Processing | Windows, state, and alerts are operational | 3 days |
| M5 | Data Sink & Lakehouse | Iceberg tables populated with exactly-once guarantees | 3 days |
| M6 | Analytics & Observability | Trino queries and Grafana dashboards are live | 2 days |
| M7 | Production Hardening | Tests, docs, checkpointing, and recovery verified | 3 days |
| M8 | Future Enhancements | Roadmap documented for advanced features | 1 day |

---

# 3 Epics

## Milestone 1 — Infrastructure Foundation

| Epic ID | Name | Description |
|---------|------|-------------|
| M1-E1 | Project Bootstrap | Repository structure, environment configuration, and documentation |
| M1-E2 | Kafka Infrastructure | Broker, Zookeeper, and Kafka UI services |
| M1-E3 | Storage Layer | MinIO buckets and Iceberg REST catalog |
| M1-E4 | Flink Infrastructure | PyFlink JobManager and TaskManager |
| M1-E5 | Monitoring Stack | Prometheus and Grafana with auto-provisioning |

## Milestone 2 — Data Ingestion Layer

| Epic ID | Name | Description |
|---------|------|-------------|
| M2-E1 | Vehicle Simulator | Configurable telemetry generator with realistic data |
| M2-E2 | Kafka Topics & Schemas | Topic creation and Avro/JSON schema contracts |
| M2-E3 | Producer Deployment | Containerized simulator integrated into Compose |

## Milestone 3 — Stream Processing Core

| Epic ID | Name | Description |
|---------|------|-------------|
| M3-E1 | Flink Job Skeleton | Entry point, environment, and Kafka source |
| M3-E2 | Event Time & Watermarks | Timestamp extraction and watermark strategies |
| M3-E3 | Data Validation & DLQ | Schema validation and dead-letter routing |

## Milestone 4 — Advanced Stream Processing

| Epic ID | Name | Description |
|---------|------|-------------|
| M4-E1 | Windowing | Tumbling, sliding, and session window aggregations |
| M4-E2 | Stateful Processing | GPS tracking, trip detection, and vehicle state |
| M4-E3 | Alerting Engine | Real-time rule evaluation and alert publication |

## Milestone 5 — Data Sink & Lakehouse

| Epic ID | Name | Description |
|---------|------|-------------|
| M5-E1 | Iceberg Integration | Flink Iceberg sink and table definitions |
| M5-E2 | Exactly-Once Semantics | Transactional Kafka producer and Iceberg sink |
| M5-E3 | Iceberg Advanced Features | Schema evolution, time travel, and compaction |

## Milestone 6 — Analytics & Observability

| Epic ID | Name | Description |
|---------|------|-------------|
| M6-E1 | Trino SQL Analytics | Trino catalog configuration and analytics queries |
| M6-E2 | Grafana Dashboards | Pipeline, business, and alerting dashboards |
| M6-E3 | Operational Monitoring | Flink metrics, Prometheus rules, and health checks |

## Milestone 7 — Production Hardening

| Epic ID | Name | Description |
|---------|------|-------------|
| M7-E1 | Checkpointing & Recovery | Incremental checkpoints and savepoint management |
| M7-E2 | Failure Recovery Demo | Chaos tests and recovery verification |
| M7-E3 | Testing & Documentation | Unit tests, integration tests, and operations docs |

## Milestone 8 — Future Enhancements

| Epic ID | Name | Description |
|---------|------|-------------|
| M8-E1 | Advanced Features | Vehicle routes, REST API, multi-topic ingestion, AI |
| M8-E2 | Cloud Migration Path | Kubernetes, Terraform, and CI/CD outlines |

---

# 4 Atomic Tasks

---

## Milestone 1 — Infrastructure Foundation

### Epic M1-E1: Project Bootstrap

#### M1-E1-T01: Create Root Environment Configuration
- **Task Name:** Create `.env` Environment File
- **Description:** Define all environment variables used across the Docker Compose stack including Kafka, MinIO, Flink, and Trino credentials, ports, and memory limits.
- **Expected Files:** `.env`
- **Dependencies:** None
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - All services reference variables from `.env`
  - No hardcoded secrets in `docker-compose.yml`
  - `source .env && echo $KAFKA_PORT` returns expected value

#### M1-E1-T02: Create Docker Compose Base Infrastructure
- **Task Name:** Create `docker-compose.yml` Base Services
- **Description:** Define Zookeeper, Kafka Broker, and Kafka UI services with health checks, volume mounts, and network configuration.
- **Expected Files:** `docker-compose.yml`
- **Dependencies:** M1-E1-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - `docker compose up -d zookeeper kafka kafka-ui` starts successfully
  - Kafka UI accessible at `http://localhost:8080`
  - `docker compose ps` shows all three services healthy

#### M1-E1-T03: Create Project README
- **Task Name:** Create `README.md`
- **Description:** Project overview, quick-start instructions, architecture diagram placeholder, and tech stack summary.
- **Expected Files:** `README.md`
- **Dependencies:** None
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - README renders correctly on GitHub
  - Contains quick-start command: `docker compose up -d`
  - Lists all exposed ports

#### M1-E1-T04: Create Folder Structure
- **Task Name:** Initialize Repository Directory Layout
- **Description:** Create all directories defined in the project plan: `producer/`, `flink/`, `iceberg/catalog/`, `iceberg/warehouse/`, `iceberg/sql/`, `grafana/dashboards/`, `grafana/provisioning/`, `prometheus/`, `tests/unit/`, `tests/integration/`, `tests/smoke/`, `tests/chaos/`, `docs/`.
- **Expected Files:** Directory tree only (no files)
- **Dependencies:** None
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - `tree -d` shows all expected directories
  - `.gitkeep` files added to empty directories

---

### Epic M1-E2: Kafka Infrastructure

#### M1-E2-T01: Configure Zookeeper Service
- **Task Name:** Define Zookeeper Docker Service
- **Description:** Add Zookeeper service to `docker-compose.yml` with persistent volume, health check, and environment variables from `.env`.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M1-E1-T02
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Zookeeper starts and responds on port 2181
  - Health check passes within 30 seconds

#### M1-E2-T02: Configure Kafka Broker Service
- **Task Name:** Define Kafka Broker Docker Service
- **Description:** Add Kafka broker with KRaft or Zookeeper mode, advertised listeners for internal and external access, auto topic creation disabled, and persistent volume.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M1-E2-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Kafka broker starts and listens on port 9092 (external) and 29092 (internal)
  - `kafka-broker-api-versions.sh --bootstrap-server localhost:9092` succeeds

#### M1-E2-T03: Configure Kafka UI Service
- **Task Name:** Define Kafka UI Docker Service
- **Description:** Add Provectus Kafka UI for topic inspection, message browsing, and consumer group monitoring.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M1-E2-T02
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Kafka UI accessible at `http://localhost:8080`
  - Can view broker and topic list

#### M1-E2-T04: Create Kafka Topic Initialization Script
- **Task Name:** Create Topic Bootstrap Script
- **Description:** Python script that creates `vehicle.telemetry`, `vehicle.alerts`, and `vehicle.deadletter` topics with appropriate partition counts and replication factors.
- **Expected Files:** `scripts/create_topics.py`
- **Dependencies:** M1-E2-T02
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Script runs successfully after `docker compose up`
  - All three topics visible in Kafka UI
  - `vehicle.telemetry` has at least 3 partitions

---

### Epic M1-E3: Storage Layer

#### M1-E3-T01: Configure MinIO Service
- **Task Name:** Define MinIO Docker Service
- **Description:** Add MinIO service with S3-compatible API, console UI, persistent volume, and root credentials from `.env`.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M1-E1-T02
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - MinIO API on port 9000 and console on port 9001
  - Can log in to console with credentials from `.env`

#### M1-E3-T02: Configure Iceberg REST Catalog Service
- **Task Name:** Define Iceberg REST Catalog Docker Service
- **Description:** Add Apache Iceberg REST catalog (e.g., using `tabulario/iceberg-rest` or Apache Polaris) connected to MinIO as the warehouse backend.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M1-E3-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - REST catalog responds on configured port
  - `curl http://localhost:8181/v1/config` returns valid JSON

#### M1-E3-T03: Create MinIO Bucket Initialization Script
- **Task Name:** Create MinIO Bucket Bootstrap Script
- **Description:** Python script using `boto3` to create the `iceberg-warehouse` bucket and set appropriate policies.
- **Expected Files:** `scripts/init_minio.py`
- **Dependencies:** M1-E3-T01
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - `iceberg-warehouse` bucket exists in MinIO
  - Bucket is readable/writable

#### M1-E3-T04: Create Iceberg Catalog Configuration
- **Task Name:** Create Iceberg Catalog Config File
- **Description:** YAML/Properties file defining the Iceberg catalog connection URI, warehouse path (s3://iceberg-warehouse), and S3 endpoint override for MinIO.
- **Expected Files:** `iceberg/catalog/iceberg.properties`
- **Dependencies:** M1-E3-T02
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Properties file parsed correctly by REST catalog
  - Warehouse path points to MinIO bucket

---

### Epic M1-E4: Flink Infrastructure

#### M1-E4-T01: Configure PyFlink JobManager Service
- **Task Name:** Define Flink JobManager Docker Service
- **Description:** Add Flink JobManager with RPC, blob server, and UI ports exposed. Use official Flink image with Python support.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M1-E1-T02
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - JobManager UI accessible at `http://localhost:8081`
  - Shows Flink dashboard with no running jobs

#### M1-E4-T02: Configure PyFlink TaskManager Service
- **Task Name:** Define Flink TaskManager Docker Service
- **Description:** Add Flink TaskManager with slots, memory configuration, and connection to JobManager. Scale to 2+ slots.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M1-E4-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - TaskManager registers with JobManager
  - UI shows available task slots > 0

#### M1-E4-T03: Create Flink Configuration File
- **Task Name:** Create `flink-conf.yaml`
- **Description:** Flink configuration including state backend, checkpointing defaults, metrics reporters, and Kafka/Iceberg connector JARs classpath.
- **Expected Files:** `flink/conf/flink-conf.yaml`
- **Dependencies:** M1-E4-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Config mounted into JobManager and TaskManager containers
  - `state.backend` set to `rocksdb`
  - `execution.checkpointing.interval` set to 30s

#### M1-E4-T04: Create Flink Dockerfile
- **Task Name:** Create Custom Flink Docker Image
- **Description:** Dockerfile extending `flink:1.18-scala_2.12-java11` with Python 3.12, PyFlink, and required connector JARs (Kafka, Iceberg) downloaded.
- **Expected Files:** `flink/Dockerfile`
- **Dependencies:** M1-E4-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Image builds successfully
  - `python --version` returns 3.12 inside container
  - Kafka and Iceberg connectors present in `/opt/flink/lib/`

---

### Epic M1-E5: Monitoring Stack

#### M1-E5-T01: Configure Prometheus Service
- **Task Name:** Define Prometheus Docker Service
- **Description:** Add Prometheus service with persistent TSDB volume and configuration mount.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M1-E1-T02
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Prometheus UI accessible at `http://localhost:9090`
  - Shows Prometheus self-metrics

#### M1-E5-T02: Create Prometheus Configuration
- **Task Name:** Create `prometheus.yml`
- **Description:** Scrape configs for Prometheus self-monitoring, Flink metrics (via Prometheus reporter), Kafka (via JMX exporter if available), and MinIO.
- **Expected Files:** `prometheus/prometheus.yml`
- **Dependencies:** M1-E5-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - All targets show as UP in Prometheus UI
  - Flink metrics endpoint reachable

#### M1-E5-T03: Configure Grafana Service
- **Task Name:** Define Grafana Docker Service
- **Description:** Add Grafana with persistent volume, admin credentials from `.env`, and provisioning directories mounted.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M1-E5-T01
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Grafana accessible at `http://localhost:3000`
  - Can log in with admin credentials

#### M1-E5-T04: Create Grafana Datasource Provisioning
- **Task Name:** Create Grafana Prometheus Datasource
- **Description:** YAML file in `grafana/provisioning/datasources/` that auto-configures Prometheus as the default datasource.
- **Expected Files:** `grafana/provisioning/datasources/prometheus.yml`
- **Dependencies:** M1-E5-T03
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Datasource appears in Grafana without manual configuration
  - Test connection succeeds

---

## Milestone 2 — Data Ingestion Layer

### Epic M2-E1: Vehicle Simulator

#### M2-E1-T01: Create Simulator Configuration Module
- **Task Name:** Create `producer/config.py`
- **Description:** Configuration dataclass for simulator settings: vehicle IDs, TPS (transactions per second), delay ranges, duplicate probability, out-of-order probability, and Kafka connection params.
- **Expected Files:** `producer/config.py`
- **Dependencies:** M1-E2-T02
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Config loads from environment variables with sensible defaults
  - All fields have type hints
  - Validation rejects invalid ranges (e.g., negative TPS)

#### M2-E1-T02: Create Vehicle Data Models
- **Task Name:** Create `producer/schemas.py`
- **Description:** Pydantic or dataclass models for vehicle telemetry events including all fields: vehicleId, timestamp, latitude, longitude, speed, rpm, fuel, engineTemp, batteryVoltage, throttlePosition, brakePressure, steeringAngle.
- **Expected Files:** `producer/schemas.py`
- **Dependencies:** M2-E1-T01
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Model serializes to valid JSON
  - All fields have appropriate types and validators
  - Timestamp defaults to UTC now

#### M2-E1-T03: Create Telemetry Generator Core
- **Task Name:** Create `producer/simulator.py`
- **Description:** Core simulation engine that generates realistic telemetry with configurable TPS, random delays, intentional duplicate events, and out-of-order event injection.
- **Expected Files:** `producer/simulator.py`
- **Dependencies:** M2-E1-T02
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Generates events at configured TPS
  - Produces duplicates at configured probability
  - Produces out-of-order events at configured probability
  - GPS coordinates simulate realistic movement patterns

#### M2-E1-T04: Create Kafka Producer Client
- **Task Name:** Create `producer/kafka_client.py`
- **Description:** Kafka producer wrapper using `confluent-kafka` with JSON serialization, delivery callbacks, and graceful shutdown handling.
- **Expected Files:** `producer/kafka_client.py`
- **Dependencies:** M2-E1-T03, M1-E2-T02
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Successfully publishes to `vehicle.telemetry`
  - Handles broker unavailability with retries
  - Logs delivery success/failure

#### M2-E1-T05: Create Simulator Entry Point
- **Task Name:** Create `producer/main.py`
- **Description:** CLI entry point that loads config, initializes simulator and Kafka client, and runs the event generation loop with signal handling for graceful shutdown.
- **Expected Files:** `producer/main.py`
- **Dependencies:** M2-E1-T04
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Runs continuously until SIGINT/SIGTERM
  - Prints startup message with configuration summary
  - Flushes pending messages on shutdown

#### M2-E1-T06: Create Producer Requirements and Dockerfile
- **Task Name:** Create Producer Packaging
- **Description:** `producer/requirements.txt` with pinned dependencies and `producer/Dockerfile` based on Python 3.12 slim.
- **Expected Files:** `producer/requirements.txt`, `producer/Dockerfile`
- **Dependencies:** M2-E1-T05
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Docker image builds successfully
  - Container runs and produces events when started

---

### Epic M2-E2: Kafka Topics & Schemas

#### M2-E2-T01: Implement Topic Creation Script
- **Task Name:** Finalize Topic Definitions
- **Description:** Extend `scripts/create_topics.py` to create topics with specific configs: `vehicle.telemetry` (6 partitions, retention 7 days), `vehicle.alerts` (3 partitions), `vehicle.deadletter` (3 partitions, retention 30 days).
- **Expected Files:** `scripts/create_topics.py` (edited)
- **Dependencies:** M1-E2-T04
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Topics created with correct partition counts
  - Topic configs verified via Kafka AdminClient

#### M2-E2-T02: Create JSON Schema Definitions
- **Task Name:** Create Event Schema JSON Files
- **Description:** JSON Schema files for vehicle telemetry and alert events to serve as documentation and validation reference.
- **Expected Files:** `producer/schemas/telemetry.json`, `producer/schemas/alert.json`
- **Dependencies:** M2-E1-T02
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Schemas validate sample events successfully
  - All required fields marked as required

#### M2-E2-T03: Create Schema Registry Setup (Optional)
- **Task Name:** Configure Confluent Schema Registry
- **Description:** Add Schema Registry service to docker-compose for Avro/JSON schema management.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M2-E2-T01
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Schema Registry accessible on port 8081
  - Schemas can be registered and retrieved

---

### Epic M2-E3: Producer Deployment

#### M2-E3-T01: Add Simulator to Docker Compose
- **Task Name:** Integrate Producer Service
- **Description:** Add `vehicle-simulator` service to `docker-compose.yml` with dependency on Kafka, environment variables from `.env`, and restart policy.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M2-E1-T06, M2-E2-T01
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - `docker compose up vehicle-simulator` starts and produces events
  - Kafka UI shows messages in `vehicle.telemetry`

#### M2-E3-T02: Create Simulator Health Check
- **Task Name:** Add Health Check Endpoint
- **Description:** Simple HTTP health check in simulator or Docker healthcheck command to verify producer is running.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M2-E3-T01
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - `docker compose ps` shows simulator as healthy
  - Health check fails if Kafka is unreachable

---

## Milestone 3 — Stream Processing Core

### Epic M3-E1: Flink Job Skeleton

#### M3-E1-T01: Create Flink Job Entry Point
- **Task Name:** Create `flink/main.py`
- **Description:** PyFlink job entry point that creates StreamExecutionEnvironment, configures checkpointing, sets parallelism, and defines the pipeline topology (source → process → sink placeholders).
- **Expected Files:** `flink/main.py`
- **Dependencies:** M1-E4-T04
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Job submits to Flink JobManager without errors
  - Job graph visible in Flink UI
  - Pipeline has source, process, and sink nodes

#### M3-E1-T02: Create Flink Requirements File
- **Task Name:** Create `flink/requirements.txt`
- **Description:** Pinned Python dependencies: `apache-flink==1.18.*`, `confluent-kafka`, `pyiceberg`, etc.
- **Expected Files:** `flink/requirements.txt`
- **Dependencies:** M1-E4-T04
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - All dependencies install without conflicts
  - `pip check` passes

#### M3-E1-T03: Create Kafka Source Connector
- **Task Name:** Create `flink/kafka_source.py`
- **Description:** Flink Kafka source configuration with consumer group ID, starting offsets, and JSON deserialization schema.
- **Expected Files:** `flink/kafka_source.py`
- **Dependencies:** M3-E1-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Source consumes from `vehicle.telemetry`
  - Consumer group visible in Kafka UI
  - Events flow into Flink job

#### M3-E1-T04: Add Flink Job to Docker Compose
- **Task Name:** Integrate Flink Job Service
- **Description:** Add `flink-job` service to `docker-compose.yml` that submits the PyFlink job on startup, with dependencies on Kafka and Iceberg catalog.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M3-E1-T01
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - `docker compose up flink-job` submits job automatically
  - Job remains in RUNNING state

---

### Epic M3-E2: Event Time & Watermarks

#### M3-E2-T01: Create Timestamp Assigner
- **Task Name:** Create `flink/timestamps.py`
- **Description:** Flink `TimestampAssigner` implementation that extracts event time from the `timestamp` field of vehicle telemetry JSON.
- **Expected Files:** `flink/timestamps.py`
- **Dependencies:** M3-E1-T03
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Event timestamps extracted correctly from JSON
  - Handles malformed timestamps with fallback

#### M3-E2-T02: Create Watermark Strategy
- **Task Name:** Create `flink/watermarks.py`
- **Description:** Watermark strategy with bounded out-of-orderness (e.g., 5 seconds), idle timeout, and alignment for multiple sources.
- **Expected Files:** `flink/watermarks.py`
- **Dependencies:** M3-E2-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Watermarks generated at expected interval
  - Late events identified and counted
  - Flink UI shows watermark progress

#### M3-E2-T03: Integrate Watermarks into Pipeline
- **Task Name:** Wire Watermarks to Kafka Source
- **Description:** Update `flink/main.py` to assign timestamps and watermarks to the Kafka source stream.
- **Expected Files:** `flink/main.py` (edited)
- **Dependencies:** M3-E2-T02
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Pipeline uses event time processing
  - Watermark metrics visible in Flink UI

---

### Epic M3-E3: Data Validation & DLQ

#### M3-E3-T01: Create Validation Rules Engine
- **Task Name:** Create `flink/validation.py`
- **Description:** Validation functions for: non-negative speed, valid timestamp (not in future, not too old), non-null vehicleId, valid GPS coordinates (lat -90 to 90, lon -180 to 180).
- **Expected Files:** `flink/validation.py`
- **Dependencies:** M3-E1-T03
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Each rule correctly identifies invalid records
  - Rules are composable
  - Returns structured validation result with error code

#### M3-E3-T02: Create Dead Letter Queue Sink
- **Task Name:** Create `flink/dead_letter.py`
- **Description:** Kafka sink for invalid records that publishes to `vehicle.deadletter` with original payload and validation error metadata.
- **Expected Files:** `flink/dead_letter.py`
- **Dependencies:** M3-E3-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Invalid records published to `vehicle.deadletter`
  - Dead letter messages include error reason
  - Valid records continue through pipeline

#### M3-E3-T03: Create Data Quality Metrics
- **Task Name:** Add Validation Metrics
- **Description:** Flink metrics (counters) for valid records, invalid records per rule, and dead letter publish count.
- **Expected Files:** `flink/validation.py` (edited) or `flink/metrics.py`
- **Dependencies:** M3-E3-T02
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Metrics visible in Flink UI
  - Prometheus scrapes validation counters

---

## Milestone 4 — Advanced Stream Processing

### Epic M4-E1: Windowing

#### M4-E1-T01: Create Tumbling Window Processor
- **Task Name:** Create Tumbling Window Aggregations
- **Description:** 1-minute tumbling windows computing average speed, average RPM, and max engine temperature per vehicle.
- **Expected Files:** `flink/windows.py`
- **Dependencies:** M3-E2-T03
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Window results emitted at end of each 1-minute window
  - Results contain correct aggregations
  - Late events handled per allowed lateness

#### M4-E1-T02: Create Sliding Window Processor
- **Task Name:** Create Sliding Window Aggregations
- **Description:** 5-minute sliding windows with 1-minute slide for fuel consumption rate and distance traveled.
- **Expected Files:** `flink/windows.py` (edited)
- **Dependencies:** M4-E1-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Results emitted every minute
  - Overlapping windows produce correct incremental results

#### M4-E1-T03: Create Session Window Processor
- **Task Name:** Create Session Window Aggregations
- **Description:** Session windows with 2-minute gap for trip detection: trip duration, average speed, total distance.
- **Expected Files:** `flink/windows.py` (edited)
- **Dependencies:** M4-E1-T02
- **Estimated Difficulty:** High
- **Acceptance Criteria:**
  - Sessions split correctly on 2+ minute gaps
  - Trip metrics calculated per session

#### M4-E1-T04: Create Windowed Aggregation Functions
- **Task Name:** Create Aggregate Functions
- **Description:** Reusable Flink AggregateFunction implementations for avg, max, sum, and custom distance calculation.
- **Expected Files:** `flink/aggregations.py`
- **Dependencies:** M4-E1-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Functions stateful and checkpoint-safe
  - Unit tests pass for each function

---

### Epic M4-E2: Stateful Processing

#### M4-E2-T01: Create State Backend Configuration
- **Task Name:** Configure State Backend
- **Description:** Update `flink-conf.yaml` to use RocksDB state backend with incremental checkpoints and local recovery enabled.
- **Expected Files:** `flink/conf/flink-conf.yaml` (edited)
- **Dependencies:** M1-E4-T03
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - RocksDB directory mounted as volume
  - Incremental checkpoints confirmed in Flink UI

#### M4-E2-T02: Create GPS Distance Calculator
- **Task Name:** Create Distance State Processor
- **Description:** Flink ProcessFunction using ValueState to store previous GPS coordinates and compute haversine distance between consecutive events.
- **Expected Files:** `flink/state.py`
- **Dependencies:** M4-E2-T01, M3-E2-T03
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Distance calculated correctly between GPS points
  - State cleared on vehicle session timeout
  - Metric exposed for total distance per vehicle

#### M4-E2-T03: Create Vehicle Online/Offline Detector
- **Task Name:** Create Online Status State Processor
- **Description:** Detects vehicle online/offline status using last-seen timestamp state. Emits offline event if no telemetry received for 5 minutes.
- **Expected Files:** `flink/state.py` (edited)
- **Dependencies:** M4-E2-T02
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Offline events emitted after 5-minute gap
  - Online events emitted on first message after offline
  - Status transitions logged

#### M4-E2-T04: Create Trip State Manager
- **Task Name:** Create Trip Detection Logic
- **Description:** Manages trip lifecycle: start on ignition (speed > 0 after stationary), end on stationary (speed = 0 for 2+ minutes). Tracks trip ID, start time, end time.
- **Expected Files:** `flink/state.py` (edited)
- **Dependencies:** M4-E2-T03
- **Estimated Difficulty:** High
- **Acceptance Criteria:**
  - Trip start/end events generated correctly
  - Trip ID consistent across windowed aggregations
  - Concurrent trips per vehicle handled

---

### Epic M4-E3: Alerting Engine

#### M4-E3-T01: Create Alert Rules Configuration
- **Task Name:** Create `flink/alerts.py`
- **Description:** Alert rule definitions: engineTemp > 110°C, batteryVoltage < 11V, speed > 120 km/h, fuel < 5%. Each rule has severity (WARNING, CRITICAL).
- **Expected Files:** `flink/alerts.py`
- **Dependencies:** M3-E3-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Each rule fires on threshold breach
  - Rules configurable via environment variables
  - No false positives on edge values

#### M4-E3-T02: Create Alert Publisher
- **Task Name:** Create Alert Kafka Sink
- **Description:** Kafka sink that publishes alert events to `vehicle.alerts` topic with vehicleId, rule name, severity, timestamp, and current value.
- **Expected Files:** `flink/alerts.py` (edited)
- **Dependencies:** M4-E3-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Alerts published to `vehicle.alerts`
  - Alert format matches schema
  - Duplicate alerts suppressed within 1-minute window

#### M4-E3-T03: Create Alert Severity Classifier
- **Task Name:** Add Alert Deduplication
- **Description:** Alert deduplication logic using Flink state to prevent spam: same rule + same vehicle alerts only once per minute.
- **Expected Files:** `flink/alerts.py` (edited)
- **Dependencies:** M4-E3-T02
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Duplicate alerts within 1 minute suppressed
  - Alert count metric accurate
  - State TTL set to 2 minutes

---

## Milestone 5 — Data Sink & Lakehouse

### Epic M5-E1: Iceberg Integration

#### M5-E1-T01: Create Iceberg Table Definitions
- **Task Name:** Create `iceberg/sql/create_tables.sql`
- **Description:** SQL DDL for `vehicle_events` (raw telemetry), `vehicle_aggregations` (windowed metrics), and `vehicle_alerts` (alert history) using Iceberg format.
- **Expected Files:** `iceberg/sql/create_tables.sql`
- **Dependencies:** M1-E3-T04
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - SQL executes successfully in Trino
  - Tables use Iceberg format
  - Partitioning strategy defined (e.g., date partition on event_date)

#### M5-E1-T02: Create Flink Iceberg Sink Configuration
- **Task Name:** Create `flink/iceberg_sink.py`
- **Description:** Flink Iceberg sink builder with catalog configuration pointing to REST catalog, table identifier, and row data serialization.
- **Expected Files:** `flink/iceberg_sink.py`
- **Dependencies:** M5-E1-T01, M1-E4-T04
- **Estimated Difficulty:** High
- **Acceptance Criteria:**
  - Sink connects to Iceberg REST catalog
  - Data lands in MinIO warehouse
  - Table metadata updated correctly

#### M5-E1-T03: Create Vehicle Events Iceberg Sink
- **Task Name:** Wire Raw Events to Iceberg
- **Description:** Update `flink/main.py` to sink validated raw telemetry to `vehicle_events` Iceberg table.
- **Expected Files:** `flink/main.py` (edited)
- **Dependencies:** M5-E1-T02
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Raw events persisted to Iceberg
  - Queryable via Trino
  - Row count increases with simulator output

#### M5-E1-T04: Create Vehicle Alerts Iceberg Sink
- **Task Name:** Wire Alerts to Iceberg
- **Description:** Sink alert stream to `vehicle_alerts` Iceberg table.
- **Expected Files:** `flink/main.py` (edited)
- **Dependencies:** M5-E1-T03, M4-E3-T02
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Alerts persisted to Iceberg
  - Alert severity column queryable

---

### Epic M5-E2: Exactly-Once Semantics

#### M5-E2-T01: Configure Flink Checkpointing
- **Task Name:** Enable Exactly-Once Checkpoints
- **Description:** Update `flink-conf.yaml` and `flink/main.py` to enable exactly-once checkpointing with 30-second intervals, externalized checkpoints, and unaligned checkpoints disabled.
- **Expected Files:** `flink/conf/flink-conf.yaml` (edited), `flink/main.py` (edited)
- **Dependencies:** M3-E1-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Checkpoints complete successfully every 30s
  - Checkpoint size and duration metrics visible
  - No checkpoint failures under normal load

#### M5-E2-T02: Configure Kafka Transactional Producer
- **Task Name:** Enable Kafka EOS
- **Description:** Configure Flink Kafka sink with `Semantic.EXACTLY_ONCE`, transactional ID prefix, and two-phase commit.
- **Expected Files:** `flink/kafka_sink.py`
- **Dependencies:** M5-E2-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Kafka transactions committed atomically
  - No duplicate messages on consumer restart
  - Transaction coordinator metrics healthy

#### M5-E2-T03: Configure Iceberg Exactly-Once Sink
- **Task Name:** Enable Iceberg EOS
- **Description:** Ensure Iceberg sink uses Flink's two-phase commit protocol. Verify commit conflicts handled via retry.
- **Expected Files:** `flink/iceberg_sink.py` (edited)
- **Dependencies:** M5-E2-T02
- **Estimated Difficulty:** High
- **Acceptance Criteria:**
  - Iceberg snapshots created per checkpoint
  - No duplicate data in table on JobManager restart
  - Snapshot history shows clean commits

#### M5-E2-T04: Create Exactly-Once Verification Test
- **Task Name:** Create EOS Integration Test
- **Description:** Test that kills and restarts Flink job while simulator runs, then verifies no duplicates and no missing events in Iceberg.
- **Expected Files:** `tests/integration/test_exactly_once.py`
- **Dependencies:** M5-E2-T03
- **Estimated Difficulty:** High
- **Acceptance Criteria:**
  - Test script runs automatically
  - Row count in Iceberg matches expected count
  - Zero duplicate primary keys

---

### Epic M5-E3: Iceberg Advanced Features

#### M5-E3-T01: Create Schema Evolution Script
- **Task Name:** Create Schema Evolution Demo
- **Description:** SQL script that adds a new column `tire_pressure` to `vehicle_events` and backfills with default value.
- **Expected Files:** `iceberg/sql/schema_evolution.sql`
- **Dependencies:** M5-E1-T01
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - ALTER TABLE succeeds without full rewrite
  - Old snapshots still readable with old schema
  - New data includes new column

#### M5-E3-T02: Create Time Travel Query Examples
- **Task Name:** Create Time Travel SQL
- **Description:** SQL queries demonstrating `AS OF TIMESTAMP` and `AS OF SYSTEM_VERSION` to query historical table states.
- **Expected Files:** `iceberg/sql/time_travel.sql`
- **Dependencies:** M5-E1-T01
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Queries return different row counts for different timestamps
  - Snapshot IDs retrievable from `$snapshots` metadata table

#### M5-E3-T03: Create Compaction Script
- **Task Name:** Create Iceberg Compaction Procedure
- **Description:** SQL script or Python script calling Iceberg's `rewrite_data_files` procedure to compact small files.
- **Expected Files:** `iceberg/sql/compaction.sql`
- **Dependencies:** M5-E1-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Small files merged into larger ones
  - Query performance improves post-compaction
  - Snapshot history preserved

#### M5-E3-T04: Create Partition Evolution Script
- **Task Name:** Create Partition Evolution Demo
- **Description:** SQL script showing partition evolution from daily to hourly partitioning using Iceberg's hidden partitioning.
- **Expected Files:** `iceberg/sql/partition_evolution.sql`
- **Dependencies:** M5-E3-T01
- **Estimated Difficulty:** High
- **Acceptance Criteria:**
  - Partition spec updated without rewrite
  - New data written with new partition scheme
  - Old partitions remain queryable

---

## Milestone 6 — Analytics & Observability

### Epic M6-E1: Trino SQL Analytics

#### M6-E1-T01: Configure Trino Service
- **Task Name:** Define Trino Docker Service
- **Description:** Add Trino coordinator and worker services to `docker-compose.yml` with Iceberg connector configured.
- **Expected Files:** `docker-compose.yml` (edited)
- **Dependencies:** M1-E3-T02
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Trino UI accessible at `http://localhost:8080`
  - Cluster shows active worker nodes

#### M6-E1-T02: Create Trino Iceberg Catalog Configuration
- **Task Name:** Create Trino Catalog Properties
- **Description:** Iceberg catalog properties file for Trino pointing to REST catalog and MinIO S3 endpoint.
- **Expected Files:** `trino/catalog/iceberg.properties`
- **Dependencies:** M6-E1-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - `SHOW CATALOGS` includes `iceberg`
  - `SHOW SCHEMAS IN iceberg` lists default schema

#### M6-E1-T03: Create Analytics Queries
- **Task Name:** Create `iceberg/sql/queries.sql`
- **Description:** Business analytics queries: top 10 fastest vehicles, average speed by hour, fuel usage trends, alert frequency by rule, trip summaries.
- **Expected Files:** `iceberg/sql/queries.sql`
- **Dependencies:** M6-E1-T02
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - All queries execute successfully
  - Results are meaningful with simulator data
  - Queries documented with expected output

#### M6-E1-T04: Create Trino View Definitions
- **Task Name:** Create Analytics Views
- **Description:** Trino views for common queries: `vehicle_summary`, `alert_summary`, `trip_metrics`.
- **Expected Files:** `iceberg/sql/views.sql`
- **Dependencies:** M6-E1-T03
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Views queryable like tables
  - View definitions stored in Iceberg metadata

---

### Epic M6-E2: Grafana Dashboards

#### M6-E2-T01: Create Pipeline Metrics Dashboard
- **Task Name:** Create Flink Pipeline Dashboard JSON
- **Description:** Grafana dashboard showing: events/sec, Kafka lag, checkpoint duration, processing latency, watermark delay, backpressure.
- **Expected Files:** `grafana/dashboards/pipeline_metrics.json`
- **Dependencies:** M1-E5-T04
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Dashboard imports without errors
  - All panels show data when pipeline is running
  - Refresh interval set to 5s

#### M6-E2-T02: Create Business Metrics Dashboard
- **Task Name:** Create Business KPI Dashboard JSON
- **Description:** Grafana dashboard with Trino datasource showing: active vehicles, average fleet speed, alert count by severity, fuel efficiency, trip count.
- **Expected Files:** `grafana/dashboards/business_metrics.json`
- **Dependencies:** M6-E1-T04
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Panels query Trino successfully
  - Data updates reflect simulator changes
  - Time range controls work

#### M6-E2-T03: Create Alerting Dashboard
- **Task Name:** Create Alert Monitor Dashboard JSON
- **Description:** Real-time alert feed panel, alert history table, and alert rate graph.
- **Expected Files:** `grafana/dashboards/alert_monitor.json`
- **Dependencies:** M6-E2-T02
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Alerts appear within 10 seconds of generation
  - Severity color-coded
  - Acknowledgment workflow documented

#### M6-E2-T04: Create Dashboard Provisioning Config
- **Task Name:** Create Dashboard Auto-Provisioning
- **Description:** YAML configuration in `grafana/provisioning/dashboards/` to auto-load all dashboard JSON files.
- **Expected Files:** `grafana/provisioning/dashboards/dashboards.yml`
- **Dependencies:** M6-E2-T01
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Dashboards appear on first Grafana startup
  - No manual import required

---

### Epic M6-E3: Operational Monitoring

#### M6-E3-T01: Configure Flink Metrics Reporter
- **Task Name:** Enable Prometheus Metrics Reporter
- **Description:** Update `flink-conf.yaml` to push metrics to Prometheus via PushGateway or expose via Prometheus reporter.
- **Expected Files:** `flink/conf/flink-conf.yaml` (edited)
- **Dependencies:** M1-E5-T02
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Flink metrics visible in Prometheus
  - Key metrics: numRecordsIn, numRecordsOut, checkpointDuration

#### M6-E3-T02: Create Prometheus Recording Rules
- **Task Name:** Create Recording Rules
- **Description:** Prometheus recording rules for derived metrics: events per second, average lag, error rate.
- **Expected Files:** `prometheus/recording_rules.yml`
- **Dependencies:** M6-E3-T01
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Rules evaluate without errors
  - Recorded metrics queryable in Prometheus

#### M6-E3-T03: Create Prometheus Alert Rules
- **Task Name:** Create Infrastructure Alerts
- **Description:** Prometheus alert rules for: Flink checkpoint failures, Kafka lag > 1000, MinIO disk > 80%, dead letter queue growing.
- **Expected Files:** `prometheus/alert_rules.yml`
- **Dependencies:** M6-E3-T02
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Alerts fire on simulated failure conditions
  - Alertmanager routes to visible channel (or log)

---

## Milestone 7 — Production Hardening

### Epic M7-E1: Checkpointing & Recovery

#### M7-E1-T01: Configure Incremental Checkpoints
- **Task Name:** Optimize Checkpoint Configuration
- **Description:** Update `flink-conf.yaml` for incremental checkpoints, local recovery, and compression.
- **Expected Files:** `flink/conf/flink-conf.yaml` (edited)
- **Dependencies:** M5-E2-T01
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Incremental checkpoint size < 10% of full checkpoint
  - Local recovery enabled
  - State backend metrics visible

#### M7-E1-T02: Create Savepoint Management Script
- **Task Name:** Create Savepoint CLI Tool
- **Description:** Bash/Python script to trigger savepoints, list savepoints, and restore from savepoint.
- **Expected Files:** `scripts/savepoint_manager.py`
- **Dependencies:** M7-E1-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Savepoint triggered successfully
  - Job restarts from savepoint with correct state
  - Script has `--trigger`, `--list`, `--restore` commands

#### M7-E1-T03: Configure State TTL
- **Task Name:** Add State TTL Policies
- **Description:** Configure TTL for GPS state (1 hour), alert dedup state (10 minutes), and trip state (24 hours).
- **Expected Files:** `flink/state.py` (edited)
- **Dependencies:** M4-E2-T04
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - State size stabilizes over time
  - Expired state cleaned up
  - No memory leaks in TaskManager

---

### Epic M7-E2: Failure Recovery Demo

#### M7-E2-T01: Create Chaos Test Script
- **Task Name:** Create Failure Injection Tests
- **Description:** Python script that randomly kills TaskManager, JobManager, or simulator containers and verifies recovery.
- **Expected Files:** `tests/chaos/test_recovery.py`
- **Dependencies:** M7-E1-T02
- **Estimated Difficulty:** High
- **Acceptance Criteria:**
  - Container killed and restarted automatically
  - Job recovers to RUNNING state
  - No data loss verified in Iceberg

#### M7-E2-T02: Create Recovery Verification Script
- **Task Name:** Create Data Integrity Checker
- **Description:** Script that counts events in Kafka, Flink metrics, and Iceberg to verify consistency after recovery.
- **Expected Files:** `tests/chaos/verify_integrity.py`
- **Dependencies:** M7-E2-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Row counts match within tolerance
  - No duplicate event IDs
  - Report generated with pass/fail status

#### M7-E2-T03: Create Failure Scenario Documentation
- **Task Name:** Document Recovery Scenarios
- **Description:** Markdown doc describing: TaskManager failure, JobManager failure, Kafka broker failure, MinIO outage, and expected recovery behavior.
- **Expected Files:** `docs/failure_scenarios.md`
- **Dependencies:** M7-E2-T02
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Document covers all 4 failure types
  - Recovery time objectives stated
  - Verification steps included

---

### Epic M7-E3: Testing & Documentation

#### M7-E3-T01: Create Simulator Unit Tests
- **Task Name:** Create `tests/unit/test_simulator.py`
- **Description:** Unit tests for telemetry generation, config validation, and Kafka client mock tests.
- **Expected Files:** `tests/unit/test_simulator.py`
- **Dependencies:** M2-E1-T06
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - pytest passes with >80% coverage
  - Mock Kafka producer verifies message format

#### M7-E3-T02: Create Validation Unit Tests
- **Task Name:** Create `tests/unit/test_validation.py`
- **Description:** Unit tests for each validation rule: negative speed, invalid coordinates, missing vehicleId, future timestamp.
- **Expected Files:** `tests/unit/test_validation.py`
- **Dependencies:** M3-E3-T01
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - All edge cases covered
  - Invalid inputs rejected correctly
  - Error messages descriptive

#### M7-E3-T03: Create Integration Tests
- **Task Name:** Create `tests/integration/test_pipeline.py`
- **Description:** Integration test spinning up Kafka + Flink + MinIO via testcontainers, running simulator, and verifying end-to-end data flow.
- **Expected Files:** `tests/integration/test_pipeline.py`
- **Dependencies:** M5-E1-T04
- **Estimated Difficulty:** High
- **Acceptance Criteria:**
  - Testcontainers manage dependencies
  - Full pipeline executes in < 5 minutes
  - Iceberg rows verified

#### M7-E3-T04: Create Smoke Tests
- **Task Name:** Create `tests/smoke/test_end_to_end.py`
- **Description:** Lightweight smoke test that verifies all services respond on expected ports and basic functionality works.
- **Expected Files:** `tests/smoke/test_end_to_end.py`
- **Dependencies:** M6-E1-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - All services health checks pass
  - Kafka produces and consumes
  - Trino executes simple query

#### M7-E3-T05: Create Architecture Documentation
- **Task Name:** Create `docs/architecture.md`
- **Description:** Comprehensive architecture doc with component diagrams, data flow, technology justifications, and configuration reference.
- **Expected Files:** `docs/architecture.md`
- **Dependencies:** All previous milestones
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Mermaid or ASCII diagrams included
  - All data flows documented
  - Configuration table complete

#### M7-E3-T06: Create Operations Runbook
- **Task Name:** Create `docs/operations.md`
- **Description:** Runbook covering: startup, shutdown, scaling, debugging, common issues, log locations, and metric interpretation.
- **Expected Files:** `docs/operations.md`
- **Dependencies:** M7-E3-T05
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Commands are copy-paste ready
  - Troubleshooting flowchart included
  - Contact/escalation info placeholder

---

## Milestone 8 — Future Enhancements

### Epic M8-E1: Advanced Features

#### M8-E1-T01: Document Vehicle Routes Feature
- **Task Name:** Create Vehicle Routes RFC
- **Description:** Design doc for simulating actual GPS paths using predefined routes rather than random coordinates.
- **Expected Files:** `docs/rfc/vehicle_routes.md`
- **Dependencies:** None
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Route format defined (GeoJSON or GPX)
  - Interpolation logic described
  - Acceptance criteria listed

#### M8-E1-T02: Document REST API Feature
- **Task Name:** Create REST API RFC
- **Description:** Design doc for FastAPI service exposing analytics endpoints: /vehicles, /trips, /alerts, /metrics.
- **Expected Files:** `docs/rfc/rest_api.md`
- **Dependencies:** None
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - API spec in OpenAPI format
  - Authentication approach defined
  - Rate limiting discussed

#### M8-E1-T03: Document Multi-Topic Ingestion
- **Task Name:** Create Multi-Topic RFC
- **Description:** Design doc for ingesting engine diagnostics, weather, and GPS as separate Kafka topics with unified processing.
- **Expected Files:** `docs/rfc/multi_topic.md`
- **Dependencies:** None
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Topic schema definitions
  - Join strategy documented
  - Backpressure handling discussed

#### M8-E1-T04: Document AI Extension
- **Task Name:** Create AI Alert RFC
- **Description:** Design doc for integrating Ollama LLM to generate natural language alert summaries from structured alert data.
- **Expected Files:** `docs/rfc/ai_extension.md`
- **Dependencies:** None
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Prompt template designed
  - Latency requirements stated
  - Fallback behavior documented

---

### Epic M8-E2: Cloud Migration Path

#### M8-E2-T01: Create Cloud Architecture Comparison
- **Task Name:** Create Cloud Migration Guide
- **Description:** Document mapping local services to cloud equivalents: Kafka→Event Hubs, MinIO→ADLS Gen2, Iceberg→Unity Catalog, Trino→Databricks SQL, Docker→AKS.
- **Expected Files:** `docs/cloud_migration.md`
- **Dependencies:** None
- **Estimated Difficulty:** Low
- **Acceptance Criteria:**
  - Service mapping table complete
  - Configuration differences noted
  - Cost considerations mentioned

#### M8-E2-T02: Create Terraform Module Outline
- **Task Name:** Create Infrastructure-as-Code Outline
- **Description:** Skeleton Terraform modules for Azure deployment: resource group, Event Hubs, ADLS Gen2, AKS cluster.
- **Expected Files:** `terraform/main.tf`, `terraform/variables.tf`, `terraform/outputs.tf`
- **Dependencies:** M8-E2-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - `terraform validate` passes
  - Modules parameterized

#### M8-E2-T03: Create Kubernetes Deployment Outline
- **Task Name:** Create K8s Manifests Skeleton
- **Description:** Kubernetes Deployment and Service manifests for Flink JobManager, TaskManager, and simulator.
- **Expected Files:** `k8s/flink-deployment.yml`, `k8s/simulator-deployment.yml`
- **Dependencies:** M8-E2-T01
- **Estimated Difficulty:** Medium
- **Acceptance Criteria:**
  - Manifests syntactically valid
  - Resource limits defined
  - ConfigMap references correct

---

# 5 Dependency Graph

```
M1 Infrastructure Foundation
│
├─ M1-E1 Project Bootstrap
│  ├─ M1-E1-T01 .env
│  ├─ M1-E1-T02 docker-compose.yml (base)
│  ├─ M1-E1-T03 README.md
│  └─ M1-E1-T04 Folder structure
│
├─ M1-E2 Kafka Infrastructure
│  ├─ M1-E2-T01 Zookeeper service
│  ├─ M1-E2-T02 Kafka broker service
│  ├─ M1-E2-T03 Kafka UI service
│  └─ M1-E2-T04 Topic init script
│
├─ M1-E3 Storage Layer
│  ├─ M1-E3-T01 MinIO service
│  ├─ M1-E3-T02 Iceberg REST catalog
│  ├─ M1-E3-T03 MinIO bucket init
│  └─ M1-E3-T04 Catalog config
│
├─ M1-E4 Flink Infrastructure
│  ├─ M1-E4-T01 JobManager service
│  ├─ M1-E4-T02 TaskManager service
│  ├─ M1-E4-T03 flink-conf.yaml
│  └─ M1-E4-T04 Flink Dockerfile
│
└─ M1-E5 Monitoring Stack
   ├─ M1-E5-T01 Prometheus service
   ├─ M1-E5-T02 prometheus.yml
   ├─ M1-E5-T03 Grafana service
   └─ M1-E5-T04 Datasource provisioning

        ↓

M2 Data Ingestion Layer
│
├─ M2-E1 Vehicle Simulator
│  ├─ M2-E1-T01 producer/config.py
│  ├─ M2-E1-T02 producer/schemas.py
│  ├─ M2-E1-T03 producer/simulator.py
│  ├─ M2-E1-T04 producer/kafka_client.py
│  ├─ M2-E1-T05 producer/main.py
│  └─ M2-E1-T06 Producer Dockerfile + requirements
│
├─ M2-E2 Kafka Topics & Schemas
│  ├─ M2-E2-T01 Topic definitions
│  ├─ M2-E2-T02 JSON schemas
│  └─ M2-E2-T03 Schema registry
│
└─ M2-E3 Producer Deployment
   ├─ M2-E3-T01 Simulator in compose
   └─ M2-E3-T02 Health check

        ↓

M3 Stream Processing Core
│
├─ M3-E1 Flink Job Skeleton
│  ├─ M3-E1-T01 flink/main.py
│  ├─ M3-E1-T02 flink/requirements.txt
│  ├─ M3-E1-T03 flink/kafka_source.py
│  └─ M3-E1-T04 Flink job in compose
│
├─ M3-E2 Event Time & Watermarks
│  ├─ M3-E2-T01 flink/timestamps.py
│  ├─ M3-E2-T02 flink/watermarks.py
│  └─ M3-E2-T03 Integrate watermarks
│
└─ M3-E3 Data Validation & DLQ
   ├─ M3-E3-T01 flink/validation.py
   ├─ M3-E3-T02 flink/dead_letter.py
   └─ M3-E3-T03 Validation metrics

        ↓

M4 Advanced Stream Processing
│
├─ M4-E1 Windowing
│  ├─ M4-E1-T01 Tumbling windows
│  ├─ M4-E1-T02 Sliding windows
│  ├─ M4-E1-T03 Session windows
│  └─ M4-E1-T04 Aggregation functions
│
├─ M4-E2 Stateful Processing
│  ├─ M4-E2-T01 State backend config
│  ├─ M4-E2-T02 GPS distance calc
│  ├─ M4-E2-T03 Online/offline detector
│  └─ M4-E2-T04 Trip state manager
│
└─ M4-E3 Alerting Engine
   ├─ M4-E3-T01 flink/alerts.py rules
   ├─ M4-E3-T02 Alert publisher
   └─ M4-E3-T03 Alert deduplication

        ↓

M5 Data Sink & Lakehouse
│
├─ M5-E1 Iceberg Integration
│  ├─ M5-E1-T01 create_tables.sql
│  ├─ M5-E1-T02 flink/iceberg_sink.py
│  ├─ M5-E1-T03 Wire events sink
│  └─ M5-E1-T04 Wire alerts sink
│
├─ M5-E2 Exactly-Once Semantics
│  ├─ M5-E2-T01 Checkpoint config
│  ├─ M5-E2-T02 Kafka EOS
│  ├─ M5-E2-T03 Iceberg EOS
│  └─ M5-E2-T04 EOS verification test
│
└─ M5-E3 Iceberg Advanced Features
   ├─ M5-E3-T01 Schema evolution
   ├─ M5-E3-T02 Time travel queries
   ├─ M5-E3-T03 Compaction
   └─ M5-E3-T04 Partition evolution

        ↓

M6 Analytics & Observability
│
├─ M6-E1 Trino SQL Analytics
│  ├─ M6-E1-T01 Trino service
│  ├─ M6-E1-T02 Trino catalog config
│  ├─ M6-E1-T03 queries.sql
│  └─ M6-E1-T04 views.sql
│
├─ M6-E2 Grafana Dashboards
│  ├─ M6-E2-T01 Pipeline dashboard
│  ├─ M6-E2-T02 Business dashboard
│  ├─ M6-E2-T03 Alert dashboard
│  └─ M6-E2-T04 Dashboard provisioning
│
└─ M6-E3 Operational Monitoring
   ├─ M6-E3-T01 Flink metrics reporter
   ├─ M6-E3-T02 Recording rules
   └─ M6-E3-T03 Alert rules

        ↓

M7 Production Hardening
│
├─ M7-E1 Checkpointing & Recovery
│  ├─ M7-E1-T01 Incremental checkpoints
│  ├─ M7-E1-T02 Savepoint manager
│  └─ M7-E1-T03 State TTL
│
├─ M7-E2 Failure Recovery Demo
│  ├─ M7-E2-T01 Chaos tests
│  ├─ M7-E2-T02 Integrity checker
│  └─ M7-E2-T03 Failure scenarios doc
│
└─ M7-E3 Testing & Documentation
   ├─ M7-E3-T01 Unit: simulator
   ├─ M7-E3-T02 Unit: validation
   ├─ M7-E3-T03 Integration tests
   ├─ M7-E3-T04 Smoke tests
   ├─ M7-E3-T05 Architecture docs
   └─ M7-E3-T06 Operations runbook

        ↓

M8 Future Enhancements
│
├─ M8-E1 Advanced Features
│  ├─ M8-E1-T01 Vehicle routes RFC
│  ├─ M8-E1-T02 REST API RFC
│  ├─ M8-E1-T03 Multi-topic RFC
│  └─ M8-E1-T04 AI extension RFC
│
└─ M8-E2 Cloud Migration Path
   ├─ M8-E2-T01 Cloud migration guide
   ├─ M8-E2-T02 Terraform outline
   └─ M8-E2-T03 Kubernetes outline
```

---

# 6 Git Commit Plan

| Commit | Message | Scope | Tasks Included |
|--------|---------|-------|----------------|
| 1 | `chore: initialize repository structure` | Repo | M1-E1-T04 |
| 2 | `docs: add README and project plan` | Docs | M1-E1-T03 |
| 3 | `infra: add environment configuration` | Config | M1-E1-T01 |
| 4 | `infra: add Kafka, Zookeeper, and Kafka UI services` | Docker | M1-E2-T01, M1-E2-T02, M1-E2-T03 |
| 5 | `infra: add MinIO and Iceberg REST catalog` | Docker | M1-E3-T01, M1-E3-T02 |
| 6 | `infra: add Flink JobManager and TaskManager` | Docker | M1-E4-T01, M1-E4-T02 |
| 7 | `infra: add Prometheus and Grafana services` | Docker | M1-E5-T01, M1-E5-T03 |
| 8 | `config: add Flink, Prometheus, and Grafana configs` | Config | M1-E4-T03, M1-E5-T02, M1-E5-T04 |
| 9 | `infra: add custom Flink Dockerfile` | Docker | M1-E4-T04 |
| 10 | `infra: add Kafka topic initialization script` | Scripts | M1-E2-T04 |
| 11 | `infra: add MinIO bucket initialization` | Scripts | M1-E3-T03 |
| 12 | `infra: add Iceberg catalog properties` | Config | M1-E3-T04 |
| 13 | `feat: add vehicle simulator config and schemas` | Producer | M2-E1-T01, M2-E1-T02 |
| 14 | `feat: add telemetry generator core` | Producer | M2-E1-T03 |
| 15 | `feat: add Kafka producer client` | Producer | M2-E1-T04 |
| 16 | `feat: add simulator entry point and packaging` | Producer | M2-E1-T05, M2-E1-T06 |
| 17 | `feat: add Kafka topic definitions and schemas` | Kafka | M2-E2-T01, M2-E2-T02 |
| 18 | `infra: integrate simulator into compose stack` | Docker | M2-E3-T01, M2-E3-T02 |
| 19 | `feat: add Flink job skeleton and Kafka source` | Flink | M3-E1-T01, M3-E1-T02, M3-E1-T03 |
| 20 | `infra: add Flink job to compose stack` | Docker | M3-E1-T04 |
| 21 | `feat: add event time timestamp assigner` | Flink | M3-E2-T01 |
| 22 | `feat: add watermark strategy` | Flink | M3-E2-T02 |
| 23 | `feat: integrate watermarks into pipeline` | Flink | M3-E2-T03 |
| 24 | `feat: add data validation rules engine` | Flink | M3-E3-T01 |
| 25 | `feat: add dead letter queue sink` | Flink | M3-E3-T02 |
| 26 | `feat: add validation metrics` | Flink | M3-E3-T03 |
| 27 | `feat: add tumbling and sliding windows` | Flink | M4-E1-T01, M4-E1-T02 |
| 28 | `feat: add session windows and aggregation functions` | Flink | M4-E1-T03, M4-E1-T04 |
| 29 | `config: configure RocksDB state backend` | Config | M4-E2-T01 |
| 30 | `feat: add GPS distance calculator` | Flink | M4-E2-T02 |
| 31 | `feat: add vehicle online/offline detector` | Flink | M4-E2-T03 |
| 32 | `feat: add trip state manager` | Flink | M4-E2-T04 |
| 33 | `feat: add alert rules and publisher` | Flink | M4-E3-T01, M4-E3-T02 |
| 34 | `feat: add alert deduplication` | Flink | M4-E3-T03 |
| 35 | `feat: add Iceberg table definitions` | SQL | M5-E1-T01 |
| 36 | `feat: add Flink Iceberg sink` | Flink | M5-E1-T02 |
| 37 | `feat: wire events and alerts to Iceberg` | Flink | M5-E1-T03, M5-E1-T04 |
| 38 | `feat: enable exactly-once checkpointing` | Config | M5-E2-T01 |
| 39 | `feat: enable Kafka transactional producer` | Flink | M5-E2-T02 |
| 40 | `feat: enable Iceberg exactly-once sink` | Flink | M5-E2-T03 |
| 41 | `test: add exactly-once verification test` | Tests | M5-E2-T04 |
| 42 | `feat: add schema evolution script` | SQL | M5-E3-T01 |
| 43 | `feat: add time travel queries` | SQL | M5-E3-T02 |
| 44 | `feat: add compaction script` | SQL | M5-E3-T03 |
| 45 | `feat: add partition evolution script` | SQL | M5-E3-T04 |
| 46 | `infra: add Trino service and catalog` | Docker | M6-E1-T01, M6-E1-T02 |
| 47 | `feat: add Trino analytics queries and views` | SQL | M6-E1-T03, M6-E1-T04 |
| 48 | `feat: add Grafana pipeline dashboard` | Dashboard | M6-E2-T01 |
| 49 | `feat: add Grafana business and alert dashboards` | Dashboard | M6-E2-T02, M6-E2-T03 |
| 50 | `infra: add Grafana dashboard provisioning` | Config | M6-E2-T04 |
| 51 | `feat: configure Flink Prometheus metrics` | Config | M6-E3-T01 |
| 52 | `feat: add Prometheus recording and alert rules` | Config | M6-E3-T02, M6-E3-T03 |
| 53 | `config: optimize checkpoint configuration` | Config | M7-E1-T01 |
| 54 | `feat: add savepoint management script` | Scripts | M7-E1-T02 |
| 55 | `feat: add state TTL policies` | Flink | M7-E1-T03 |
| 56 | `test: add chaos recovery tests` | Tests | M7-E2-T01 |
| 57 | `test: add data integrity checker` | Tests | M7-E2-T02 |
| 58 | `docs: add failure scenarios documentation` | Docs | M7-E2-T03 |
| 59 | `test: add simulator and validation unit tests` | Tests | M7-E3-T01, M7-E3-T02 |
| 60 | `test: add integration and smoke tests` | Tests | M7-E3-T03, M7-E3-T04 |
| 61 | `docs: add architecture and operations documentation` | Docs | M7-E3-T05, M7-E3-T06 |
| 62 | `docs: add advanced features RFCs` | Docs | M8-E1-T01–T04 |
| 63 | `docs: add cloud migration guide` | Docs | M8-E2-T01 |
| 64 | `infra: add Terraform and Kubernetes outlines` | IaC | M8-E2-T02, M8-E2-T03 |

---

# 7 GitHub Issues

## Issue Template

Each atomic task maps to one GitHub Issue with the following structure:

```yaml
Title: "[M{M}-E{E}] {Task Name}"
Labels: [milestone-{M}, epic-{E}, {component}, {priority}]
Priority: {High | Medium | Low}
Description: |
  ## Objective
  {Description from atomic task}

  ## Acceptance Criteria
  - {Criterion 1}
  - {Criterion 2}
  - {Criterion 3}

  ## Dependencies
  - {Dependency issue reference}

  ## Estimated Difficulty
  {Low | Medium | High}

  ## Expected Files
  - `{filepath}`
```

## Sample Issues (First 10)

### Issue #1: [M1-E1] Create `.env` Environment File
- **Labels:** `milestone-1`, `epic-1`, `config`, `high`
- **Priority:** High
- **Dependencies:** None
- **Expected Files:** `.env`

### Issue #2: [M1-E1] Create `docker-compose.yml` Base Services
- **Labels:** `milestone-1`, `epic-1`, `docker`, `high`
- **Priority:** High
- **Dependencies:** #1
- **Expected Files:** `docker-compose.yml`

### Issue #3: [M1-E1] Create Project README
- **Labels:** `milestone-1`, `epic-1`, `docs`, `low`
- **Priority:** Low
- **Dependencies:** None
- **Expected Files:** `README.md`

### Issue #4: [M1-E1] Initialize Repository Directory Layout
- **Labels:** `milestone-1`, `epic-1`, `chore`, `low`
- **Priority:** Low
- **Dependencies:** None
- **Expected Files:** Directory tree

### Issue #5: [M1-E2] Configure Zookeeper Service
- **Labels:** `milestone-1`, `epic-2`, `docker`, `kafka`, `high`
- **Priority:** High
- **Dependencies:** #2
- **Expected Files:** `docker-compose.yml` (edited)

### Issue #6: [M1-E2] Configure Kafka Broker Service
- **Labels:** `milestone-1`, `epic-2`, `docker`, `kafka`, `high`
- **Priority:** High
- **Dependencies:** #5
- **Expected Files:** `docker-compose.yml` (edited)

### Issue #7: [M1-E2] Configure Kafka UI Service
- **Labels:** `milestone-1`, `epic-2`, `docker`, `kafka`, `medium`
- **Priority:** Medium
- **Dependencies:** #6
- **Expected Files:** `docker-compose.yml` (edited)

### Issue #8: [M1-E2] Create Kafka Topic Initialization Script
- **Labels:** `milestone-1`, `epic-2`, `scripts`, `kafka`, `medium`
- **Priority:** Medium
- **Dependencies:** #6
- **Expected Files:** `scripts/create_topics.py`

### Issue #9: [M1-E3] Configure MinIO Service
- **Labels:** `milestone-1`, `epic-3`, `docker`, `storage`, `high`
- **Priority:** High
- **Dependencies:** #2
- **Expected Files:** `docker-compose.yml` (edited)

### Issue #10: [M1-E3] Configure Iceberg REST Catalog Service
- **Labels:** `milestone-1`, `epic-3`, `docker`, `storage`, `iceberg`, `high`
- **Priority:** High
- **Dependencies:** #9
- **Expected Files:** `docker-compose.yml` (edited)

*(Remaining 72 issues follow the same pattern for each atomic task.)*

---

# 8 Coding Prompt For Every Task

## Prompt Template

```
You are a Senior Software Engineer.

Current Milestone: {Milestone Name}
Current Epic: {Epic Name}
Current Task: {Task Name}

Current Repository Structure:
```
{tree output showing current files}
```

Requirements:
{Detailed requirements from atomic task}

Constraints:
- Python 3.12 with type hints
- PEP 8 compliance
- No placeholder code or TODOs
- Production-quality error handling
- Comprehensive docstrings (Google style)
- Structured logging using Python's logging module
- Unit tests if the file contains business logic
- Do not modify unrelated files
- Output ONLY the required file(s)

Expected Output:
{Filename and brief description}
```

## Sample Prompts (Representative Set)

### Prompt: M1-E1-T01 — Create `.env` Environment File

```
You are a Senior Software Engineer.

Current Milestone: Infrastructure Foundation
Current Epic: Project Bootstrap
Current Task: Create .env Environment File

Current Repository Structure:
```
streaming-lakehouse/
```

Requirements:
Create a `.env` file that defines all environment variables for the Docker Compose stack:
- Kafka: KAFKA_BROKER_PORT, KAFKA_INTERNAL_PORT, KAFKA_UI_PORT
- Zookeeper: ZOOKEEPER_PORT
- MinIO: MINIO_API_PORT, MINIO_CONSOLE_PORT, MINIO_ROOT_USER, MINIO_ROOT_PASSWORD
- Iceberg Catalog: CATALOG_PORT, CATALOG_WAREHOUSE
- Flink: FLINK_JOBMANAGER_PORT, FLINK_TASKMANAGER_SLOTS, FLINK_PARALLELISM
- Trino: TRINO_PORT
- Grafana: GRAFANA_PORT, GRAFANA_ADMIN_USER, GRAFANA_ADMIN_PASSWORD
- Prometheus: PROMETHEUS_PORT
- Simulator: SIMULATOR_TPS, SIMULATOR_VEHICLE_COUNT, SIMULATOR_DUPLICATE_PCT, SIMULATOR_OUT_OF_ORDER_PCT

All ports should use the values from the project plan.
No secrets should be hardcoded in docker-compose.yml; everything references these variables.

Constraints:
- Use standard .env format (KEY=VALUE)
- Include comments explaining each variable
- No quotes around values unless necessary
- Output ONLY the .env file

Expected Output: `.env`
```

### Prompt: M2-E1-T03 — Create Telemetry Generator Core

```
You are a Senior Software Engineer.

Current Milestone: Data Ingestion Layer
Current Epic: Vehicle Simulator
Current Task: Create Telemetry Generator Core

Current Repository Structure:
```
streaming-lakehouse/
├── producer/
│   ├── config.py      # SimulatorConfig dataclass with TPS, vehicle_count, etc.
│   └── schemas.py     # VehicleTelemetry dataclass with all fields
```

Requirements:
Create `producer/simulator.py` containing the core telemetry simulation engine.

The simulator must:
1. Generate VehicleTelemetry events for N configured vehicles
2. Support configurable TPS (transactions per second) across all vehicles
3. Add random delays (0-500ms) between events per vehicle
4. Inject duplicate events at configured probability (same event ID/timestamp)
5. Inject out-of-order events at configured probability (timestamp offset -10 to -30 seconds)
6. Simulate realistic GPS movement: vehicles move in a direction with slight random variation
7. Simulate realistic engine metrics: RPM correlates with speed, temperature correlates with RPM
8. Use asyncio for concurrent vehicle simulation
9. Yield events for consumption by the Kafka client

Constraints:
- Python 3.12 with full type hints
- PEP 8 compliance
- No placeholder code
- Use asyncio and asyncio.Queue
- Logging for each event generated at DEBUG level
- Docstrings for all public methods
- Output ONLY producer/simulator.py

Expected Output: `producer/simulator.py`
```

### Prompt: M3-E2-T02 — Create Watermark Strategy

```
You are a Senior Software Engineer.

Current Milestone: Stream Processing Core
Current Epic: Event Time & Watermarks
Current Task: Create Watermark Strategy

Current Repository Structure:
```
streaming-lakehouse/
├── flink/
│   ├── main.py          # Entry point with pipeline skeleton
│   ├── kafka_source.py  # Kafka source configuration
│   └── timestamps.py    # TimestampAssigner implementation
```

Requirements:
Create `flink/watermarks.py` that defines a WatermarkStrategy for vehicle telemetry events.

The strategy must:
1. Use bounded out-of-orderness of 5 seconds
2. Set idle timeout to 30 seconds (sources that go idle should not block watermarks)
3. Support watermark alignment across multiple sources if parallelism > 1
4. Expose a helper function `get_watermark_strategy()` that returns the configured strategy
5. Include a custom WatermarkGenerator if needed for special handling

Constraints:
- Python 3.12 with PyFlink 1.18
- Full type hints
- Use pyflink.datastream.window module
- No placeholder code
- Docstrings explaining the watermark semantics
- Output ONLY flink/watermarks.py

Expected Output: `flink/watermarks.py`
```

### Prompt: M4-E3-T01 — Create Alert Rules Configuration

```
You are a Senior Software Engineer.

Current Milestone: Advanced Stream Processing
Current Epic: Alerting Engine
Current Task: Create Alert Rules Configuration

Current Repository Structure:
```
streaming-lakehouse/
├── flink/
│   ├── main.py          # Pipeline with validation and windowing
│   ├── validation.py    # Data validation with dead letter queue
│   └── windows.py       # Windowed aggregations
```

Requirements:
Create `flink/alerts.py` that defines alert rules and evaluation logic for vehicle telemetry.

Alert rules:
1. ENGINE_OVERHEAT: engineTemp > 110°C → CRITICAL
2. LOW_BATTERY: batteryVoltage < 11V → WARNING
3. OVERSPEED: speed > 120 km/h → CRITICAL
4. LOW_FUEL: fuel < 5% → WARNING

The module must:
1. Define an AlertRule dataclass with name, field, threshold, operator, severity
2. Define an AlertEvent dataclass with vehicleId, rule, severity, timestamp, value, message
3. Provide `evaluate_alert(telemetry: VehicleTelemetry) -> list[AlertEvent]` function
4. Support configurable thresholds via environment variables with defaults
5. Include a severity enum (WARNING, CRITICAL)
6. Generate human-readable alert messages

Constraints:
- Python 3.12 with PyFlink 1.18
- Full type hints
- PEP 8
- No placeholder code
- Logging for each alert fired at INFO level
- Output ONLY flink/alerts.py

Expected Output: `flink/alerts.py`
```

### Prompt: M5-E1-T01 — Create Iceberg Table Definitions

```
You are a Senior Software Engineer.

Current Milestone: Data Sink & Lakehouse
Current Epic: Iceberg Integration
Current Task: Create Iceberg Table Definitions

Current Repository Structure:
```
streaming-lakehouse/
├── iceberg/
│   └── sql/
```

Requirements:
Create `iceberg/sql/create_tables.sql` with DDL statements for three Iceberg tables.

Table 1: `vehicle_events`
- id: BIGINT (event sequence or UUID)
- vehicle_id: VARCHAR
- event_time: TIMESTAMP(6) WITH TIME ZONE
- latitude: DOUBLE
- longitude: DOUBLE
- speed: DOUBLE
- rpm: INT
- fuel: DOUBLE
- engine_temp: DOUBLE
- battery_voltage: DOUBLE
- throttle_position: DOUBLE
- brake_pressure: DOUBLE
- steering_angle: DOUBLE
- processing_time: TIMESTAMP(6) WITH TIME ZONE
- Partitioned by: days(event_time)
- Properties: format_version=2, write_compression=ZSTD

Table 2: `vehicle_aggregations`
- window_start: TIMESTAMP(6)
- window_end: TIMESTAMP(6)
- vehicle_id: VARCHAR
- window_type: VARCHAR (tumbling, sliding, session)
- avg_speed: DOUBLE
- avg_rpm: DOUBLE
- max_engine_temp: DOUBLE
- total_distance: DOUBLE
- event_count: BIGINT
- Partitioned by: days(window_start)

Table 3: `vehicle_alerts`
- alert_id: BIGINT
- vehicle_id: VARCHAR
- alert_time: TIMESTAMP(6) WITH TIME ZONE
- rule_name: VARCHAR
- severity: VARCHAR
- current_value: DOUBLE
- message: VARCHAR
- Partitioned by: days(alert_time)

Constraints:
- Trino-compatible Iceberg SQL syntax
- All tables use Iceberg format
- Appropriate partitioning for time-series data
- Comments on each column
- Output ONLY iceberg/sql/create_tables.sql

Expected Output: `iceberg/sql/create_tables.sql`
```

### Prompt: M6-E2-T01 — Create Pipeline Metrics Dashboard

```
You are a Senior Software Engineer.

Current Milestone: Analytics & Observability
Current Epic: Grafana Dashboards
Current Task: Create Pipeline Metrics Dashboard JSON

Current Repository Structure:
```
streaming-lakehouse/
├── grafana/
│   └── dashboards/
```

Requirements:
Create `grafana/dashboards/pipeline_metrics.json` — a Grafana dashboard JSON model for monitoring the streaming pipeline.

Dashboard must include panels for:
1. Events/sec (rate of flink_taskmanager_job_task_operator_numRecordsIn)
2. Kafka Consumer Lag (kafka_consumer_lag)
3. Checkpoint Duration (flink_jobmanager_checkpoint_durationTime)
4. Processing Latency (custom metric or derived)
5. Watermark Delay (current processing time - max watermark)
6. Backpressure Status (flink_taskmanager_job_task_backPressuredTimeMsPerSecond)
7. Dead Letter Queue Rate
8. Validation Error Rate

Requirements:
- Dashboard title: "Streaming Pipeline Metrics"
- Datasource: Prometheus (use uid "${prometheus_ds}")
- Refresh: 5s
- Time range: Last 15 minutes
- Use stat panels for current values
- Use time series panels for trends
- Use thresholds and color coding (green/yellow/red)
- Tags: ["pipeline", "flink", "kafka"]

Constraints:
- Valid Grafana 10.x JSON model
- No placeholder queries
- All PromQL queries syntactically valid
- Output ONLY grafana/dashboards/pipeline_metrics.json

Expected Output: `grafana/dashboards/pipeline_metrics.json`
```

### Prompt: M7-E2-T01 — Create Chaos Test Script

```
You are a Senior Software Engineer.

Current Milestone: Production Hardening
Current Epic: Failure Recovery Demo
Current Task: Create Chaos Test Script

Current Repository Structure:
```
streaming-lakehouse/
├── tests/
│   └── chaos/
├── docker-compose.yml
```

Requirements:
Create `tests/chaos/test_recovery.py` — a chaos engineering test that verifies failure recovery.

Test scenarios:
1. TaskManager Kill: Stop the Flink TaskManager container, wait 30s, verify it restarts and job recovers
2. JobManager Kill: Stop the JobManager, wait 30s, verify job restarts from savepoint/checkpoint
3. Kafka Broker Unavailable: Pause Kafka container for 60s, verify Flink handles backpressure, resumes when Kafka returns
4. MinIO Outage: Pause MinIO for 60s, verify Iceberg sink buffers or fails gracefully

For each scenario:
- Record event count before failure
- Inject failure
- Wait for recovery
- Verify event count after recovery matches expected (no loss, no duplicates)
- Assert job state is RUNNING

Requirements:
- Use docker-py or subprocess to control containers
- Use KafkaConsumer to count events
- Use Trino query to count Iceberg rows
- Generate test report with pass/fail for each scenario
- Configurable via CLI arguments

Constraints:
- Python 3.12 with type hints
- pytest-compatible structure
- Comprehensive logging
- No hardcoded container names (read from env or docker-compose labels)
- Output ONLY tests/chaos/test_recovery.py

Expected Output: `tests/chaos/test_recovery.py`
```

---

# 9 Validation Checklist

## M1 — Infrastructure Foundation

### M1-E1-T02: docker-compose.yml Base
- **Build:** `docker compose up -d zookeeper kafka kafka-ui`
- **Run:** `docker compose ps`
- **Expected Output:** All services `healthy`
- **Verify:** `curl http://localhost:8080` returns Kafka UI HTML
- **Common Failures:** Port conflicts (change ports in .env), insufficient Docker memory (allocate > 4GB)

### M1-E3-T01: MinIO Service
- **Build:** `docker compose up -d minio`
- **Run:** `curl http://localhost:9000/minio/health/live`
- **Expected Output:** HTTP 200
- **Verify:** Log in to console at `http://localhost:9001`
- **Common Failures:** Bucket not initialized (run init script)

### M1-E4-T01: Flink JobManager
- **Build:** `docker compose up -d jobmanager taskmanager`
- **Run:** `curl http://localhost:8081/overview`
- **Expected Output:** JSON with Flink version and task slots
- **Verify:** UI shows slots > 0
- **Common Failures:** TaskManager cannot reach JobManager (check network/hostname)

## M2 — Data Ingestion

### M2-E3-T01: Simulator Integration
- **Build:** `docker compose up -d vehicle-simulator`
- **Run:** `docker logs -f streaming-lakehouse-vehicle-simulator-1`
- **Expected Output:** Logs showing event generation at configured TPS
- **Verify:** Kafka UI shows messages in `vehicle.telemetry`
- **Common Failures:** Kafka not reachable (check KAFKA_ADVERTISED_LISTENERS)

## M3 — Stream Processing Core

### M3-E1-T04: Flink Job Submission
- **Build:** `docker compose up -d flink-job`
- **Run:** `curl http://localhost:8081/jobs`
- **Expected Output:** JSON with job in RUNNING state
- **Verify:** Flink UI shows data flowing through operators
- **Common Failures:** Job fails immediately (check classpath for connector JARs)

### M3-E3-T02: Dead Letter Queue
- **Build:** Run simulator with invalid data (negative speed)
- **Run:** Check Kafka UI for `vehicle.deadletter`
- **Expected Output:** Messages in deadletter topic with error metadata
- **Verify:** Valid records still flow to main pipeline
- **Common Failures:** DLQ topic not created (run create_topics.py)

## M4 — Advanced Processing

### M4-E1-T01: Tumbling Windows
- **Build:** Submit Flink job with windowing enabled
- **Run:** Query Trino: `SELECT * FROM vehicle_aggregations LIMIT 10`
- **Expected Output:** Rows with window_start, window_end, avg_speed
- **Verify:** Window boundaries align to minute boundaries
- **Common Failures:** No output (check watermark generation)

### M4-E3-T02: Alert Publisher
- **Build:** Run simulator with high engine temp
- **Run:** Check Kafka UI for `vehicle.alerts`
- **Expected Output:** Alert messages with CRITICAL severity
- **Verify:** Alert format matches schema
- **Common Failures:** Alerts not firing (check threshold configuration)

## M5 — Lakehouse Sink

### M5-E1-T03: Events in Iceberg
- **Build:** Run pipeline for 5 minutes
- **Run:** Trino: `SELECT COUNT(*) FROM iceberg.default.vehicle_events`
- **Expected Output:** Count > 0 and increasing
- **Verify:** MinIO console shows objects in iceberg-warehouse bucket
- **Common Failures:** Catalog connection refused (check REST catalog URL)

### M5-E2-T04: Exactly-Once Verification
- **Build:** Run `tests/integration/test_exactly_once.py`
- **Run:** `pytest tests/integration/test_exactly_once.py -v`
- **Expected Output:** All assertions pass
- **Verify:** Row count in Iceberg matches Kafka offset
- **Common Failures:** Duplicates found (check transactional IDs are unique)

## M6 — Analytics

### M6-E1-T02: Trino Catalog
- **Build:** `docker compose up -d trino`
- **Run:** `trino --server localhost:8080 --catalog iceberg --schema default`
- **Expected Output:** Trino CLI connects
- **Verify:** `SHOW TABLES` lists vehicle_events, vehicle_aggregations, vehicle_alerts
- **Common Failures:** Catalog not found (check trino/catalog/iceberg.properties)

### M6-E2-T01: Grafana Dashboard
- **Build:** `docker compose up -d grafana`
- **Run:** Open `http://localhost:3000/d/pipeline-metrics`
- **Expected Output:** Dashboard loads with panels
- **Verify:** Panels show data (not "No data")
- **Common Failures:** Datasource not configured (check provisioning)

## M7 — Production Hardening

### M7-E2-T01: Chaos Test
- **Build:** Full stack running
- **Run:** `pytest tests/chaos/test_recovery.py -v --tb=short`
- **Expected Output:** 4 passed tests
- **Verify:** Report shows no data loss
- **Common Failures:** Job doesn't recover (check checkpoint directory permissions)

### M7-E3-T03: Integration Test
- **Build:** `pip install -r tests/requirements.txt`
- **Run:** `pytest tests/integration/ -v`
- **Expected Output:** All tests pass
- **Verify:** Coverage report > 80%
- **Common Failures:** Testcontainers timeout (increase startup timeout)

---

# 10 Testing Strategy

## Unit Tests

| Component | Test File | Coverage Target | Tools |
|-----------|-----------|-----------------|-------|
| Simulator | `tests/unit/test_simulator.py` | 85% | pytest, unittest.mock |
| Validation | `tests/unit/test_validation.py` | 90% | pytest |
| Aggregations | `tests/unit/test_aggregations.py` | 85% | pytest |
| Alerts | `tests/unit/test_alerts.py` | 85% | pytest |
| Config | `tests/unit/test_config.py` | 80% | pytest |

**Approach:**
- Mock external dependencies (Kafka, MinIO, Trino)
- Parametrize edge cases
- Use factories for test data generation

## Integration Tests

| Flow | Test File | Setup | Duration |
|------|-----------|-------|----------|
| Kafka → Flink | `tests/integration/test_pipeline.py` | testcontainers | < 5 min |
| Flink → Iceberg | `tests/integration/test_iceberg_sink.py` | testcontainers | < 5 min |
| Exactly-Once | `tests/integration/test_exactly_once.py` | docker compose | < 10 min |
| Trino Queries | `tests/integration/test_trino.py` | docker compose | < 3 min |

**Approach:**
- Spin up dependencies via testcontainers or docker compose
- Run simulator for fixed duration
- Assert row counts and data integrity

## Smoke Tests

| Check | Test File | Frequency |
|-------|-----------|-----------|
| Service Health | `tests/smoke/test_end_to_end.py` | On every deploy |
| Port Accessibility | `tests/smoke/test_ports.py` | On every deploy |
| Basic Query | `tests/smoke/test_queries.py` | On every deploy |

**Approach:**
- Fast (< 2 minutes total)
- No data verification, just connectivity
- Run in CI pipeline

## Performance Tests

| Scenario | Script | Metric |
|----------|--------|--------|
| Throughput | `tests/perf/test_throughput.py` | Events/sec sustained |
| Latency | `tests/perf/test_latency.py` | End-to-end p50/p99 |
| Checkpoint | `tests/perf/test_checkpoint.py` | Checkpoint duration vs state size |

**Approach:**
- Run for 10+ minutes
- Gradually increase TPS until backpressure
- Record saturation point

## Chaos Tests

| Scenario | Script | Injected Failure |
|----------|--------|------------------|
| TaskManager Kill | `tests/chaos/test_recovery.py::test_taskmanager_failure` | docker kill taskmanager |
| JobManager Kill | `tests/chaos/test_recovery.py::test_jobmanager_failure` | docker kill jobmanager |
| Kafka Pause | `tests/chaos/test_recovery.py::test_kafka_pause` | docker pause kafka |
| MinIO Pause | `tests/chaos/test_recovery.py::test_minio_pause` | docker pause minio |

**Approach:**
- Measure recovery time (RTO)
- Verify zero data loss (RPO = 0)
- Run nightly or weekly

---

# 11 Future Enhancements

## Must Have (Post-MVP)

| Feature | Priority | Effort | Dependencies |
|---------|----------|--------|--------------|
| REST API for analytics | High | 3 days | M6 complete |
| Authentication for Trino/Grafana | High | 2 days | M6 complete |
| CI/CD pipeline (GitHub Actions) | High | 2 days | M7 complete |

## Should Have

| Feature | Priority | Effort | Dependencies |
|---------|----------|--------|--------------|
| Vehicle route simulation (GeoJSON) | Medium | 3 days | M2 complete |
| Multi-topic ingestion (engine, weather) | Medium | 4 days | M3 complete |
| Schema Registry integration | Medium | 2 days | M2 complete |
| Kubernetes deployment manifests | Medium | 3 days | M7 complete |

## Nice To Have

| Feature | Priority | Effort | Dependencies |
|---------|----------|--------|--------------|
| AI-generated alert summaries (Ollama) | Low | 2 days | M4 complete |
| Grafana alerting notifications | Low | 1 day | M6 complete |
| Performance benchmarking suite | Low | 2 days | M7 complete |
| Terraform for cloud provisioning | Low | 3 days | M8 complete |

## Stretch Goals

| Feature | Priority | Effort | Dependencies |
|---------|----------|--------|--------------|
| Helm charts for K8s | Low | 3 days | K8s manifests |
| Cross-cloud deployment (AWS/GCP/Azure) | Low | 5 days | Terraform modules |
| Chaos mesh integration | Low | 2 days | K8s deployment |
| Real-time ML inference | Low | 5 days | M4 complete |

---

# 12 AI Development Workflow

## Recommended Workflow for AI-Assisted Development

```
┌─────────────────────────────────────────────────────────────┐
│ 1. READ PROJECT PLAN                                         │
│    └─ Review architecture, tech stack, and milestones        │
│                                                              │
│ 2. SELECT NEXT UNFINISHED TASK                               │
│    └─ Use dependency graph to find ready tasks               │
│    └─ Prioritize by milestone order                          │
│                                                              │
│ 3. PREPARE CONTEXT                                           │
│    └─ Gather all dependency files                            │
│    └─ Review acceptance criteria                             │
│    └─ Check existing code for patterns to follow             │
│                                                              │
│ 4. GENERATE CODE                                             │
│    └─ Use atomic task coding prompt                          │
│    └─ Request ONLY the target file(s)                        │
│                                                              │
│ 5. QUALITY CHECKS                                            │
│    ├─ Run ruff check {file}                                  │
│    ├─ Run ruff format {file}                                 │
│    ├─ Run mypy {file} (if type hints present)                │
│    └─ Run pytest tests/unit/ (if tests exist)                │
│                                                              │
│ 6. FIX FAILURES                                              │
│    └─ Iterate on code until all checks pass                  │
│    └─ Do not skip linting or type errors                     │
│                                                              │
│ 7. MANUAL VERIFICATION                                       │
│    └─ Follow validation checklist for the task               │
│    └─ Run build/run commands                                 │
│    └─ Verify expected output                                 │
│                                                              │
│ 8. COMMIT                                                    │
│    └─ Use conventional commit format                         │
│    └─ Reference task ID in commit message                    │
│    └─ Example: feat: add watermark strategy [M3-E2-T02]      │
│                                                              │
│ 9. MARK TASK COMPLETE                                        │
│    └─ Update project tracking (GitHub Issues)                │
│    └─ Move to next task                                      │
│                                                              │
│ 10. PERIODIC INTEGRATION                                     │
│     └─ After each milestone: run full integration tests      │
│     └─ After M7: run chaos tests                             │
│     └─ Update docs if behavior changed                       │
└─────────────────────────────────────────────────────────────┘
```

## Context Management Guidelines

1. **File Size Limit:** Keep files under 300 lines. Split large modules.
2. **Dependency Awareness:** Always provide the full repository tree and dependency file contents in prompts.
3. **Pattern Consistency:** Once a pattern is established (e.g., error handling, logging), enforce it in all subsequent tasks.
4. **No Regressions:** When editing existing files, include the full file content or use precise diffs.
5. **Test-Driven:** Write tests before or alongside implementation for complex logic.

## Prompt Engineering Tips

1. **Be Specific:** Include exact field names, types, and file paths.
2. **Provide Examples:** Include sample input/output in prompts.
3. **Define Boundaries:** Explicitly state "do not modify unrelated files."
4. **Acceptance First:** Lead with acceptance criteria, then implementation details.
5. **Incremental Delivery:** For complex tasks, split into smaller sub-prompts.

## Tooling Stack for AI Development

| Tool | Purpose | Command |
|------|---------|---------|
| ruff | Linting & formatting | `ruff check . && ruff format .` |
| mypy | Type checking | `mypy producer/ flink/` |
| pytest | Testing | `pytest tests/ -v --cov` |
| docker compose | Integration | `docker compose up -d --build` |
| trino-cli | SQL validation | `trino --f iceberg/sql/create_tables.sql` |

---

*End of Engineering Roadmap*
