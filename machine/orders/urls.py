from django.urls import path
from . import views

urlpatterns = [
    path("order/", views.create_order, name="create-order"),
    path("order/<str:order_id>/", views.order_result, name="order-result"),
]