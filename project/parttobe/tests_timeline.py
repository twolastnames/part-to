from django.test import TestCase
from parttobe.timeline import Timeline
from parttobe.timeline import define
from parttobe.timeline import Marker
from dataclasses import dataclass


@dataclass
class Definition:
    id: str
    duration: float
    engagement: float


class CollectionTaskTestClass(TestCase):

    def test_can_echo_a_simple_task(self):
        task = define(Definition(1, 200, None))
        self.assertEqual(task.engagement, 1.0)
        self.assertEqual(task.dependent, None)
        self.assertEqual(task.duration, 200)

    def test_can_position_chunks(self):
        task1 = define(Definition(1, 200, None))
        task2 = define(Definition(2, 300, None))
        task1.dependent = task2
        self.assertEqual(task1.id, "1")
        self.assertEqual(task1.dependent.id, "2")

    def test_can_return_nothing(self):
        line = Timeline()
        self.assertEqual(len(list(line)), 0)

    #    def test_split_a_task(self):
    #        chunk1, chunk2 = timeline.Task(1, 200).split(50)
    #        self.assertEqual(chunk1.duration, 50)
    #        self.assertEqual(chunk2.duration, 150)

    def test_can_add_a_duty(self):
        duty = define(Definition(1, 200, 0.5))
        line = Timeline()
        line.add(duty)
        line = list(line)
        self.assertEqual(line[0], Marker("1", 0.0, False))
        self.assertEqual(line[1], Marker("1", 200.0, True))

    def test_can_add_a_task(self):
        task = define(Definition(1, 200, None))
        line = Timeline()
        line.add(task)
        line = list(line)
        self.assertEqual(line[0], Marker("1", 0.0, False))
        self.assertEqual(line[1], Marker("1", 200.0, True))

    def test_can_order_2_nondependent_tasks(self):
        task1 = define(Definition(1, 200, None))
        task2 = define(Definition(2, 300, None))
        line = Timeline()
        line.add(task2)
        line.add(task1)
        line = list(line)
        self.assertEqual(line[0], Marker("1", 0.0, False))
        self.assertEqual(line[1], Marker("1", 200.0, True))
        self.assertEqual(line[2], Marker("2", 200.0, False))
        self.assertEqual(line[3], Marker("2", 500.0, True))

    def test_can_order_2_tasks_in_forward(self):
        task1 = define(Definition(1, 200, None))
        task2 = define(Definition(2, 300, None))
        task1.dependent = task2
        line = Timeline()
        line.add(task1)
        line.add(task2)
        line = list(line)
        self.assertEqual(line[0], Marker("1", 0.0, False))
        self.assertEqual(line[1], Marker("1", 200.0, True))
        self.assertEqual(line[2], Marker("2", 200.0, False))
        self.assertEqual(line[3], Marker("2", 500.0, True))

    def test_can_order_2_tasks_in_reverse(self):
        task1 = define(Definition(1, 200, None))
        task2 = define(Definition(2, 300, None))
        task1.dependent = task2
        line = Timeline()
        line.add(task2)
        line.add(task1)
        line = list(line)
        self.assertEqual(line[0], Marker("1", 0.0, False))
        self.assertEqual(line[1], Marker("1", 200.0, True))
        self.assertEqual(line[2], Marker("2", 200.0, False))
        self.assertEqual(line[3], Marker("2", 500.0, True))

    def test_can_set_task_in_middle_of_tasks(self):
        task1 = define(Definition(1, 200, None))
        task2 = define(Definition(2, 300, None))
        task3 = define(Definition(3, 100, None))
        task3.dependent = task2
        line = Timeline()
        line.add(task2)
        line.add(task1)
        line.add(task3)
        line = list(line)
        self.assertEqual(line[0], Marker("1", 0.0, False))
        self.assertEqual(line[1], Marker("1", 200.0, True))
        self.assertEqual(line[2], Marker("3", 200.0, False))
        self.assertEqual(line[3], Marker("3", 300.0, True))
        self.assertEqual(line[4], Marker("2", 300.0, False))
        self.assertEqual(line[5], Marker("2", 600.0, True))

    def test_can_set_task_in_middle_of_tasks_when_dependent_given_last(self):
        task1 = define(Definition(1, 200, None))
        task2 = define(Definition(2, 300, None))
        task3 = define(Definition(3, 100, None))
        task3.dependent = task2
        line = Timeline()
        line.add(task2)
        line.add(task3)
        line.add(task1)
        line = list(line)
        self.assertEqual(line[0], Marker("1", 0.0, False))
        self.assertEqual(line[1], Marker("1", 200.0, True))
        self.assertEqual(line[2], Marker("3", 200.0, False))
        self.assertEqual(line[3], Marker("3", 300.0, True))
        self.assertEqual(line[4], Marker("2", 300.0, False))
        self.assertEqual(line[5], Marker("2", 600.0, True))


    def test_will_overput_same_duration_duty(self):
        task1 = define(Definition(1, 100, None))
        duty2 = define(Definition(2, 200, 0.5))
        line = Timeline()
        line.add(task1)
        line.add(duty2)
        line = list(line)
        self.assertEqual(line[0], Marker("1", 0.0, False))
        self.assertEqual(line[1], Marker("2", 0.0, False))
        self.assertEqual(line[2], Marker("1", 200.0, True))
        self.assertEqual(line[3], Marker("2", 200.0, True))

    def test_task_will_overrun_a_duty_into_own_window(self):
        task1 = define(Definition(1, 100, None))
        duty2 = define(Definition(2, 200, 0.25))
        line = Timeline()
        line.add(task1)
        line.add(duty2)
        line = list(line)
        self.assertEqual(line[0], Marker("1", 0.0, False))
        self.assertEqual(line[1], Marker("2", 50.0, False))
        self.assertEqual(line[2], Marker("1", 200.0, True))
        self.assertEqual(line[3], Marker("2", 200.0, True))

    def test_duty_will_overrun_a_task_into_own_window(self):
        task1 = define(Definition(1, 100, None))
        duty2 = define(Definition(2, 200, 0.75))
        line = Timeline()
        line.add(task1)
        line.add(duty2)
        line = list(line)
        self.assertEqual(line[0], Marker("1", 0.0, False))
        self.assertEqual(line[1], Marker("2", 25.0, False))
        self.assertEqual(line[2], Marker("2", 225.0, True))
        self.assertEqual(line[3], Marker("1", 225.0, True))


