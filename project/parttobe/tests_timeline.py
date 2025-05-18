from django.test import TestCase
from parttobe.timeline import Timeline
from parttobe.timeline import Marker
from parttobe.timeline import Definition
from datetime import timedelta
from dataclasses import dataclass


def dump_line(line):
    print([repr(Marker(marker.id.id, marker.till, marker.is_done)) for marker in line])


class CollectionTaskTestClass(TestCase):

    def test_can_echo_a_simple_task(self):
        task = Definition(1, 200, 1.0)
        self.assertEqual(task.engagement, 1.0)
        self.assertEqual(task.depended, None)
        self.assertEqual(task.duration, timedelta(seconds=200))

    def test_can_position_chunks(self):
        task1 = Definition(1, 200, None)
        task2 = Definition(2, 300, None)
        task1.depended = task2
        self.assertEqual(task1.id, 1)
        self.assertEqual(task1.depended.id, 2)

    def test_can_return_nothing(self):
        line = Timeline([])
        self.assertEqual(len(list(line)), 0)

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

    def test_can_order_2_nondepended_tasks(self):
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
        task1.depended = task2
        line = Timeline([task1, task2])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=200.0), True))
        self.assertEqual(line[2], Marker(task2, timedelta(seconds=200.0), False))
        self.assertEqual(line[3], Marker(task2, timedelta(seconds=500.0), True))

    def test_can_order_2_tasks_in_reverse(self):
        task1 = Definition(1, 200, None)
        task2 = Definition(2, 300, None)
        task1.depended = task2
        line = Timeline([task2, task1])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=200.0), True))
        self.assertEqual(line[2], Marker(task2, timedelta(seconds=200.0), False))
        self.assertEqual(line[3], Marker(task2, timedelta(seconds=500.0), True))

    def test_can_set_task_in_middle_of_tasks(self):
        task1 = Definition("task1", 200, None)
        task2 = Definition("task2", 300, None)
        task3 = Definition("task3", 100, None)
        task3.depended = task2
        line = Timeline([task2, task1, task3])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=200.0), True))
        self.assertEqual(line[2], Marker(task3, timedelta(seconds=200.0), False))
        self.assertEqual(line[3], Marker(task3, timedelta(seconds=300.0), True))
        self.assertEqual(line[4], Marker(task2, timedelta(seconds=300.0), False))
        self.assertEqual(line[5], Marker(task2, timedelta(seconds=600.0), True))

    def test_can_set_task_in_middle_of_tasks_when_depended_given_last(self):
        task1 = Definition("task1", 200, None)
        task2 = Definition("task2", 300, None)
        task3 = Definition("task3", 100, None)
        task3.depended = task2
        line = Timeline([task2, task3, task1])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=200.0), True))
        self.assertEqual(line[2], Marker(task3, timedelta(seconds=200.0), False))
        self.assertEqual(line[3], Marker(task3, timedelta(seconds=300.0), True))
        self.assertEqual(line[4], Marker(task2, timedelta(seconds=300.0), False))
        self.assertEqual(line[5], Marker(task2, timedelta(seconds=600.0), True))

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

    def test_task_will_frontload_a_duty_when_comparably_shorter_reversed(self):
        task1 = Definition("task1", 20, None)
        duty2 = Definition("duty2", 200, 0.25)
        line = Timeline([duty2, task1])
        line = list(line)
        self.assertEqual(line[0], Marker(duty2, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(task1, timedelta(seconds=26.666667), True))
        self.assertEqual(line[3], Marker(duty2, timedelta(seconds=200.0), True))

    def test_task_will_frontload_a_duty_when_comparably_shorter_and_in_another_duty(
        self,
    ):
        task1 = Definition(1, 10, None)
        duty2 = Definition(2, 20, 0.10)
        duty3 = Definition(3, 60, 0.25)
        line = Timeline([duty3, task1, duty2])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty3, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(task1, timedelta(seconds=13.333333), True))
        self.assertEqual(line[3], Marker(duty2, timedelta(seconds=40), False))
        self.assertEqual(line[4], Marker(duty2, timedelta(seconds=60.0), True))
        self.assertEqual(line[5], Marker(duty3, timedelta(seconds=60.0), True))

    def test_task_will_frontload_before_a_dependency_reversed(self):
        task1 = Definition("task1", 6, None)
        task2 = Definition("task2", 20, None)
        duty3 = Definition("duty3", 20, 0.10)
        duty4 = Definition("duty4", 60, 0.25)
        duty3.depended = task2
        line = Timeline([duty3, task1, duty4, task2])
        line = list(line)
        self.assertEqual(line[0], Marker(duty4, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(task1, timedelta(seconds=8.0), True))
        self.assertEqual(line[3], Marker(duty3, timedelta(seconds=13.333333), False))
        self.assertEqual(line[4], Marker(duty3, timedelta(seconds=33.333333), True))
        self.assertEqual(line[5], Marker(task2, timedelta(seconds=33.333333), False))
        self.assertEqual(line[6], Marker(duty4, timedelta(seconds=60.0), True))
        self.assertEqual(line[7], Marker(task2, timedelta(seconds=60.0), True))

    def test_task_will_frontload_with_two_tasks(self):
        task1 = Definition("task1", 6, None)
        task2 = Definition("task2", 20, None)
        duty3 = Definition("duty3", 30, 0.10)
        duty4 = Definition("duty4", 40, 0.25)
        line = list(Timeline([task1, duty4, task2, duty3]))
        self.assertEqual(line[0], Marker(duty4, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task2, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(duty3, timedelta(seconds=10.0), False))
        self.assertEqual(line[3], Marker(task2, timedelta(seconds=29.230769), True))
        self.assertEqual(line[4], Marker(task1, timedelta(seconds=29.230769), False))
        self.assertEqual(line[5], Marker(task1, timedelta(seconds=38.461538), True))
        self.assertEqual(line[6], Marker(duty3, timedelta(seconds=40.0), True))
        self.assertEqual(line[7], Marker(duty4, timedelta(seconds=40.0), True))

    def test_task_will_frontload_before_a_dependency(self):
        task1 = Definition("task1", 6, None)
        task2 = Definition("task2", 20, None)
        duty3 = Definition("duty3", 20, 0.10)
        duty4 = Definition("duty4", 60, 0.25)
        duty3.depended = task2
        line = Timeline([task2, duty4, task1, duty3])
        line = list(line)
        self.assertEqual(line[0], Marker(duty4, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(task1, timedelta(seconds=8.0), True))
        self.assertEqual(line[3], Marker(duty3, timedelta(seconds=13.333333), False))
        self.assertEqual(line[4], Marker(duty3, timedelta(seconds=33.333333), True))
        self.assertEqual(line[5], Marker(task2, timedelta(seconds=33.333333), False))
        self.assertEqual(line[6], Marker(duty4, timedelta(seconds=60.0), True))
        self.assertEqual(line[7], Marker(task2, timedelta(seconds=60.0), True))

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
        task1 = Definition("task1", 25, None)
        task2 = Definition("task2", 30, None)
        duty3 = Definition("duty3", 20, 0.25)
        task1.depended = task2
        line = Timeline([duty3, task1, task2])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=25.0), True))
        self.assertEqual(line[2], Marker(task2, timedelta(seconds=25.0), False))
        self.assertEqual(line[3], Marker(duty3, timedelta(seconds=40.0), False))
        self.assertEqual(line[4], Marker(duty3, timedelta(seconds=60.0), True))
        self.assertEqual(line[5], Marker(task2, timedelta(seconds=60.0), True))

    def test_task_will_front_its_dependency_and_test_task_will_frontload_a_duty_when_comparably_shorter_duty_reverse(
        self,
    ):
        task1 = Definition("task1", 25, None)
        task2 = Definition("task2", 30, None)
        duty3 = Definition("duty3", 20, 0.25)
        task1.depended = task2
        line = Timeline([task2, duty3, task1])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=25.0), True))
        self.assertEqual(line[2], Marker(task2, timedelta(seconds=25.0), False))
        self.assertEqual(line[3], Marker(duty3, timedelta(seconds=40.0), False))
        self.assertEqual(line[4], Marker(duty3, timedelta(seconds=60.0), True))
        self.assertEqual(line[5], Marker(task2, timedelta(seconds=60.0), True))

    def test_duty_will_overrun_a_task_into_own_window(self):
        task1 = Definition("task1", 100, None)
        duty2 = Definition("duty2", 200, 0.75)
        line = Timeline([task1, duty2])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty2, timedelta(seconds=50.0), False))
        self.assertEqual(line[2], Marker(duty2, timedelta(seconds=250.0), True))
        self.assertEqual(line[3], Marker(task1, timedelta(seconds=250.0), True))

    def test_duty_will_deal_with_depended_duty(self):
        duty1 = Definition(1, 100, 0.20)
        duty2 = Definition(2, 200, 0.75)
        duty2.depended = duty1
        line = list(Timeline([duty1, duty2]))
        self.assertEqual(line[0], Marker(duty2, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty2, timedelta(seconds=200.0), True))
        self.assertEqual(line[2], Marker(duty1, timedelta(seconds=200.0), False))
        self.assertEqual(line[3], Marker(duty1, timedelta(seconds=300.0), True))

    def test_duty_will_deal_with_depended_duty_reversed(self):
        duty1 = Definition(1, 100, 0.20)
        duty2 = Definition(2, 200, 0.75)
        duty2.depended = duty1
        line = Timeline([duty2, duty1])
        line = list(line)
        self.assertEqual(line[0], Marker(duty2, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty2, timedelta(seconds=200.0), True))
        self.assertEqual(line[2], Marker(duty1, timedelta(seconds=200.0), False))
        self.assertEqual(line[3], Marker(duty1, timedelta(seconds=300.0), True))
