import json
import redis
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .tasks import process_order

# Redis client for API reads
redis_client = redis.Redis.from_url(settings.REDIS_URL)

@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    """
    POST /order/
    Body:
    {
      "order_id": "1",
      "items": ["anup", "soni"]
    }
    Returns:
    { "task_id": "<celery_task_id>" }
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    order_id = payload.get("order_id")
    items = payload.get("items")

    # if not isinstance(order_id, str) or not isinstance(items, list):
    #     return JsonResponse(
    #         {"error": "order_id must be string and items must be list of strings"},
    #         status=400,
    #     )
    if not all(isinstance(i, str) for i in items):
        return JsonResponse({"error": "items must be list of strings"}, status=400)


    task = process_order.delay(order_id, items)
    return JsonResponse({"task_id": task.id}, status=202)

@require_http_methods(["GET"])
def order_result(request, order_id: str):
    """
    GET /order/<order_id>/
    Returns the result from Redis if ready, else "processing".
    """
    key = f"order:{order_id}"
    data = redis_client.get(key)

    if data is None:
        return JsonResponse({"order_id": order_id, "status": "processing"}, status=200)

    try:
        doc = json.loads(data)
        return JsonResponse(doc, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"order_id": order_id, "status": "processing"}, status=200)