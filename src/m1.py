"""
  Capstone Project.  Code written by PUT_YOUR_NAME_HERE.
  Fall term, 2018-2019.
"""

import rosebotics as rb
import time


def main():
    """ Runs YOUR specific part of the project """
    #run_test_inches()
    run_test_spin()


def run_test_inches():
    robot = rb.Snatch3rRobot()

    robot.drive_system.go_straight_inches(10, 75)

def run_test_spin():
    robot = rb.Snatch3rRobot()

    robot.drive_system.spin_in_place_degrees(-360, 50)

main()
