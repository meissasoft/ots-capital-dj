import pandas as pd
import asyncio
import websockets
import json
from asgiref.sync import sync_to_async
from .models import OHLC
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

ohlc_data = {}


def format_websocket_url(uri):
    # Remove "http://" or "https://" from the URL
    if uri.startswith("http://"):
        return uri.replace("http://", "ws://")
    elif uri.startswith("https://"):
        return uri.replace("https://", "wss://")
    return uri  # Return as-is if no prefix is found


async def consume_quotes(ws_url, timeframe):
    logger.info(f"Connecting to WebSocket URL: {ws_url}")
    async with websockets.connect(ws_url) as websocket:
        while True:
            try:
                # Receive real-time data
                message = await websocket.recv()
                data = json.loads(message)
                logger.debug(f"Received data: {data}")
                await process_quote(data, timeframe)
            except Exception as e:
                logger.error(f"Error in WebSocket connection: {e}")
                await asyncio.sleep(5)  # Retry on failure


async def process_quote(data, timeframe):
    if data["type"] != "Quote":
        logger.debug(f"Ignored non-quote data: {data}")
        return

    symbol = data["data"]["symbol"]
    price = data["data"]["bid"]  # Use "bid" or customize for OHLC logic
    timestamp = pd.to_datetime(data["data"]["time"])

    logger.info(f"Processing quote for symbol: {symbol}, price: {price}, timestamp: {timestamp}")

    # Ensure symbol entry in ohlc_data
    if symbol not in ohlc_data:
        ohlc_data[symbol] = []

    # Append new data
    ohlc_data[symbol].append({"price": price, "timestamp": timestamp})

    # Resample and save data to the database
    await resample_and_save(symbol, timeframe)


@sync_to_async
def resample_and_save(symbol, timeframe):
    df = pd.DataFrame(ohlc_data[symbol])
    if df.empty:
        logger.warning(f"No data to resample for symbol: {symbol}")
        return

    # Resample into 1-minute OHLC
    df.set_index("timestamp", inplace=True)
    ohlc_resampled = df["price"].resample(timeframe).ohlc()

    logger.info(f"Resampled OHLC data for symbol: {symbol} with timeframe: {timeframe}")

    # Save to the database
    for timestamp, row in ohlc_resampled.iterrows():
        if timestamp:
            timestamp = timezone.make_aware(timestamp.to_pydatetime())
        OHLC.objects.update_or_create(
            symbol=symbol,
            timeframe=timeframe,
            timestamp=timestamp,
            defaults={
                "open_price": row["open"],
                "high_price": row["high"],
                "low_price": row["low"],
                "close_price": row["close"],
            },
        )
        logger.debug(f"Saved OHLC data for symbol: {symbol}, timestamp: {timestamp}")

    # Clear cached data for this symbol after processing
    ohlc_data[symbol] = []
    logger.info(f"Cleared cached data for symbol: {symbol}")
