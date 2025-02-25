from django.test import TestCase
from parttobe.timeline import Timeline
from parttobe.timeline import Marker
import functools
from datetime import timedelta


@functools.total_ordering
class Definition:
    def __init__(self, id, duration, engagement):
        self.id = id
        self.duration = timedelta(seconds=duration)
        self.engagement = engagement
        self.dependent = None

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return "[id={}:duration={}:engagement={}]".format(
            self.id, self.duration, self.engagement
        )

    def __eq__(self, other):
        if not hasattr(other, "id"):
            return False
        if not other.id:
            return False
        return self.id == other.id


class CollectionTaskTestClass(TestCase):

    def test_can_echo_a_simple_task(self):
        task = Definition(1, 200, 1.0)
        self.assertEqual(task.engagement, 1.0)
        self.assertEqual(task.dependent, None)
        self.assertEqual(task.duration, timedelta(seconds=200))

    def test_can_position_chunks(self):
        task1 = Definition(1, 200, None)
        task2 = Definition(2, 300, None)
        task1.dependent = task2
        self.assertEqual(task1.id, 1)
        self.assertEqual(task1.dependent.id, 2)

    def test_can_return_nothing(self):
        line = Timeline([])
        self.assertEqual(len(list(line)), 0)

    #    def test_split_a_task(self):
    #        chunk1, chunk2 = timeline.Task(1, 200).split(50)
    #        self.assertEqual(chunk1.duration, 50)
    #        self.assertEqual(chunk2.duration, 150)

    def test_can_add_a_duty(self):
        duty = Definition(1, 200, 0.5)
        line = Timeline([duty])
        line = list(line)
        self.assertEqual(line[0], Marker(duty, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty, timedelta(seconds=200.0), True))

    def test_can_add_a_task(self):
        task = Definition(1, 200, None)
        line = Timeline([task])
        line = list(line)
        self.assertEqual(line[0], Marker(task, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task, timedelta(seconds=200.0), True))

    def test_can_order_2_nondependent_tasks(self):
        task1 = Definition(1, 200, None)
        task2 = Definition(2, 300, None)
        line = Timeline([task2, task1])
        line = list(line)
        self.assertEqual(line[0], Marker(task2, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task2, timedelta(seconds=300.0), True))
        self.assertEqual(line[2], Marker(task1, timedelta(seconds=300.0), False))
        self.assertEqual(line[3], Marker(task1, timedelta(seconds=500.0), True))

    def test_can_order_2_tasks_in_forward(self):
        task1 = Definition(1, 200, None)
        task2 = Definition(2, 300, None)
        task1.dependent = task2
        line = Timeline([task1, task2])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=200.0), True))
        self.assertEqual(line[2], Marker(task2, timedelta(seconds=200.0), False))
        self.assertEqual(line[3], Marker(task2, timedelta(seconds=500.0), True))

    def test_can_order_2_tasks_in_reverse(self):
        task1 = Definition(1, 200, None)
        task2 = Definition(2, 300, None)
        task1.dependent = task2
        line = Timeline([task2, task1])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=200.0), True))
        self.assertEqual(line[2], Marker(task2, timedelta(seconds=200.0), False))
        self.assertEqual(line[3], Marker(task2, timedelta(seconds=500.0), True))

    def test_can_set_task_in_middle_of_tasks(self):
        task1 = Definition(1, 200, None)
        task2 = Definition(2, 300, None)
        task3 = Definition(3, 100, None)
        task3.dependent = task2
        line = Timeline([task2, task1, task3])
        line = list(line)
        self.assertEqual(line[0], Marker(task3, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task3, timedelta(seconds=100.0), True))
        self.assertEqual(line[2], Marker(task2, timedelta(seconds=100.0), False))
        self.assertEqual(line[3], Marker(task2, timedelta(seconds=400.0), True))
        self.assertEqual(line[4], Marker(task1, timedelta(seconds=400.0), False))
        self.assertEqual(line[5], Marker(task1, timedelta(seconds=600.0), True))

    def test_can_set_task_in_middle_of_tasks_when_dependent_given_last(self):
        task1 = Definition(1, 200, None)
        task2 = Definition(2, 300, None)
        task3 = Definition(3, 100, None)
        task3.dependent = task2
        line = Timeline([task2, task3, task1])
        line = list(line)
        self.assertEqual(line[0], Marker(task3, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task3, timedelta(seconds=100.0), True))
        self.assertEqual(line[2], Marker(task2, timedelta(seconds=100.0), False))
        self.assertEqual(line[3], Marker(task2, timedelta(seconds=400.0), True))
        self.assertEqual(line[4], Marker(task1, timedelta(seconds=400.0), False))
        self.assertEqual(line[5], Marker(task1, timedelta(seconds=600.0), True))

    def test_will_overput_same_duration_duty(self):
        duty1 = Definition(1, 100, 0.3)
        duty2 = Definition(2, 100, 0.5)
        line = Timeline([duty1, duty2])
        line = list(line)
        self.assertEqual(line[0], Marker(duty1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty2, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(duty1, timedelta(seconds=100.0), True))
        self.assertEqual(line[3], Marker(duty2, timedelta(seconds=100.0), True))

    def test_will_split_different_duration_duty(self):
        duty1 = Definition(1, 70, 0.3)
        duty2 = Definition(2, 100, 0.5)
        line = Timeline([duty1, duty2])
        line = list(line)
        self.assertEqual(line[0], Marker(duty2, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty1, timedelta(seconds=30.0), False))
        self.assertEqual(line[2], Marker(duty1, timedelta(seconds=100.0), True))
        self.assertEqual(line[3], Marker(duty2, timedelta(seconds=100.0), True))

    def test_will_split_different_duration_duty_reversed(self):
        duty1 = Definition(1, 170, 0.3)
        duty2 = Definition(2, 100, 0.5)
        line = Timeline([duty1, duty2])
        line = list(line)
        self.assertEqual(line[0], Marker(duty1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty2, timedelta(seconds=70.0), False))
        self.assertEqual(line[2], Marker(duty1, timedelta(seconds=170.0), True))
        self.assertEqual(line[3], Marker(duty2, timedelta(seconds=170.0), True))

    def test_task_will_overrun_a_duty_into_own_window(self):
        task1 = Definition(1, 200, None)
        duty2 = Definition(2, 200, 0.25)
        line = Timeline([task1, duty2])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty2, timedelta(seconds=50.0), False))
        self.assertEqual(line[2], Marker(task1, timedelta(seconds=250.0), True))
        self.assertEqual(line[3], Marker(duty2, timedelta(seconds=250.0), True))

    def test_task_will_frontload_a_duty_when_comparably_shorter(self):
        task1 = Definition(1, 20, None)
        duty2 = Definition(2, 200, 0.25)
        line = Timeline([task1, duty2])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty2, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(task1, timedelta(seconds=26.666667), True))
        self.assertEqual(line[3], Marker(duty2, timedelta(seconds=200.0), True))

    def test_task_will_frontload_a_duty_when_comparably_shorter_and_in_another_duty(self):
        task1 = Definition(1, 10, None)
        duty2 = Definition(2, 20, 0.10)
        duty3 = Definition(3, 60, 0.25)
        line = Timeline([duty3,task1, duty2])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty2, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(task1, timedelta(seconds=11.0),True))
        self.assertEqual(line[3], Marker(task1, timedelta(seconds=26.666667), True))
        self.assertEqual(line[4], Marker(duty2, timedelta(seconds=200.0), True))
        self.assertEqual(line[5], Marker(duty2, timedelta(seconds=200.0), True))

    def test_task_will_overlay_a_duty_with_comparable_weight(self):
        task = Definition(1, 150, None)
        duty = Definition(2, 200, 0.25)
        line = Timeline([duty, task])
        line = list(line)
        self.assertEqual(line[0], Marker(task, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(task, timedelta(seconds=200.0), True))
        self.assertEqual(line[3], Marker(duty, timedelta(seconds=200.0), True))

    def test_duty_will_overrun_a_task_with_comparable_weight(self):
        task = Definition(1, 150, None)
        duty = Definition(2, 200, 0.25)
        line = Timeline([task, duty])
        line = list(line)
        self.assertEqual(line[0], Marker(task, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(task, timedelta(seconds=200.0), True))
        self.assertEqual(line[3], Marker(duty, timedelta(seconds=200.0), True))

    def test_task_will_overrun_a_duty_with_comparable_weight(self):
        task = Definition(1, 150, None)
        duty = Definition(2, 200, 0.25)
        line = Timeline([duty, task])
        line = list(line)
        self.assertEqual(line[0], Marker(task, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(task, timedelta(seconds=200.0), True))
        self.assertEqual(line[3], Marker(duty, timedelta(seconds=200.0), True))

    def test_task_will_front_its_dependency_and_duty(self):
        task1 = Definition(1, 25, None)
        task2 = Definition(2, 30, None)
        duty3 = Definition(3, 20, 0.25)
        task1.dependent = task2
        line = Timeline([task1, duty3, task2])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=25.0), True))
        self.assertEqual(line[2], Marker(task2, timedelta(seconds=25.0), False))
        self.assertEqual(line[3], Marker(duty3, timedelta(seconds=40.0), False))
        self.assertEqual(line[4], Marker(task2, timedelta(seconds=60.0), True))
        self.assertEqual(line[5], Marker(duty3, timedelta(seconds=60.0), True))

    def test_task_will_front_its_dependency_and_duty_reverse(self):
        task1 = Definition(1, 25, None)
        task2 = Definition(2, 30, None)
        duty3 = Definition(3, 20, 0.25)
        task1.dependent = task2
        line = Timeline([task2, duty3, task1])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=25.0), True))
        self.assertEqual(line[2], Marker(task2, timedelta(seconds=25.0), False))
        self.assertEqual(line[3], Marker(duty3, timedelta(seconds=40.0), False))
        self.assertEqual(line[4], Marker(task2, timedelta(seconds=60.0), True))
        self.assertEqual(line[5], Marker(duty3, timedelta(seconds=60.0), True))

    def test_duty_will_overrun_a_task_into_own_window(self):
        task1 = Definition(1, 100, None)
        duty2 = Definition(2, 200, 0.75)
        line = Timeline([task1, duty2])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty2, timedelta(seconds=50.0), False))
        self.assertEqual(line[2], Marker(task1, timedelta(seconds=250.0), True))
        self.assertEqual(line[3], Marker(duty2, timedelta(seconds=250.0), True))

    def test_duty_will_deal_with_dependent_duty(self):
        duty1 = Definition(1, 100, 0.20)
        duty2 = Definition(2, 200, 0.75)
        duty2.dependent = duty1
        line = Timeline([duty1, duty2])
        line = list(line)
        self.assertEqual(line[0], Marker(duty2, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty2, timedelta(seconds=200.0), True))
        self.assertEqual(line[2], Marker(duty1, timedelta(seconds=200.0), False))
        self.assertEqual(line[3], Marker(duty1, timedelta(seconds=300.0), True))

    def test_duty_will_deal_with_dependent_duty_reversed(self):
        duty1 = Definition(1, 100, 0.20)
        duty2 = Definition(2, 200, 0.75)
        duty2.dependent = duty1
        line = Timeline([duty2, duty1])
        line = list(line)
        self.assertEqual(line[0], Marker(duty2, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty2, timedelta(seconds=200.0), True))
        self.assertEqual(line[2], Marker(duty1, timedelta(seconds=200.0), False))
        self.assertEqual(line[3], Marker(duty1, timedelta(seconds=300.0), True))
