import json
import random
import time
import redis
from celery import shared_task
from django.conf import settings
from typing import List

import logging
logger = logging.getLogger(__name__)

# Redis client (module-level singleton)
redis_client = redis.Redis.from_url(settings.REDIS_URL)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True, max_retries=3)
def process_order(self, order_id: str, items: List[str]):
    """
    Simulates processing an order by iterating items with short delays.
    Computes total items and writes result to Redis with TTL.

    Retry logic:
    - 5% random chance to fail per item to exercise retries.
    """
    for _ in items:
        time.sleep(0.5)
        if random.random() < 0.05:
            raise RuntimeError("Transient error while processing items")

    result = {
        "order_id": order_id,
        "items_count": len(items),
        "status": "processed",
    }
    logger.warning(f"Started task for order_id={order_id}, items={items}")

    key = f"order:{order_id}"
    ttl = settings.REDIS_TTL_SECONDS
    redis_client.setex(key, ttl, json.dumps(result))
    logger.warning(f"Finished task for order_id={order_id}")

    # Return is optional (we don't use Celery's result backend)
    return result