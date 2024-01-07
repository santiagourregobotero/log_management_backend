from rest_framework import serializers
from .models import SysLog
from rest_framework.serializers import ValidationError

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysLog
        fields = ['id', 'timestamp', 'message', 'severity', 'source']
    
    def validate(self, data):
        if data["severity"] == data["message"]:
           raise ValidationError("Message & Severity must be different")
       
        return data
    
    def validate_message(self, value):
        if len(value) < 10:
           raise ValidationError("Message must be more than 10 char")
       
        if len(value) > 256:
           raise ValidationError("Message must be less than 256 char")
       
        return value
    
    def validate_severity(self, value):
        if len(value) < 3:
           raise ValidationError("Severity must be more than 3 char")
       
        if len(value) > 20:
           raise ValidationError("Severity must be less than 20 char")
       
        return value
    
    def validate_source(self, value):
        if len(value) < 3:
           raise ValidationError("Source must be more than 3 char")
       
        if len(value) > 50:
           raise ValidationError("Source must be less than 50 char")
       
        return value