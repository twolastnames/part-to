from django.test import TestCase
from django.test import Client
import json

class HelloWorldTestCase(TestCase):
    def test_hello_world(self):
        client = Client()
        response = client.get('/api/hello-world/', format='json')
        self.assertEqual(json.loads(response.content), {'message': 'Hello, world!'})

class JobTestClass(TestCase):
    def test_get_job_set(self):
        client = Client()
        response = client.get('/api/job/jobName', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'message': 'Hello, world!'})

    def test_get_job(self):
        client = Client()
        response = client.get('/api/job/jobName', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'message': 'Hello, world!'})

class TaskTestClass(TestCase):
    def test_get_task(self):
        client = Client()
        response = client.get('/api/task/someID', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'message': 'Hello, world!'})

class DutyTestClass(TestCase):
    def test_get_duty(self):
        client = Client()
        response = client.get('/api/duty/someId', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'message': 'Hello, world!'})



