from rest_framework.test import APITestCase
from rest_framework import status
from .models import SysLog
import json

token = 'yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJhZG1pbkBnbWFpbC5jb20iLCJleHAiOjE3MDk1NzMyMzQsImlhdCI6MTcwNDM4OTIzNH0.u7-r_hSmVkQ8LHGAf4a6Tk-6HCd4bQXfdPhb5KYlbHE'
headers = {'HTTP_AUTHORIZATION': f'Bearer {token}', 'content_type': 'application/json'}

class SysLogAPITest(APITestCase):
    def test_create_log(self):
        data = json.dumps({
            "timestamp": "2024-01-05 02:25:34",
            "message": "MESSAGE_MESSAGE",
            "severity": "INFO",
            "source": "Google"
        })
        response = self.client.post('/api/logs', data=data, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_validate_message(self):
        data = json.dumps({
            "timestamp": "2024-01-05 02:25:34",
            "message": "MESSAGE",
            "severity": "INFO",
            "source": "Google"
        })
        response = self.client.post('/api/logs', data=data, **headers)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"message":["Message must be more than 10 char"]})
        
        data = json.dumps({
            "timestamp": "2024-01-05 02:25:34",
            "message": "MESSAGE"*100,
            "severity": "INFO",
            "source": "Google"
        })
        response = self.client.post('/api/logs', data=data, **headers)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"message":["Ensure this field has no more than 255 characters."]})
        
    def test_validate(self):
        data = json.dumps({
            "timestamp": "2024-01-05 02:25:34",
            "message": "INFO_INFO_INFO",
            "severity": "INFO_INFO_INFO",
            "source": "INFO"
        })
        response = self.client.post('/api/logs', data=data, **headers)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"non_field_errors":["Message & Severity must be different"]})
        
    def test_aggregate_log(self):
        response = self.client.get('/api/logs/analytics?start_date=2024-01-01&end_date=2025-01-01&constraint=source', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
class SysLogAPIIntegrationTest(APITestCase):
    
    def test_create_log(self):
        data = json.dumps({
            "timestamp": "2024-01-05 02:25:34",
            "message": "MESSAGE_MESSAGE",
            "severity": "INFO",
            "source": "Google"
        })
        response = self.client.post('/api/logs', data=data, **headers)
        
        
        print(str(response.content, encoding='utf8'))
        self.assertContains(response, 'MESSAGE_MESSAGE', status_code=status.HTTP_201_CREATED)