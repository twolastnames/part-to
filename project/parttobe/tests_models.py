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


class CollectionOuterDutyTestClass(TestCase):
    def setUp(self):
        get_task_definitions.cache_clear()

    @classmethod
    def setUpClass(cls):
        super(CollectionOuterDutyTestClass, cls).setUpClass()
        part_to = PartTo.objects.create(name="My Part To")
        CollectionOuterDutyTestClass.part_to = part_to
        CollectionOuterDutyTestClass.task1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=1),
            part_to=part_to,
            description="do task1",
        )
        CollectionOuterDutyTestClass.task2 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=2),
            part_to=part_to,
            description="do task2",
            depended=CollectionOuterDutyTestClass.task1,
        )
        CollectionOuterDutyTestClass.task3 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=2),
            part_to=part_to,
            description="do task3",
            depended=CollectionOuterDutyTestClass.task2,
        )
        CollectionOuterDutyTestClass.duty1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(seconds=30),
            part_to=part_to,
            description="do duty1",
            depended=CollectionOuterDutyTestClass.task1,
            engagement=10,
        )

    def test_calculating_overflowing_task_duractions(self):
        self.assertEqual(
            TaskDefinition.duration_to(CollectionOuterDutyTestClass.task1),
            datetime.timedelta(minutes=5, seconds=30),
        )

    def test_sorting_tasks(self):
        task1 = CollectionOuterDutyTestClass.task1
        task2 = CollectionOuterDutyTestClass.task2
        task3 = CollectionOuterDutyTestClass.task3
        duty1 = CollectionOuterDutyTestClass.duty1
        all = list(CollectionOuterDutyTestClass.part_to.task_definitions)
        self.assertEqual(task1 > task2, True)
        self.assertEqual(task1 > duty1, True)
        self.assertEqual(task1 < task2, False)
        self.assertEqual(task1 < duty1, False)
        self.assertEqual(task2 > task3, True)
        all.sort()
        forward = list(map(lambda task: task.description, all))
        self.assertEqual(forward, ["do duty1", "do task3", "do task2", "do task1"])
        all.reverse()
        backward = list(map(lambda task: task.description, all))
        self.assertEqual(backward, ["do task1", "do task2", "do task3", "do duty1"])


class CollectionInnerDutyTestClass(TestCase):
    def setUp(self):
        get_task_definitions.cache_clear()

    @classmethod
    def setUpClass(cls):
        super(CollectionInnerDutyTestClass, cls).setUpClass()
        part_to = PartTo.objects.create(name="My Part To")
        CollectionInnerDutyTestClass.part_to = part_to
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
        CollectionInnerDutyTestClass.duty1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(seconds=30),
            part_to=part_to,
            description="do duty1",
            depended=CollectionInnerDutyTestClass.task2,
            engagement=10,
        )

    def test_calculating_overflowing_task_duractions(self):
        self.assertEqual(
            TaskDefinition.chain_duration(CollectionInnerDutyTestClass.duty1),
            datetime.timedelta(minutes=3, seconds=3),
        )

    def test_calculating_underflowing_task_duractions(self):
        duty1 = CollectionInnerDutyTestClass.duty1
        duty1.initial_duration = datetime.timedelta(minutes = 5)
        self.assertEqual(
            TaskDefinition.chain_duration(CollectionInnerDutyTestClass.duty1),
            datetime.timedelta(minutes=3, seconds=30),
        )


    def test_sorting_tasks(self):
        task1 = CollectionInnerDutyTestClass.task1
        task2 = CollectionInnerDutyTestClass.task2
        duty1 = CollectionInnerDutyTestClass.duty1
        all = list(CollectionInnerDutyTestClass.part_to.task_definitions)
        self.assertEqual(task1 > task2, True)
        self.assertEqual(task1 > duty1, True)
        self.assertEqual(task1 < task2, False)
        self.assertEqual(task1 < duty1, False)
        all.sort()
        forward = list(map(lambda task: task.description, all))
        self.assertEqual(forward, ["do duty1", "do task2", "do task1"])
        all.reverse()
        backward = list(map(lambda task: task.description, all))
        self.assertEqual(backward, ["do task1", "do task2", "do duty1"])
