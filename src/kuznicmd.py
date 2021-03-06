"""
  Capstone Project.  Code written by Michael Kuznicki.
  Fall term, 2018-2019.
"""

import rosebotics_new as rb
import time


def main():
    """ Runs YOUR specific part of the project """

    # run_test_wait_until_intensity_is_less_than()
    # run_test_wait_until_intensity_is_greater_than()
    # run_test_wait_until_color_is()
    # run_test_wait_until_color_is_one_of()
    # run_test_follow_line()
    # run_test_raise_arm_and_close_claw()
    # run_test_calibrate()
    # run_test_move_arm_to_position()
    test2()


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
    robot.color_sensor.wait_until_color_is(rb.Color.YELLOW.value)
    print('YAY 3')


def run_test_wait_until_color_is_one_of():

    robot = rb.Snatch3rRobot()
    robot.color_sensor.wait_until_color_is_one_of([rb.Color.BLUE.value, rb.Color.GREEN.value, rb.Color.YELLOW.value,
                                                   rb.Color.RED])
    print('YAY 4')


def run_test_follow_line():

    robot = rb.Snatch3rRobot()
    robot.color_sensor.follow_line(robot)


def run_test_raise_arm_and_close_claw():

    robot = rb.Snatch3rRobot()
    robot.arm.raise_arm_and_close_claw()


def run_test_calibrate():

    robot = rb.Snatch3rRobot()
    robot.arm.calibrate()


def run_test_move_arm_to_position():

    robot = rb.Snatch3rRobot()
    robot.arm.move_arm_to_position((14.2 * 360) / (4 / 3))


def test():
    rover = rb.Snatch3rRobot()
    rover.drive_system.start_spinning_left(50)
    while True:
        piece = rover.camera.get_biggest_blob()

        if piece.is_against_left_edge() is True:
            rover.drive_system.start_spinning_left()
            while True:
                if piece.center.x == 0:
                    rover.drive_system.stop_moving()

        if piece.is_against_right_edge() is True:
            rover.drive_system.start_spinning_right()
            while True:
                if piece.center.x == 0:
                    rover.drive_system.stop_moving()


def test1():
    rover = rb.Snatch3rRobot()




def test2():
    rover = rb.Snatch3rRobot()

    while True:
        print(rover.beacon_sensor.get_distance_to_beacon())


main()
