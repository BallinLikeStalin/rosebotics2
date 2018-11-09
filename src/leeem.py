"""
  Capstone Project.  Code written by Eric Lee.
  Fall term, 2018-2019.
"""

import rosebotics_new as rb
import time

def main():
    """ Runs YOUR specific part of the project """
    # run_test_wait_until_pressed()
    # run_test_wait_until_released()
    #run_test_drive_until_color()
    run_test_beeping()

def run_test_wait_until_pressed():
    robot = rb.Snatch3rRobot()
    robot.touch_sensor.wait_until_pressed()
    print('this is stupid')


def run_test_wait_until_released():
    robot = rb.Snatch3rRobot()
    robot.touch_sensor.wait_until_released()
    print('i dont like this')
# this code is supposed to make it drive until it sees a colour


def run_test_drive_until_color():
    robot = rb.Snatch3rRobot()

    robot.color_sensor.drive_until_color(robot, rb.Color.YELLOW.value)


def run_test_beeping():
    robot = rb.Snatch3rRobot()
    robot.proximity_sensor.beep_if_in_range()




main()
