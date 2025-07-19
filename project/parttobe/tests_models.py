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
            CollectionTaskTestClass.task3.chain_duration(),
            datetime.timedelta(minutes=5),
        )

    def test_sorting_dual_dependency_tasks(
        self,
    ):
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
        forward = list(
            map(
                lambda task: task.description,
                all,
            )
        )
        self.assertEqual(
            forward,
            [
                "do task3",
                "do task4",
                "do task2",
                "do task1",
            ],
        )
        all.reverse()
        backward = list(
            map(
                lambda task: task.description,
                all,
            )
        )
        self.assertEqual(
            backward,
            [
                "do task1",
                "do task2",
                "do task4",
                "do task3",
            ],
        )

    def test_dependency_chain_from(self):
        chain_from = CollectionTaskTestClass.task1.dependency_chain_from()
        result = list(
            map(
                lambda task: task.description,
                chain_from,
            )
        )
        self.assertEquals(
            result,
            [
                "do task1",
                "do task2",
                "do task3",
            ],
        )

    def test_dual_short_dependency_chain_from(
        self,
    ):
        task4 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(seconds=3),
            part_to=CollectionTaskTestClass.task1.part_to,
            description="do task4",
            depended=CollectionTaskTestClass.task2,
        )
        chain_from = CollectionTaskTestClass.task1.dependency_chain_from()
        result = list(
            map(
                lambda task: task.description,
                chain_from,
            )
        )
        self.assertEquals(
            result,
            [
                "do task1",
                "do task2",
                "do task3",
                "do task4",
            ],
        )

    def test_dual_long_dependency_chain_from(
        self,
    ):
        task4 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=3),
            part_to=CollectionTaskTestClass.task1.part_to,
            description="do task4",
            depended=CollectionTaskTestClass.task2,
        )
        chain_from = CollectionTaskTestClass.task1.dependency_chain_from()
        result = list(
            map(
                lambda task: task.description,
                chain_from,
            )
        )
        self.assertEquals(
            result,
            [
                "do task1",
                "do task2",
                "do task4",
                "do task3",
            ],
        )

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
        forward = list(
            map(
                lambda task: task.description,
                all,
            )
        )
        self.assertEqual(
            forward,
            [
                "do task3",
                "do task2",
                "do task1",
            ],
        )
        all.reverse()
        backward = list(
            map(
                lambda task: task.description,
                all,
            )
        )
        self.assertEqual(
            backward,
            [
                "do task1",
                "do task2",
                "do task3",
            ],
        )


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

    def test_calculating_overflowing_task_duractions(
        self,
    ):
        self.assertEqual(
            CollectionOuterDutyTestClass.task1.duration_to(),
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
        forward = list(
            map(
                lambda task: task.description,
                all,
            )
        )
        self.assertEqual(
            forward,
            [
                "do duty1",
                "do task3",
                "do task2",
                "do task1",
            ],
        )
        all.reverse()
        backward = list(
            map(
                lambda task: task.description,
                all,
            )
        )
        self.assertEqual(
            backward,
            [
                "do task1",
                "do task2",
                "do task3",
                "do duty1",
            ],
        )


class MultiplePartToMiddleDutyTestClass(TestCase):
    def setUp(self):
        get_task_definitions.cache_clear()

    @classmethod
    def setUpClass(cls):
        super(
            MultiplePartToMiddleDutyTestClass,
            cls,
        ).setUpClass()
        part_to1 = PartTo.objects.create(name="My Part To One")
        MultiplePartToMiddleDutyTestClass.part_to1 = part_to1
        MultiplePartToMiddleDutyTestClass.task1_1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=1),
            part_to=part_to1,
            description="do task1-1",
        )
        MultiplePartToMiddleDutyTestClass.duty1_1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(seconds=30),
            part_to=part_to1,
            description="do duty1-1",
            depended=MultiplePartToMiddleDutyTestClass.task1_1,
            engagement=10,
        )
        MultiplePartToMiddleDutyTestClass.task1_2 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=2),
            part_to=part_to1,
            description="do task1-2",
            depended=MultiplePartToMiddleDutyTestClass.duty1_1,
        )
        part_to2 = PartTo.objects.create(name="My Part To Two")
        MultiplePartToMiddleDutyTestClass.part_to2 = part_to2
        MultiplePartToMiddleDutyTestClass.task2_1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=1),
            part_to=part_to2,
            description="do task2-1",
        )
        MultiplePartToMiddleDutyTestClass.task2_2 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=4),
            part_to=part_to2,
            description="do task2-2",
            depended=MultiplePartToMiddleDutyTestClass.task2_1,
        )
        MultiplePartToMiddleDutyTestClass.duty2_1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(seconds=30),
            part_to=part_to2,
            description="do duty2-1",
            depended=MultiplePartToMiddleDutyTestClass.task2_2,
            engagement=10,
        )

    def test_singlepartto_sorting(self):
        all = [
            MultiplePartToMiddleDutyTestClass.task1_1,
            MultiplePartToMiddleDutyTestClass.task1_2,
            MultiplePartToMiddleDutyTestClass.duty1_1,
        ]
        all.sort()
        descriptions = list(
            map(
                lambda task: task.description,
                all,
            )
        )
        self.assertEqual(
            descriptions,
            [
                "do task1-2",
                "do duty1-1",
                "do task1-1",
            ],
        )

    def test_multipartto_sorting(self):
        all = [
            MultiplePartToMiddleDutyTestClass.task1_1,
            MultiplePartToMiddleDutyTestClass.task1_2,
            MultiplePartToMiddleDutyTestClass.task2_2,
            MultiplePartToMiddleDutyTestClass.duty1_1,
            MultiplePartToMiddleDutyTestClass.task2_1,
            MultiplePartToMiddleDutyTestClass.duty2_1,
        ]
        all.sort()
        descriptions = list(
            map(
                lambda task: task.description,
                all,
            )
        )
        self.assertEqual(
            descriptions,
            [
                "do duty2-1",
                "do task2-2",
                "do task1-2",
                "do duty1-1",
                "do task1-1",
                "do task2-1",
            ],
        )

    def test_time_calculation(self):
        all = [
            MultiplePartToMiddleDutyTestClass.task1_1,
            MultiplePartToMiddleDutyTestClass.task1_2,
            MultiplePartToMiddleDutyTestClass.duty1_1,
            MultiplePartToMiddleDutyTestClass.task2_1,
            MultiplePartToMiddleDutyTestClass.task2_2,
            MultiplePartToMiddleDutyTestClass.duty2_1,
        ]
        all.sort()
        self.assertEqual(
            all[0].chain_duration(),
            datetime.timedelta(minutes=5, seconds=3),
        )


class MultiplePartToTestClass(TestCase):
    def setUp(self):
        get_task_definitions.cache_clear()

    @classmethod
    def setUpClass(cls):
        super(MultiplePartToTestClass, cls).setUpClass()
        part_to1 = PartTo.objects.create(name="My Part To One")
        MultiplePartToTestClass.part_to1 = part_to1
        MultiplePartToTestClass.task1_1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=1),
            part_to=part_to1,
            description="do task1-1",
        )
        MultiplePartToTestClass.task1_2 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=2),
            part_to=part_to1,
            description="do task1-2",
            depended=MultiplePartToTestClass.task1_1,
        )
        MultiplePartToTestClass.duty1_1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(seconds=30),
            part_to=part_to1,
            description="do duty1-1",
            depended=MultiplePartToTestClass.task1_2,
            engagement=10,
        )
        part_to2 = PartTo.objects.create(name="My Part To Two")
        MultiplePartToTestClass.part_to2 = part_to2
        MultiplePartToTestClass.task2_1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=4),
            part_to=part_to2,
            description="do task2-1",
        )
        MultiplePartToTestClass.task2_2 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(minutes=2),
            part_to=part_to2,
            description="do task2-2",
            depended=MultiplePartToTestClass.task2_1,
        )
        MultiplePartToTestClass.duty2_1 = TaskDefinition.objects.create(
            initial_duration=datetime.timedelta(seconds=30),
            part_to=part_to2,
            description="do duty2-1",
            depended=MultiplePartToTestClass.task2_2,
            engagement=10,
        )

    def test_multipartto_sorting(self):
        all = [
            MultiplePartToTestClass.task1_1,
            MultiplePartToTestClass.task1_2,
            MultiplePartToTestClass.task2_2,
            MultiplePartToTestClass.duty1_1,
            MultiplePartToTestClass.task2_1,
            MultiplePartToTestClass.duty2_1,
        ]
        all.sort()
        descriptions = list(
            map(
                lambda task: task.description,
                all,
            )
        )
        self.assertEqual(
            descriptions,
            [
                "do duty2-1",
                "do task2-2",
                "do task2-1",
                "do duty1-1",
                "do task1-2",
                "do task1-1",
            ],
        )

    def test_time_calculation(self):
        all = [
            MultiplePartToTestClass.task1_1,
            MultiplePartToTestClass.task1_2,
            MultiplePartToTestClass.duty1_1,
            MultiplePartToTestClass.task2_1,
            MultiplePartToTestClass.task2_2,
            MultiplePartToTestClass.duty2_1,
        ]
        all.sort()
        self.assertEqual(
            all[0].chain_duration(),
            datetime.timedelta(minutes=6, seconds=3),
        )


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

    def test_calculating_overflowing_task_duractions(
        self,
    ):
        self.assertEqual(
            CollectionInnerDutyTestClass.duty1.chain_duration(),
            datetime.timedelta(minutes=3, seconds=3),
        )

    def test_calculating_underflowing_task_duractions(
        self,
    ):
        duty1 = CollectionInnerDutyTestClass.duty1
        duty1.initial_duration = datetime.timedelta(minutes=5)
        self.assertEqual(
            CollectionInnerDutyTestClass.duty1.chain_duration(),
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
        forward = list(
            map(
                lambda task: task.description,
                all,
            )
        )
        self.assertEqual(
            forward,
            [
                "do duty1",
                "do task2",
                "do task1",
            ],
        )
        all.reverse()
        backward = list(
            map(
                lambda task: task.description,
                all,
            )
        )
        self.assertEqual(
            backward,
            [
                "do task1",
                "do task2",
                "do duty1",
            ],
        )
