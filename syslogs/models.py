from django.db import models

# Create your models here.
import logging

class SysLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    severity = models.CharField(max_length=20)
    source = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.timestamp} - {self.severity} - {self.source}"