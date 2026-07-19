# Production-Grade Streaming Lakehouse
## Kafka + PyFlink + Apache Iceberg + MinIO + Trino + Grafana

---

# Goal

Build a production-inspired streaming data platform that demonstrates real-world data engineering concepts using only open-source technologies.

The project should showcase expertise in:

- Apache Kafka
- Apache Flink (PyFlink)
- Apache Iceberg
- MinIO
- Trino
- Docker
- Grafana
- Prometheus

No cloud services.
No Databricks.
Everything runs locally using Docker Compose.

---

# Why This Project?

Most portfolio projects stop at:

Producer
↓

Kafka
↓

Consumer

This project demonstrates production-grade concepts:

- Stateful stream processing
- Event-time processing
- Watermarks
- Windowing
- Exactly-once semantics
- Checkpointing
- Schema evolution
- Time travel
- Iceberg catalog
- Monitoring
- SQL analytics
- Dockerized deployment

---

# Architecture

                    Docker Network

┌──────────────────────────────────────────────────────────┐

Vehicle Simulator
        │
        ▼
     Kafka Broker
        │
        ▼
    PyFlink Job
        │
        │
        ├── Watermarks
        ├── Windows
        ├── Stateful Processing
        ├── Deduplication
        ├── Validation
        ├── Alerts
        │
        ▼
 Apache Iceberg Tables
        │
        ▼
      MinIO Storage
        │
        ▼
     Trino Queries
        │
        ▼
 Grafana Dashboard

└──────────────────────────────────────────────────────────┘

---

# Tech Stack

## Core

- Python 3.12
- PyFlink
- Kafka
- Apache Iceberg
- MinIO

## Infrastructure

- Docker
- Docker Compose

## Analytics

- Trino

## Monitoring

- Grafana
- Prometheus

---

# Folder Structure

streaming-lakehouse/

docker-compose.yml

README.md

PROJECT_PLAN.md

.env

docs/

architecture.png

producer/

simulator.py

config.py

flink/

main.py

schemas.py

processors.py

alerts.py

watermarks.py

windows.py

state.py

iceberg/

catalog/

warehouse/

sql/

create_tables.sql

queries.sql

grafana/

dashboards/

prometheus/

prometheus.yml

tests/

---

# Docker Containers

## Kafka

Purpose

Message Broker

---

## Kafka UI

Purpose

Inspect Topics

Consume Messages

Debug Streams

---

## PyFlink JobManager

Purpose

Coordinates jobs

---

## PyFlink TaskManager

Purpose

Runs stream processing

---

## MinIO

Purpose

S3 compatible object storage

Stores Iceberg data

---

## Iceberg REST Catalog

Purpose

Metadata catalog

---

## Trino

Purpose

SQL engine over Iceberg

---

## Grafana

Purpose

Visualization

---

## Prometheus

Purpose

Metrics

---

## Vehicle Simulator

Purpose

Generate streaming telemetry

---

# Development Roadmap

---

## Phase 1

Infrastructure

Goal

Everything starts successfully.

Tasks

- Docker Compose
- Kafka
- Kafka UI
- MinIO
- Iceberg Catalog
- PyFlink

Deliverable

docker compose up works

---

## Phase 2

Vehicle Simulator

Generate realistic telemetry.

Fields

VehicleId

Timestamp

Latitude

Longitude

Speed

RPM

Fuel

Engine Temperature

Battery Voltage

Throttle Position

Brake Pressure

Steering Angle

Example

{
 "vehicleId":"CAR001",
 "timestamp":"...",
 "speed":72,
 "rpm":2800,
 "fuel":61
}

Support

- configurable vehicles
- configurable TPS
- random delays
- duplicate events
- out-of-order events

Deliverable

Kafka topic continuously receives events

---

## Phase 3

Kafka

Topics

vehicle.telemetry

vehicle.alerts

vehicle.deadletter

Deliverable

Events flowing continuously

---

## Phase 4

PyFlink

Consume Kafka

Deserialize JSON

Assign timestamps

Create watermark strategy

Deliverable

Streaming pipeline operational

---

## Phase 5

Watermarks

Demonstrate

Late arrivals

Out-of-order events

Allowed lateness

Deliverable

Correct event-time processing

---

## Phase 6

Windowing

Implement

Tumbling Window

Sliding Window

Session Window

Examples

Average speed

Fuel consumption

Trip duration

Deliverable

Windowed aggregations

---

## Phase 7

Stateful Processing

Maintain

Previous GPS

Distance travelled

Current trip

Vehicle online/offline

Deliverable

State backend working

---

## Phase 8

Checkpointing

Checkpoint every

30 seconds

Demonstrate

Kill Flink

Restart

No data loss

Deliverable

Fault tolerance

---

## Phase 9

Exactly Once

Enable

Checkpointing

Kafka transactions

Iceberg sink

Deliverable

No duplicate rows

---

## Phase 10

Data Validation

Reject

Negative speed

Invalid timestamp

Missing vehicleId

Invalid coordinates

Write invalid records to

vehicle.deadletter

Deliverable

Data quality pipeline

---

## Phase 11

Alerts

Rules

Temperature >110°C

Battery Voltage <11V

Overspeed

Fuel <5%

Publish

vehicle.alerts

Deliverable

Real-time alerting

---

## Phase 12

Apache Iceberg

Create

vehicle_events

vehicle_alerts

Store

Raw events

Aggregations

Alerts

Deliverable

Iceberg tables populated

---

## Phase 13

Iceberg Features

Demonstrate

Schema Evolution

Time Travel

Snapshots

Partition Evolution

Hidden Partitioning

Compaction

Deliverable

Production Iceberg functionality

---

## Phase 14

SQL

Query with Trino

Examples

Top fastest vehicles

Average speed

Fuel usage

Alerts

Trips

Deliverable

Analytics layer

---

## Phase 15

Monitoring

Grafana dashboards

Metrics

Events/sec

Kafka Lag

Checkpoint Duration

Processing Latency

Watermark Delay

Alerts

Deliverable

Operational dashboard

---

## Phase 16

Failure Recovery Demo

Scenario

Kill TaskManager

Restart

Observe

State restored

No duplicates

No data loss

Deliverable

Production-grade demo

---

# Nice-to-Have Features

## Vehicle Routes

Simulate actual GPS paths

---

## REST API

Expose analytics

---

## Authentication

Secure Trino

---

## Multi-topic ingestion

Engine

GPS

Diagnostics

Weather

---

## AI Extension

Use local Ollama

Generate natural language alerts

Example

"Vehicle CAR-102 has exceeded safe engine temperatures for the past 15 minutes."

---

# Stretch Goals

- Kubernetes deployment
- Helm charts
- CI/CD with GitHub Actions
- Terraform
- Integration tests
- Performance benchmarking
- Chaos testing

---

# Skills Demonstrated

✓ Kafka

✓ PyFlink

✓ Docker

✓ Apache Iceberg

✓ MinIO

✓ Trino

✓ Grafana

✓ Prometheus

✓ Event Time

✓ Watermarks

✓ Windowing

✓ Stateful Streaming

✓ Checkpointing

✓ Exactly Once

✓ Fault Tolerance

✓ Data Validation

✓ Dead Letter Queue

✓ Monitoring

✓ SQL Analytics

✓ Production Architecture

---

# Deliverables

README.md

Architecture Diagram

Docker Compose

Complete Source Code

Sample Data Generator

Screenshots

Grafana Dashboard

SQL Queries

Documentation

Failure Recovery Demo

Architecture Walkthrough Video (optional)

---

# Future Cloud Version

Once the local version is complete, migrate the same architecture to:

Kafka → Azure Event Hub

MinIO → ADLS Gen2

Iceberg → Unity Catalog

Trino → Databricks SQL

Docker → Kubernetes

This demonstrates that the architecture is cloud-agnostic while preserving the same core design.