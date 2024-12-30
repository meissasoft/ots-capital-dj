from rest_framework import serializers


class SaveQuotesSerializer(serializers.Serializer):
    api_url = serializers.CharField()

    class Meta:
        fields = ["api_url"]
