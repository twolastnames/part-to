from django.test import TestCase
from parttobe.models import PartTo
from parttobe.models import TaskDefinition
from parttobe.models import get_task_definitions

import datetime


class CollectionTaskTestClass(TestCase):
    def setUp(self):
        get_task_definitions.cache_clear()
    @classmethod
    def setUpClass(cls):
        super(CollectionTaskTestClass, cls).setUpClass()
        part_to = PartTo.objects.create(name="My Part To")
        CollectionTaskTestClass.task1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=1),
            part_to=part_to,
            description="do task1",
        )
        CollectionTaskTestClass.task2 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=2),
            part_to=part_to,
            description="do task2",
            depended=CollectionTaskTestClass.task1,
        )
        CollectionTaskTestClass.task3 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=2),
            part_to=part_to,
            description="do task3",
            depended=CollectionTaskTestClass.task2,
        )

    def test_calculating_task_duractions(self):
        self.assertEqual(
            TaskDefinition.chain_duration(CollectionTaskTestClass.task3),
            datetime.timedelta(minutes=5),
        )

    def test_sorting_dual_dependency_tasks(self):
        task1 = CollectionTaskTestClass.task1
        task2 = CollectionTaskTestClass.task2
        task3 = CollectionTaskTestClass.task3
        task4 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=3),
            part_to=task1.part_to,
            description="do task4",
            depended=CollectionTaskTestClass.task2,
        )
        all = [
            task1,
            task4,
            task3,
            task2,
        ]
        self.assertEqual(task1 >= task4, True)
        self.assertEqual(task1 <= task4, False)
        self.assertEqual(task1 > task4, True)
        self.assertEqual(task1 < task4, False)
        all.sort()
        forward = list(map(lambda task: task.description, all))
        self.assertEqual(forward, ["do task3", "do task4", "do task2", "do task1"])
        all.reverse()
        backward = list(map(lambda task: task.description, all))
        self.assertEqual(backward, ["do task1", "do task2", "do task4", "do task3"])

    def test_dependency_chain_from(self):
        chain_from = TaskDefinition.dependency_chain_from(CollectionTaskTestClass.task1)
        result = list(map(lambda task: task.description, chain_from))
        self.assertEquals(result, ["do task1", "do task2", "do task3"])

    def test_dual_short_dependency_chain_from(self):
        task4 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(seconds=3),
            part_to=CollectionTaskTestClass.task1.part_to,
            description="do task4",
            depended=CollectionTaskTestClass.task2,
        )
        chain_from = TaskDefinition.dependency_chain_from(CollectionTaskTestClass.task1)
        result = list(map(lambda task: task.description, chain_from))
        self.assertEquals(result, ["do task1", "do task2", "do task3", "do task4"])

    def test_dual_long_dependency_chain_from(self):
        task4 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=3),
            part_to=CollectionTaskTestClass.task1.part_to,
            description="do task4",
            depended=CollectionTaskTestClass.task2,
        )
        chain_from = TaskDefinition.dependency_chain_from(CollectionTaskTestClass.task1)
        result = list(map(lambda task: task.description, chain_from))
        self.assertEquals(result, ["do task1", "do task2", "do task4", "do task3"])

    def test_sorting_tasks(self):
        task1 = CollectionTaskTestClass.task1
        task2 = CollectionTaskTestClass.task2
        task3 = CollectionTaskTestClass.task3
        all = [task1, task3, task2]
        self.assertEqual(task1 > task2, True)
        self.assertEqual(task1 < task2, False)
        self.assertEqual(task1 > task3, True)
        self.assertEqual(task1 < task3, False)
        self.assertEqual(task2 > task3, True)
        self.assertEqual(task2 < task3, False)
        self.assertEqual(task1 >= task2, True)
        self.assertEqual(task1 <= task2, False)
        self.assertEqual(task2 <= task2, True)
        self.assertEqual(task2 >= task2, True)
        self.assertEqual(task3 <= task3, True)
        self.assertEqual(task3 >= task3, True)
        all.sort()
        forward = list(map(lambda task: task.description, all))
        self.assertEqual(forward, ["do task3", "do task2", "do task1"])
        all.reverse()
        backward = list(map(lambda task: task.description, all))
        self.assertEqual(backward, ["do task1", "do task2", "do task3"])


class CollectionInnerDutyTestClass(TestCase):
    @classmethod
    def setUpClass(cls):
        super(CollectionInnerDutyTestClass, cls).setUpClass()
        part_to = PartTo.objects.create(name="My Part To")
        CollectionInnerDutyTestClass.task1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=1),
            part_to=part_to,
            description="do task1",
        )
        CollectionInnerDutyTestClass.task2 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=2),
            part_to=part_to,
            description="do task2",
            depended=CollectionInnerDutyTestClass.task1,
        )
        CollectionInnerDutyTestClass.task3 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=2),
            part_to=part_to,
            description="do task3",
            depended=CollectionInnerDutyTestClass.task2,
        )
        CollectionInnerDutyTestClass.duty1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(seconds=30),
            part_to=part_to,
            description="do duty1",
            depended=CollectionInnerDutyTestClass.task1,
        )

    def test_calculating_task_duractions(self):
        self.assertEqual(
            TaskDefinition.chain_duration(CollectionInnerDutyTestClass.task3),
            datetime.timedelta(seconds=30, minutes=5),
        )

    def test_sorting_tasks(self):
        task1 = CollectionInnerDutyTestClass.task1
        task2 = CollectionInnerDutyTestClass.task2
        task3 = CollectionInnerDutyTestClass.task3
        duty1 = CollectionInnerDutyTestClass.duty1
        all = [task1, task3, task2, duty1]
        self.assertEqual(task1 < task2, True)
        all.sort()
        forward = list(map(lambda task: task.description, all))
        self.assertEqual(forward, ["do task1", "do task2", "do duty1", "do task3"])
        all.reverse()
        backward = list(map(lambda task: task.description, all))
        self.assertEqual(backward, ["do task3", "do duty1", "do task2", "do task1"])
