"""
  Capstone Project.  Code written by Michael Kuznicki.
  Fall term, 2018-2019.
"""

import rosebotics as rb
import time


def main():
    """ Runs YOUR specific part of the project """

    # run_test_wait_until_intensity_is_less_than()
    # run_test_wait_until_intensity_is_greater_than()
    run_test_wait_until_color_is()
    # run_test_wait_until_color_is_one_of()


def run_test_wait_until_intensity_is_less_than():

    robot = rb.Snatch3rRobot()

    robot.color_sensor.wait_until_intensity_is_less_than(50)

    print('YAY 1')


def run_test_wait_until_intensity_is_greater_than():

    robot = rb.Snatch3rRobot()

    robot.color_sensor.wait_until_intensity_is_greater_than(50)

    print('YAY 2')


def run_test_wait_until_color_is():

    # print(rb.Color.RED.value)
    robot = rb.Snatch3rRobot()

    robot.color_sensor.wait_until_color_is(rb.Color.RED.value)

    print('YAY 3')


def run_test_wait_until_color_is_one_of():

    robot = rb.Snatch3rRobot()

    robot.color_sensor.wait_until_color_is_one_of([rb.Color.BLUE.value, rb.Color.GREEN.value, rb.Color.YELLOW.value,
                                                   rb.Color.RED])

    print('YAY 4')


main()
