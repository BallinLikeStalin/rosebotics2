"""
  Capstone Project.  Code written by Eric Lee.
  Fall term, 2018-2019.
"""

import rosebotics as rb
import time


def main():
    """ Runs YOUR specific part of the project """
    run_test_wait_until_pressed()
    # run_test_wait_until_released()


def run_test_wait_until_pressed():
    robot = rb.Snatch3rRobot()
    robot.touch_sensor.wait_until_pressed()
    print('this is stupid')


def run_test_wait_until_released():
    robot = rb.Snatch3rRobot()
    robot.touch_sensor.wait_until_released()
    print('i dont like this')


main()
