# Asynchronous Order Processor (Django + Celery + RabbitMQ + Redis)

## Features
- Asynchronous background order processing  
- RabbitMQ as Celery message broker  
- Redis as result storage (with TTL)  
- Retry logic with exponential backoff for transient errors  

## Prerequisites
- Python 3.11+  
- RabbitMQ installed and running on `localhost:5672`  
- Redis installed and running on `localhost:6379`  

## Setup & Installation

### 1. Clone the repository and create a virtual environment
```bash
git clone https://github.com/Anup-Soni2511/machine_round_python.git
cd machine_round_python
cd machine
python -m venv venv
venv\Scripts\activate   # on Windows
source venv/bin/activate # on Linux/Mac
pip install -r requirements.txt


### Running the System

Open two terminals:

1. Django server

python manage.py runserver 8001

2. Celery worker

On Linux/Mac:

celery -A machine worker -l info


On Windows (use solo pool to avoid errors):

celery -A machine worker -l info -P solo



Usage
Create an order
curl -X POST http://127.0.0.1:8001/order/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": "123", "items": ["apple", "banana", "orange"]}'


Response:

{ "task_id": "c4f3c04e-12aa-4d9e-890a-d35d7c4fa7c3" }

Check order status
curl http://127.0.0.1:8001/order/123/


While processing:

{ "order_id": "123", "status": "processing" }


Once finished:

{ "order_id": "123", "items_count": 3, "status": "processed" }