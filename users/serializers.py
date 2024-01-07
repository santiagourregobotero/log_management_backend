from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name']

        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password', None))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(validated_data.get('password', None))

        instance.save()
        return instance