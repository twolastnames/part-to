from django.test import TestCase
from django.test import Client
import json


class HelloWorldTestCase(TestCase):
    def test_hello_world(self):
        client = Client()
        response = client.get("/api/hello-world/", format="json")
        self.assertEqual(json.loads(response.content), {"message": "Hello, world!"})


class JobTestClass(TestCase):
    def test_get_job_set(self):
        client = Client()
        response = client.post(
            "/api/job",
            json.dumps(
                {
                    jobIds: ["job1", "job2"],
                }
            ),
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": "someId",
                "report": "2024-03-29 15:29:10.418159",
                "task": "taskId2",
                "duties": ["dutyId1", "dutyId2"],
            },
        )

    def test_get_job_report(self):
        client = Client()
        response = client.get("/api/job/someId", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": "someId",
                "report": "2024-03-29 15:29:10.418159",
                "task": "taskId2",
                "duties": ["dutyId1", "dutyId2", "dutyId3"],
            },
        )


class TaskTestClass(TestCase):
    def test_get_running_task(self):
        client = Client()
        response = client.get("/api/task/someID", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "description": "Hello, world!",
                "status": "running",
                "projectedSeconds": 77.7,
            },
        )

    def test_get_waiting_task(self):
        client = Client()
        response = client.get("/api/task/someID", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "description": "Hello, world!",
                "status": "waiting",
                "projectedSeconds": 77.7,
            },
        )

    def test_patch_complete_task(self):
        client = Client()
        response = client.patch(
            "/api/task/taskId1", json.dumps({"status": "complete"}), format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": "someId",
                "report": "2024-03-29 15:29:10.418159",
                "task": "taskId2",
                "duties": ["dutyId1", "dutyId2"],
            },
        )

    def test_patch_complete_task_new_duty(self):
        client = Client()
        response = client.patch(
            "/api/task/taskId3", json.dumps({"status": "complete"}), format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": "someId",
                "report": "2024-03-29 15:29:10.418159",
                "task": "taskId4",
                "duties": ["dutyId1", "dutyId2", "dutyId3"],
            },
        )


class DutyTestClass(TestCase):
    def test_get_duty(self):
        client = Client()
        response = client.get("/api/duty/someId", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "description": "Do something cool",
                "projectedSeconds": 55.7,
            },
        )

    def test_patch_complete_duty(self):
        client = Client()
        response = client.patch(
            "/api/duty/duty1",
            json.dumps(
                {
                    "status": "complete",
                    "duration": 888.88,
                }
            ),
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": "someId",
                "report": "2024-03-29 15:29:10.418159",
                "task": "taskId1",
                "duties": ["dutyId2"],
            },
        )
