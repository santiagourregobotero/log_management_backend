from rest_framework import serializers

class MessageResponseSerializer(serializers.Serializer):
    msg = serializers.CharField(max_length=255)
