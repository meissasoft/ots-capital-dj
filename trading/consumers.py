from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import OHLC
import logging

logger = logging.getLogger(__name__)


@sync_to_async
def get_ohlc_data(symbol, timeframe):
    logger.debug(f"Fetching OHLC data for symbol: {symbol}, timeframe: {timeframe}")
    return list(
        OHLC.objects.filter(symbol=symbol, timeframe=timeframe).order_by("timestamp")
    )


class OHLCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("WebSocket connection accepted")
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket connection closed with code: {close_code}")

    async def receive(self, text_data):
        logger.debug(f"Received message: {text_data}")

        # Parse received message
        data = json.loads(text_data)
        symbol = data.get("symbol")
        timeframe = data.get("timeframe", "1m")

        logger.info(f"Received request for symbol: {symbol}, timeframe: {timeframe}")

        # Fetch OHLC data from the database
        ohlc_data = await get_ohlc_data(symbol, timeframe)

        ohlc_list = [
            {
                "timestamp": ohlc.timestamp.isoformat(),
                "open": ohlc.open_price,
                "high": ohlc.high_price,
                "low": ohlc.low_price,
                "close": ohlc.close_price,
                "volume": ohlc.volume,
            }
            for ohlc in ohlc_data
        ]

        logger.debug(f"Sending OHLC data: {ohlc_list}")

        # Send the OHLC data to the WebSocket client
        await self.send(text_data=json.dumps({"data": ohlc_list}))
