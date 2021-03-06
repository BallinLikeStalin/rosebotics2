"""
Mini-application:  Buttons on a Tkinter GUI tell the robot to:
  - Go forward at the speed given in an entry box.

Also: responds to Beacon button-presses by beeping, speaking.

This module runs on the ROBOT.
It uses MQTT to RECEIVE information from a program running on the LAPTOP.

Authors:  David Mutchler, his colleagues, and Michael Kuznicki.
"""
# ------------------------------------------------------------------------------
# DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.  Then delete this TO DO.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# TODO: 2. With your instructor, review the "big picture" of laptop-robot
# TODO:    communication, per the comment in mqtt_sender.py.
# TODO:    Once you understand the "big picture", delete this TODO.
# ------------------------------------------------------------------------------

import rosebotics_new as rb
import time
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3


def main():
    # --------------------------------------------------------------------------
    # TODO: 3. Construct a Snatch3rRobot.  Test.  When OK, delete this TODO.
    # --------------------------------------------------------------------------

    robot = rb.Snatch3rRobot()

    # --------------------------------------------------------------------------
    # TODO: 4. Add code that constructs a   com.MqttClient   that will
    # TODO:    be used to receive commands sent by the laptop.
    # TODO:    Connect it to this robot.  Test.  When OK, delete this TODO.
    # --------------------------------------------------------------------------

    rc = RemoteControlEtc(robot)
    mqtt_client = com.MqttClient(rc)
    mqtt_client.connect_to_pc()

    # --------------------------------------------------------------------------
    # TODO: 5. Add a class for your "delegate" object that will handle messages
    # TODO:    sent from the laptop.  Construct an instance of the class and
    # TODO:    pass it to the MqttClient constructor above.  Augment the class
    # TODO:    as needed for that, and also to handle the go_forward message.
    # TODO:    Test by PRINTING, then with robot.  When OK, delete this TODO.
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # TODO: 6. With your instructor, discuss why the following WHILE loop,
    # TODO:    that appears to do nothing, is necessary.
    # TODO:    When you understand this, delete this TODO.
    # --------------------------------------------------------------------------
    while True:
        # ----------------------------------------------------------------------
        # TODO: 7. Add code that makes the robot beep if the top-red button
        # TODO:    on the Beacon is pressed.  Add code that makes the robot
        # TODO:    speak "Hello. How are you?" if the top-blue button on the
        # TODO:    Beacon is pressed.  Test.  When done, delete this TODO.
        # ----------------------------------------------------------------------
        if robot.beacon_button_sensor.is_top_red_button_pressed():
            ev3.Sound.beep().wait()

        if robot.beacon_button_sensor.is_top_blue_button_pressed():
            ev3.Sound.speak('Hello. How are you?').wait()

        time.sleep(0.01)  # For the delegate to do its work


class RemoteControlEtc(object):
    def __init__(self, robot):
        """
        Stores the robot.
           :type robot: rb.Snatch3rRobot
        """

        self.robot = robot

    def go_forward(self, speed_string):
        """ Makes the robot go forward at the given speed. """

        print("Telling the robot to start moving at", speed_string)
        speed = int(speed_string)
        self.robot.drive_system.start_moving(speed, speed)


# main()

def run_game():
    """
    Constructs the robot.
    Tells the robot to stop moving and raise its arm when it is 0 inches away from the beacon.
    Also, tells the robot to wait until it sees a color with an intensity greater than 50 (white).
    """

    rover = rb.Snatch3rRobot()

    rc = RemoteControl(rover)
    mqtt_client = com.MqttClient(rc)
    mqtt_client.connect_to_pc()

    while True:
        if abs(rover.beacon_sensor.get_distance_to_beacon()) == 0:
            rover.drive_system.stop_moving()
            rover.arm.raise_arm_and_close_claw()

        if rover.color_sensor.get_reflected_intensity() > 50:
            rover.drive_system.stop_moving()
            rover.arm.calibrate()
            break

        time.sleep(0.01)


class RemoteControl(object):
    def __init__(self, rover):
        """
        Stores the robot.
            :type rover: rb.Snatch3rRobot
        """
        self.rover = rover

    def turn_left(self, speed):
        """
        Tells the robot to turn left at a given speed.
        """

        self.stop()
        print('Telling the robot to turn left at the speed: ', speed)
        speed = int(speed)
        self.rover.drive_system.start_spinning_left(speed)

    def turn_right(self, speed):
        """
        Tells the robot to turn right at a given speed.
        """

        self.stop()
        print('Telling the robot to turn right at the speed: ', speed)
        speed = int(speed)
        self.rover.drive_system.start_spinning_right(speed)

    def move_forward(self, speed):
        """
        Tells the robot to move forward at a given speed.
        """

        self.stop()
        print('Telling the robot to move forward at the speed: ', speed)
        speed = int(speed)
        self.rover.drive_system.start_moving(speed, speed)

    def move_backward(self, speed):
        """
        Tells the robot to move backward at a given speed.
        """

        self.stop()
        print('Telling the robot to move backward at the speed: ', speed)
        speed = int(speed)
        self.rover.drive_system.start_moving(-speed, -speed)

    def stop(self):
        """
        Tells the robot to stop.
        """

        self.rover.drive_system.stop_moving()


run_game()
