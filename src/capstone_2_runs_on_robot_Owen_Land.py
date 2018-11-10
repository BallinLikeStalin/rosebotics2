"""
Mini-application:  Buttons on a Tkinter GUI tell the robot to:
  - Go forward at the speed given in an entry box.

Also: responds to Beacon button-presses by beeping, speaking.

This module runs on the ROBOT.
It uses MQTT to RECEIVE information from a program running on the LAPTOP.

Authors:  David Mutchler, his colleagues, and Owen Land.
"""
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

import rosebotics_new as rb
import time
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3


def main():
    robot = rb.Snatch3rRobot()
    rc = RemoteControlEtc(robot)
    mqtt_client = com.MqttClient(rc)
    mqtt_client.connect_to_pc()

    while True:

        time.sleep(0.01)  # For the delegate to do its work


class RemoteControlEtc(object):
    def __init__(self, robot):
        """
        Stores the robot.
          :type   robot: rb.Snatch3rRobot
        """
        self.robot = robot

    def go_forward(self, speed_string):
        print('Telling the robot to start moving at', speed_string)
        speed = int(speed_string)
        self.robot.drive_system.start_moving(speed, speed)

        while True:
            if self.robot.proximity_sensor.get_distance_to_nearest_object() < 5:
                self.robot.drive_system.stop_moving()
                self.robot.arm.raise_arm_and_close_claw()
                time.sleep(5)
                break
            break

        while True:
            if self.robot.color_sensor.get_color() is rb.Color.BLUE:
                self.robot.drive_system.stop_moving()
                self.robot.arm.calibrate()
                time.sleep(5)
                ev3.Sound.speak("Looks Cold Now").wait()
                self.robot.arm.raise_arm_and_close_claw()
                ev3.Sound.speak("Cheers").wait()
                break
            break

    def go_backward(self, speed_string):
        print('Telling the robot to start moving at', speed_string)
        speed = int(speed_string)
        self.robot.drive_system.start_moving(-speed, -speed)

    def go_left(self, degrees_string):
        print('Telling the robot to turn left', degrees_string)
        degrees = int(degrees_string)
        self.robot.drive_system.turn_degrees(-degrees, 50)

    def go_right(self, degrees_string):
        print('Telling the robot to turn right', degrees_string)
        degrees = int(degrees_string)
        self.robot.drive_system.turn_degrees(degrees, 50)

    def stop_moving(self):
        self.robot.drive_system.stop_moving()


main()
