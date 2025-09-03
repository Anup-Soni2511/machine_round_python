# Asynchronous Order Processor (Django + Celery + RabbitMQ + Redis)

This app exposes:
- POST /order/ → Enqueue a Celery task using RabbitMQ broker
- GET /order/<order_id>/ → Fetch processed result from Redis (with TTL)

The Celery task simulates processing, includes retry logic, and stores results in Redis under key `order:<order_id>`.

## Prerequisites
- Python 3.11+
- Docker (for RabbitMQ + Redis)
- Create `.env` from `.env.example` and edit as needed.

## 1) Start RabbitMQ and Redis

```bash
docker compose up -d
# RabbitMQ UI: http://localhost:15672  (user: guest / pass: guest)
# AMQP broker: amqp://guest:guest@localhost:5672//
# Redis: redis://localhost:6379/0