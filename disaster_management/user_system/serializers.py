from rest_framework import serializers
from django.contrib.auth.models import User
from user_system.models import CustomUser
from datetime import datetime

class RedisUserSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(read_only=True)
    data = serializers.JSONField()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name','last_name','email', 'password', 'confirm_password', 'last_login']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password', None)
        validated_data['last_login'] = datetime.now()
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

        

