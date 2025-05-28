from rest_framework import serializers

class RedisUserSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    data = serializers.JSONField()