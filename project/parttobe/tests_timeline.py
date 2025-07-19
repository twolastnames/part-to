from django.test import TestCase
from parttobe.timeline import Timeline
from parttobe.timeline import Marker
from parttobe.timeline import Definition
from datetime import timedelta
from dataclasses import dataclass
from unittest import skip
import os


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
        task1 = Definition("task1", 200, None)
        task2 = Definition("task2", 300, None)
        line = Timeline([task2, task1])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=200.0), True))
        self.assertEqual(line[2], Marker(task2, timedelta(seconds=200.0), False))
        self.assertEqual(line[3], Marker(task2, timedelta(seconds=500.0), True))

    def test_seen_baked_beans_fail(self):
        # remove pan from oven and let stand for 5 minutes
        duty1 = Definition("duty1", 300, 0.05)
        # remove beans from oven
        task2 = Definition("task2", 10, None)
        # bake to desired consistency
        duty3 = Definition("duty3", 9000, 0.02)
        # pour bean mixture in 3 quart baking pan and layout cooked bacon on top
        task4 = Definition("task4", 30, None)
        # simmer bean mixture a minute or so
        duty5 = Definition("duty5", 90, 0.05)
        # saute diced green peppers and onion
        duty6 = Definition("duty6", 300, 0.1)
        # dice half of a green pepper and a whole yellow onion and combine aside
        task7 = Definition("task7", 120, None)
        # heat pan to medium heat
        duty8 = Definition("duty8", 150, 0.02)
        # get pan and put 2 tbs butter in it
        task9 = Definition("task9", 60, None)
        # gather and combine 54 oz canned pork and beans, 2 tsp dry mustard, 2/3 cup brown sugar, 1/4 cup cider vinegar, 4 tbs ketchup, & 1/4 cup molasses
        task10 = Definition("task10", 180, None)
        # cook bacon to slightly rare
        duty11 = Definition("duty11", 1200, 0.03)
        # put 10 slices of bacon on pan and put in oven
        task12 = Definition("task12", 120, None)
        # Heat Oven to 325 degrees
        duty13 = Definition("duty13", 900, 0.0)
        # grease 3 quart baking pan
        task14 = Definition("task14", 45, None)
        task2.depended = duty1
        duty3.depended = task2
        task4.depended = duty3
        duty5.depended = task4
        duty6.depended = duty5
        task7.depended = duty6
        duty8.depended = duty6
        task9.depended = duty8
        task10.depended = duty5
        duty11.depended = task4
        task12.depended = duty11
        duty13.depended = task12
        task14.depended = task4
        line = list(
            Timeline(
                [
                    duty1,
                    task2,
                    duty3,
                    task4,
                    duty5,
                    duty6,
                    task7,
                    duty8,
                    task9,
                    task10,
                    duty11,
                    task12,
                    duty13,
                    task14,
                ]
            )
        )
        self.assertEqual(line[0], Marker(duty13, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(duty13, timedelta(seconds=900.0), True))
        self.assertEqual(line[2], Marker(task12, timedelta(seconds=900.0), False))
        self.assertEqual(line[3], Marker(task12, timedelta(seconds=1020.0), True))
        self.assertEqual(line[4], Marker(duty11, timedelta(seconds=1020.0), False))
        self.assertEqual(line[5], Marker(task9, timedelta(seconds=1020.0), False))
        self.assertEqual(line[6], Marker(task9, timedelta(seconds=1081.85567), True))
        self.assertEqual(line[7], Marker(task7, timedelta(seconds=1081.85567), False))
        self.assertEqual(line[8], Marker(task7, timedelta(seconds=1205.56701), True))
        self.assertEqual(line[9], Marker(task10, timedelta(seconds=1205.56701), False))
        self.assertEqual(line[10], Marker(task10, timedelta(seconds=1391.134021), True))
        self.assertEqual(
            line[11], Marker(task14, timedelta(seconds=1391.134021), False)
        )
        self.assertEqual(line[12], Marker(task14, timedelta(seconds=1437.525773), True))
        self.assertEqual(line[13], Marker(task4, timedelta(seconds=1437.525773), False))
        self.assertEqual(line[14], Marker(task4, timedelta(seconds=1468.453608), True))
        self.assertEqual(line[15], Marker(duty8, timedelta(seconds=1680.0), False))
        self.assertEqual(line[16], Marker(duty8, timedelta(seconds=1830.0), True))
        self.assertEqual(line[17], Marker(duty6, timedelta(seconds=1830.0), False))
        self.assertEqual(line[18], Marker(duty6, timedelta(seconds=2130.0), True))
        self.assertEqual(line[19], Marker(duty5, timedelta(seconds=2130.0), False))
        self.assertEqual(line[20], Marker(duty11, timedelta(seconds=2220.0), True))
        self.assertEqual(line[21], Marker(duty5, timedelta(seconds=2220.0), True))
        self.assertEqual(line[22], Marker(duty3, timedelta(seconds=2250.0), False))
        self.assertEqual(line[23], Marker(duty3, timedelta(seconds=11250.0), True))
        self.assertEqual(line[24], Marker(task2, timedelta(seconds=11250.0), False))
        self.assertEqual(line[25], Marker(task2, timedelta(seconds=11260.0), True))
        self.assertEqual(line[26], Marker(duty1, timedelta(seconds=11260.0), False))
        self.assertEqual(line[27], Marker(duty1, timedelta(seconds=11560.0), True))

    def test_seen_pot_roast_fail_with_leading_task(self):
        # put oil in dutch oven
        task1 = Definition("task1", 30, None)
        # put the following in the bowl onion bowl: 1/2 tsp ground ginger, 1/2 tsp pepper, 1 bay leaf,  1 tsp ground cinnamon, 1 tsp salt, 2 tbs sugar, 1 tbs white vinegar, 8 oz tomato sauce, 3/4 cup beer or beef broth, 1 1/4 cup water
        task2 = Definition("task2", 180, None)
        # chop an onion and put it in 4ish cup bowl
        task3 = Definition("task3", 120, None)
        # remove meat and slice
        task4 = Definition("task4", 120, None)
        # reduce heat, cover, and simmer
        duty5 = Definition("duty5", 9900, 0.01)
        # dump ingredients in dutch oven and stir
        task6 = Definition("task6", 30, None)
        # put roast meat in dutch oven and brown all sides
        duty7 = Definition("duty7", 600, 0.1)
        # heat oil in dutch oven
        duty8 = Definition("duty8", 150, 0.02)
        task1.depended = duty8
        task2.depended = task6
        task3.depended = task2
        duty5.depended = task4
        task6.depended = duty5
        duty7.depended = task6
        duty8.depended = duty7
        line = Timeline([task1, task2, task3, task4, duty5, task6, duty7, duty8])
        line = list(line)
        self.assertEqual(line[0], Marker(task1, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task1, timedelta(seconds=30.0), True))
        self.assertEqual(line[2], Marker(duty8, timedelta(seconds=30.0), False))
        self.assertEqual(line[3], Marker(task3, timedelta(seconds=30.0), False))
        self.assertEqual(line[4], Marker(task3, timedelta(seconds=152.44898), True))
        self.assertEqual(line[5], Marker(task2, timedelta(seconds=152.44898), False))
        self.assertEqual(line[6], Marker(duty8, timedelta(seconds=180.0), True))
        self.assertEqual(line[7], Marker(duty7, timedelta(seconds=180.0), False))
        self.assertEqual(line[8], Marker(task2, timedelta(seconds=350.0), True))
        self.assertEqual(line[9], Marker(task6, timedelta(seconds=350.0), False))
        self.assertEqual(line[10], Marker(task6, timedelta(seconds=383.333333), True))
        self.assertEqual(line[11], Marker(duty7, timedelta(seconds=780.0), True))
        self.assertEqual(line[12], Marker(duty5, timedelta(seconds=810.0), False))
        self.assertEqual(line[13], Marker(duty5, timedelta(seconds=10710.0), True))
        self.assertEqual(line[14], Marker(task4, timedelta(seconds=10710.0), False))
        self.assertEqual(line[15], Marker(task4, timedelta(seconds=10830.0), True))

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

    def test_ends_with_task_with_inner_tasks(self):
        task1 = Definition("task1", 20, None)
        duty2 = Definition("duty2", 240, 0.04)
        task3 = Definition("task3", 120, None)
        task4 = Definition("task4", 60, None)
        duty5 = Definition("duty5", 480, 0.02)
        duty2.depended = task1
        task3.depended = duty2
        task4.depended = task3
        duty5.depended = duty2
        line = Timeline([task1, duty2, task3, task4, duty5])
        line = list(line)
        self.assertEqual(line[0], Marker(duty5, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task4, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(task4, timedelta(seconds=61.22449), True))
        self.assertEqual(line[3], Marker(task3, timedelta(seconds=61.22449), False))
        self.assertEqual(line[4], Marker(task3, timedelta(seconds=183.673469), True))
        self.assertEqual(line[5], Marker(duty5, timedelta(seconds=480.0), True))
        self.assertEqual(line[6], Marker(duty2, timedelta(seconds=480.0), False))
        self.assertEqual(line[7], Marker(duty2, timedelta(seconds=720.0), True))
        self.assertEqual(line[8], Marker(task1, timedelta(seconds=720.0), False))
        self.assertEqual(line[9], Marker(task1, timedelta(seconds=740.0), True))

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

    @skip("deal with after db change")
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
        self.assertEqual(line[3], Marker(duty3, timedelta(seconds=55.0), False))
        self.assertEqual(line[4], Marker(duty3, timedelta(seconds=75.0), True))
        self.assertEqual(line[5], Marker(task2, timedelta(seconds=75.0), True))

    @skip("deal with after db change")
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
        self.assertEqual(line[3], Marker(duty3, timedelta(seconds=55.0), False))
        self.assertEqual(line[4], Marker(duty3, timedelta(seconds=75.0), True))
        self.assertEqual(line[5], Marker(task2, timedelta(seconds=75.0), True))

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

    def test_failed_frozen_veggies(self):
        # drain and serve beans
        task1 = Definition("task1", 30, None)
        # get water boiling again
        duty2 = Definition("duty2", 120, 0.02)
        # put and leave beans in boiling water
        duty3 = Definition("duty3", 240, 0.05)
        # boil water in large pot
        duty4 = Definition("duty4", 540, 0.02)
        duty2.depended = task1
        duty3.depended = duty2
        duty4.depended = duty3
        # remove from heat
        task5 = Definition("task5", 20, None)
        # put corn in and boil
        duty6 = Definition("duty6", 240, 0.04)
        # cut partially with kitchen shears to weaken cob middle to break in half
        task7 = Definition("task7", 120, None)
        # wash the corn
        task8 = Definition("task8", 60, None)
        # boil water in large pot
        duty9 = Definition("duty9", 480, 0.02)
        duty6.depended = task5
        task7.depended = duty6
        task8.depended = task7
        duty9.depended = duty6
        # good
        # line = list(Timeline([
        # task5,
        # duty6,
        # task7,
        # task8,
        # duty9,
        # task1,
        # duty2,
        # duty3,
        # duty4,
        # ]))
        # bad
        line = list(
            Timeline(
                [
                    # wash the corn
                    task8,
                    # boil water in large pot
                    duty4,
                    # cut partially with kitchen shears to weaken cob middle to break in half
                    task7,
                    # boil water in large pot
                    duty9,
                    # put and leave beans in boiling water
                    duty3,
                    # put corn in and boil
                    duty6,
                    # get water boiling again
                    duty2,
                    # drain and serve beans
                    task1,
                    # remove from heat
                    task5,
                ]
            )
        )
        self.assertEqual(line[0], Marker(duty4, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task8, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(task8, timedelta(seconds=61.22449), True))
        self.assertEqual(line[3], Marker(task7, timedelta(seconds=61.22449), False))
        self.assertEqual(line[4], Marker(task7, timedelta(seconds=183.673469), True))
        self.assertEqual(line[5], Marker(duty9, timedelta(seconds=211.25), False))
        self.assertEqual(line[6], Marker(duty4, timedelta(seconds=540.0), True))
        self.assertEqual(line[7], Marker(duty3, timedelta(seconds=540.0), False))
        self.assertEqual(line[8], Marker(duty9, timedelta(seconds=691.25), True))
        self.assertEqual(line[9], Marker(duty6, timedelta(seconds=691.25), False))
        self.assertEqual(line[10], Marker(duty3, timedelta(seconds=780.0), True))
        self.assertEqual(line[11], Marker(duty2, timedelta(seconds=780.0), False))
        self.assertEqual(line[12], Marker(duty2, timedelta(seconds=900.0), True))
        self.assertEqual(line[13], Marker(task1, timedelta(seconds=900.0), False))
        self.assertEqual(line[14], Marker(duty6, timedelta(seconds=931.25), True))
        self.assertEqual(line[15], Marker(task1, timedelta(seconds=931.25), True))
        self.assertEqual(line[16], Marker(task5, timedelta(seconds=931.25), False))
        self.assertEqual(line[17], Marker(task5, timedelta(seconds=951.25), True))

    @skip("deal with after db change")
    def test_does_not_have_seen_duplicates(self):
        # reduce heat, cover, and simmer
        duty1 = Definition("duty1", 9900, 0.01)
        # dump ingredients in dutch oven and stir
        task2 = Definition("task2", 30, None)
        # put roast meat in dutch oven and brown all sides
        duty3 = Definition("duty3", 600, 0.1)
        # heat oil in dutch oven
        duty4 = Definition("duty4", 150, 0.02)
        # put oil in dutch oven
        task5 = Definition("task5", 30, None)
        # put the following in the bowl onion bowl: 1/2 tsp ground ginger, 1/2 tsp pepper, 1 bay leaf,  1 tsp ground cinnamon, 1 tsp salt, 2 tbs sugar, 1 tbs white vinegar, 8 oz tomato sauce, 3/4 cup beer or beef broth, 1 1/4 cup water
        task6 = Definition("task6", 180, None)
        # chop an onion and put it in 4ish cup bowl
        task7 = Definition("task7", 120, None)
        # remove meat and slice
        task8 = Definition("task8", 120, None)
        duty1.depended = task8
        task2.depended = duty1
        duty3.depended = task2
        duty4.depended = duty3
        task5.depended = duty4
        task6.depended = task2
        task7.depended = task6
        # remove pan from oven and let stand for 5 minutes
        duty9 = Definition("duty9", 300, 0.05)
        # remove beans from oven
        task10 = Definition("task10", 10, None)
        # bake to desired consistency
        duty11 = Definition("duty11", 9000, 0.02)
        # pour bean mixture in 3 quart baking pan and layout cooked bacon on top
        task12 = Definition("task12", 30, None)
        # simmer bean mixture a minute or so
        duty13 = Definition("duty13", 90, 0.05)
        # saute diced green peppers and onion
        duty14 = Definition("duty14", 300, 0.1)
        # dice half of a green pepper and a whole yellow onion and combine aside
        task15 = Definition("task15", 120, None)
        # heat pan to medium heat
        duty16 = Definition("duty16", 150, 0.02)
        # get pan and put 2 tbs butter in it
        task17 = Definition("task17", 60, None)
        # gather and combine 54 oz canned pork and beans, 2 tsp dry mustard, 2/3 cup brown sugar, 1/4 cup cider vinegar, 4 tbs ketchup, & 1/4 cup molasses
        task18 = Definition("task18", 180, None)
        # put bacon in oven and cook to slightly rare
        duty19 = Definition("duty19", 1200, 0.03)
        # put 10 slices of bacon on pan
        task20 = Definition("task20", 120, None)
        # Heat Oven to 325 degrees
        duty21 = Definition("duty21", 900, 0.01)
        # grease 3 quart baking pan
        task22 = Definition("task22", 45, None)
        task10.depended = duty9
        duty11.depended = task10
        task12.depended = duty11
        duty13.depended = task12
        duty14.depended = duty13
        task15.depended = duty14
        duty16.depended = duty14
        task17.depended = duty16
        task18.depended = duty13
        duty19.depended = task12
        task20.depended = duty19
        duty21.depended = task20
        task22.depended = task12
        line = list(
            Timeline(
                [
                    duty9,
                    task10,
                    duty11,
                    task12,
                    duty13,
                    duty14,
                    task15,
                    duty16,
                    task17,
                    task18,
                    duty19,
                    task20,
                    duty21,
                    task22,
                    duty1,
                    task2,
                    duty3,
                    duty4,
                    task5,
                    task6,
                    task7,
                    task8,
                ]
            )
        )
        self.assertEqual(line[0], Marker(duty21, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task5, timedelta(seconds=0.0), False))
        self.assertEqual(line[2], Marker(task5, timedelta(seconds=30.30303), True))
        self.assertEqual(line[3], Marker(task7, timedelta(seconds=30.30303), False))
        self.assertEqual(line[4], Marker(task7, timedelta(seconds=151.515152), True))
        self.assertEqual(line[5], Marker(task6, timedelta(seconds=151.515152), False))
        self.assertEqual(line[6], Marker(task6, timedelta(seconds=333.333333), True))
        self.assertEqual(line[7], Marker(task2, timedelta(seconds=333.333333), False))
        self.assertEqual(line[8], Marker(task2, timedelta(seconds=363.636364), True))
        self.assertEqual(line[9], Marker(task17, timedelta(seconds=363.636364), False))
        self.assertEqual(line[10], Marker(task17, timedelta(seconds=424.242424), True))
        self.assertEqual(line[11], Marker(task15, timedelta(seconds=424.242424), False))
        self.assertEqual(line[12], Marker(task15, timedelta(seconds=545.454545), True))
        self.assertEqual(line[13], Marker(task18, timedelta(seconds=545.454545), False))
        self.assertEqual(line[14], Marker(task18, timedelta(seconds=727.272727), True))
        self.assertEqual(line[15], Marker(task22, timedelta(seconds=727.272727), False))
        self.assertEqual(line[16], Marker(task22, timedelta(seconds=772.727273), True))
        self.assertEqual(line[17], Marker(task12, timedelta(seconds=772.727273), False))
        self.assertEqual(line[18], Marker(task12, timedelta(seconds=803.030303), True))
        self.assertEqual(line[19], Marker(duty4, timedelta(seconds=842.15615), False))
        self.assertEqual(line[20], Marker(duty21, timedelta(seconds=900.0), True))
        self.assertEqual(line[21], Marker(task20, timedelta(seconds=900.0), False))
        self.assertEqual(line[22], Marker(duty4, timedelta(seconds=992.15615), True))
        self.assertEqual(line[23], Marker(duty3, timedelta(seconds=992.15615), False))
        self.assertEqual(line[24], Marker(duty3, timedelta(seconds=1025.141676), True))
        self.assertEqual(line[25], Marker(task20, timedelta(seconds=1025.141676), True))
        self.assertEqual(
            line[26], Marker(duty19, timedelta(seconds=1025.141676), False)
        )
        self.assertEqual(line[27], Marker(duty3, timedelta(seconds=1025.141676), False))
        self.assertEqual(line[28], Marker(duty3, timedelta(seconds=1592.15615), True))
        self.assertEqual(line[29], Marker(duty1, timedelta(seconds=1665.545716), False))
        self.assertEqual(
            line[30], Marker(duty16, timedelta(seconds=1685.141676), False)
        )
        self.assertEqual(line[31], Marker(duty16, timedelta(seconds=1835.141676), True))
        self.assertEqual(
            line[32], Marker(duty14, timedelta(seconds=1835.141676), False)
        )
        self.assertEqual(line[33], Marker(duty14, timedelta(seconds=2135.141676), True))
        self.assertEqual(
            line[34], Marker(duty13, timedelta(seconds=2135.141676), False)
        )
        self.assertEqual(line[35], Marker(duty13, timedelta(seconds=2225.141676), True))
        self.assertEqual(line[36], Marker(duty19, timedelta(seconds=2225.141676), True))
        self.assertEqual(
            line[37], Marker(duty11, timedelta(seconds=2255.444706), False)
        )
        self.assertEqual(
            line[38], Marker(duty11, timedelta(seconds=11255.444706), True)
        )
        self.assertEqual(
            line[39], Marker(task10, timedelta(seconds=11255.444706), False)
        )
        self.assertEqual(
            line[40], Marker(task10, timedelta(seconds=11265.545716), True)
        )
        self.assertEqual(
            line[41], Marker(duty9, timedelta(seconds=11265.545716), False)
        )
        self.assertEqual(line[42], Marker(duty1, timedelta(seconds=11565.545716), True))
        self.assertEqual(
            line[43], Marker(task8, timedelta(seconds=11565.545716), False)
        )
        self.assertEqual(line[44], Marker(duty9, timedelta(seconds=11691.861505), True))
        self.assertEqual(line[45], Marker(task8, timedelta(seconds=11691.861505), True))

    @skip("deal with after db change")
    def test_seen_apple_crisp_roast_error(self):
        # bake in 350 degree oven for 45-60 minutes until fruit is soft and topping is golden brown
        duty1 = Definition("duty1", 3300, 0.02)
        # Preheat oven to 350 degrees
        duty2 = Definition("duty2", 480, 0.02)
        # Sprinkle crumble evenly over fruit in baking dish
        task3 = Definition("task3", 60, None)
        # Melt butter in microwave and stir into crumble until well coated and crumbly
        duty4 = Definition("duty4", 120, 0.44)
        # Pour the apple mixture into the baking dish
        task5 = Definition("task5", 60, None)
        # Combine sliced apples with other ingredients
        task6 = Definition("task6", 180, None)
        # Slice apples in put in a bowl large enough to mix a little with it
        task7 = Definition("task7", 240, None)
        # Grease a deep dish pie plate or large baking dish cooking spray and set aside
        task8 = Definition("task8", 60, None)
        # Combine crumble components in a medium dish and stir
        task9 = Definition("task9", 240, None)
        duty2.depended = duty1
        task3.depended = duty1
        duty4.depended = task3
        task5.depended = duty4
        task6.depended = task5
        task7.depended = task6
        task8.depended = task5
        task9.depended = duty4
        # put oil in dutch oven
        task10 = Definition("task10", 30, None)
        # put the following in the bowl onion bowl: 1/2 tsp ground ginger, 1/2 tsp pepper, 1 bay leaf,  1 tsp ground cinnamon, 1 tsp salt, 2 tbs sugar, 1 tbs white vinegar, 8 oz tomato sauce, 3/4 cup beer or beef broth, 1 1/4 cup water
        task11 = Definition("task11", 180, None)
        # chop an onion and put it in 4ish cup bowl
        task12 = Definition("task12", 120, None)
        # remove meat and slice
        task13 = Definition("task13", 120, None)
        # reduce heat, cover, and simmer
        duty0 = Definition("duty0", 9900, 0.01)
        # dump ingredients in dutch oven and stir
        task15 = Definition("task15", 30, None)
        # put roast meat in dutch oven and brown all sides
        duty16 = Definition("duty16", 600, 0.1)
        # heat oil in dutch oven
        duty17 = Definition("duty17", 150, 0.02)
        task10.depended = duty17
        task11.depended = task15
        task12.depended = task11
        duty0.depended = task13
        task15.depended = duty0
        duty16.depended = task15
        duty17.depended = duty16
        line = list(
            Timeline(
                [
                    duty1,
                    duty2,
                    task3,
                    duty4,
                    task5,
                    task6,
                    task7,
                    task8,
                    task9,
                    task13,
                    duty0,
                    task15,
                    duty16,
                    duty17,
                    task10,
                    task11,
                    task12,
                ]
            )
        )
        self.assertEqual(line[0], Marker(task10, timedelta(seconds=0.0), False))
        self.assertEqual(line[1], Marker(task10, timedelta(seconds=30.0), True))
        self.assertEqual(line[2], Marker(duty17, timedelta(seconds=30.0), False))
        self.assertEqual(line[3], Marker(task12, timedelta(seconds=30.0), False))
        self.assertEqual(line[4], Marker(task12, timedelta(seconds=152.44898), True))
        self.assertEqual(line[5], Marker(task11, timedelta(seconds=152.44898), False))
        self.assertEqual(line[6], Marker(duty17, timedelta(seconds=180.0), True))
        self.assertEqual(line[7], Marker(duty16, timedelta(seconds=180.0), False))
        self.assertEqual(line[8], Marker(task11, timedelta(seconds=350.0), True))
        self.assertEqual(line[9], Marker(task15, timedelta(seconds=350.0), False))
        self.assertEqual(line[10], Marker(task15, timedelta(seconds=383.333333), True))
        self.assertEqual(line[11], Marker(task9, timedelta(seconds=383.333333), False))
        self.assertEqual(line[12], Marker(task9, timedelta(seconds=650.0), True))
        self.assertEqual(line[13], Marker(task8, timedelta(seconds=650.0), False))
        self.assertEqual(line[14], Marker(task8, timedelta(seconds=716.666667), True))
        self.assertEqual(line[15], Marker(task7, timedelta(seconds=716.666667), False))
        self.assertEqual(line[16], Marker(duty16, timedelta(seconds=780.0), True))
        self.assertEqual(line[17], Marker(duty0, timedelta(seconds=810.0), False))
        self.assertEqual(line[18], Marker(task7, timedelta(seconds=964.545455), True))
        self.assertEqual(line[19], Marker(task6, timedelta(seconds=964.545455), False))
        self.assertEqual(line[20], Marker(task6, timedelta(seconds=1146.363636), True))
        self.assertEqual(line[21], Marker(task5, timedelta(seconds=1146.363636), False))
        self.assertEqual(line[22], Marker(task5, timedelta(seconds=1206.969697), True))
        self.assertEqual(line[23], Marker(duty2, timedelta(seconds=6930.0), False))
        self.assertEqual(line[24], Marker(duty4, timedelta(seconds=7228.14433), False))
        self.assertEqual(line[25], Marker(duty4, timedelta(seconds=7348.14433), True))
        self.assertEqual(line[26], Marker(task3, timedelta(seconds=7348.14433), False))
        self.assertEqual(line[27], Marker(duty2, timedelta(seconds=7410.0), True))
        self.assertEqual(line[28], Marker(task3, timedelta(seconds=7410.0), True))
        self.assertEqual(line[29], Marker(duty1, timedelta(seconds=7410.0), False))
        self.assertEqual(line[30], Marker(duty0, timedelta(seconds=10710.0), True))
        self.assertEqual(line[31], Marker(task13, timedelta(seconds=10710.0), False))
        self.assertEqual(line[32], Marker(duty1, timedelta(seconds=10832.44898), True))
        self.assertEqual(line[33], Marker(task13, timedelta(seconds=10832.44898), True))
