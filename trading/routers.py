from django.urls import path
from .consumers import OHLCConsumer

websocket_urlpatterns = [
    path("ws/ohlc/", OHLCConsumer.as_asgi()),
]
