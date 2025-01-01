from rest_framework import serializers


class SaveQuotesSerializer(serializers.Serializer):
    api_url = serializers.CharField()
    timeframe = serializers.CharField(default="1m")

    class Meta:
        fields = ["api_url", "timeframe"]
