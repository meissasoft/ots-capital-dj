from asgiref.sync import async_to_sync
from .websocket_client import consume_quotes, format_websocket_url
from rest_framework.response import Response
from rest_framework.views import APIView
from threading import Thread
from drf_yasg.utils import swagger_auto_schema
from .serializers import SaveQuotesSerializer


def start_websocket_client(ws_url):
    async_to_sync(consume_quotes)(ws_url)


class SaveQuotes(APIView):
    @swagger_auto_schema(
        request_body=SaveQuotesSerializer,
        operation_description="Save quotes from the provided API URL.",
    )
    def post(self, request):
        api_url = request.data.get("api_url")
        ws_url = format_websocket_url(api_url)
        if ws_url:
            try:
                thread = Thread(target=start_websocket_client, args=(ws_url,))
                thread.start()
                return Response({"message": "Started consuming quotes"}, status=200)
            except Exception as e:
                print(f"Error: {e}")
                return Response({"message": f"Error: {e}"}, status=500)
        else:
            print("Failed to fetch WebSocket URL.")
            return Response({"message": "Failed to fetch WebSocket URL."}, status=400)
