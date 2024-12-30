from django.db import models


class OHLC(models.Model):
    symbol = models.CharField(max_length=10)
    timeframe = models.CharField(max_length=10, default="1m")
    timestamp = models.DateTimeField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.FloatField(default=0.0)

    class Meta:
        unique_together = ("symbol", "timeframe", "timestamp")  # Prevent duplicates
        indexes = [
            models.Index(fields=["symbol", "timeframe", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.symbol} {self.timeframe} {self.timestamp}"
