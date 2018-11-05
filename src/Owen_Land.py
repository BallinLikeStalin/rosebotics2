"""
  Capstone Project.  Code written by PUT_YOUR_NAME_HERE.
  Fall term, 2018-2019.
"""

import rosebotics_new as rb
import ev3dev.ev3 as ev3


def main():
    """ Runs YOUR specific part of the project """
    run_test_camera_beep()


def run_test_inches():
    robot = rb.Snatch3rRobot()

    robot.drive_system.go_straight_inches(10, 75)


def run_test_spin():
    robot = rb.Snatch3rRobot()

    robot.drive_system.spin_in_place_degrees(360, 50)


def run_test_turn():
    robot = rb.Snatch3rRobot()

    robot.drive_system.turn_degrees(180/(4-2), 50)


def run_test_polygon():

    robot = rb.Snatch3rRobot()

    robot.drive_system.drive_polygon(6, 75)


def run_test_camera_beep():
    robot = rb.Snatch3rRobot()
    while True:
        if robot.camera.get_biggest_blob().get_area() >= 600:
            ev3.Sound.beep().wait()
        if robot.touch_sensor.is_pressed() == 1:
            return


main()
