from rest_framework import serializers


class LoginValidationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=False)
    password = serializers.CharField(max_length=255, required=False)

    def validate(self, attrs):
        if attrs.get("email", None) == None:
            raise serializers.ValidationError("email is required")
        if attrs.get("password", None) == None:
            raise serializers.ValidationError("password is required")
        return attrs
    
    
class TokenValidationSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=255, required=False)

    def validate(self, attrs):
        if attrs.get("access_token", None) == None:
            raise serializers.ValidationError("token is required")
        return attrs