"""
  Capstone Project.
  This module contains high-level, general-purpose methods for a Snatch3r robot.

  Team members:  Eric Lee, Owen Land, and Michael Kuznicki.
  Fall term, 2018-2019.
"""
# DONE: Put your names in the above.
# DONE: Do the TO DO's below.
# DONE: Augment this module as appropriate, being sure to always
# DONE:   ** coordinate with your teammates ** in doing so.

from ev3dev import ev3
from enum import Enum
import low_level_rosebotics_new as low_level_rb
import time

# ------------------------------------------------------------------------------
# Global constants.  Reference them as (for example):  rb.BRAKE   rb.GREEN
# ------------------------------------------------------------------------------
COAST = 'coast'
BRAKE = 'brake'
HOLD = 'hold'

NO_COLOR = 0
BLACK = 1
BLUE = 2
GREEN = 3
YELLOW = 4
RED = 5
WHITE = 6
BROWN = 7

# For buttons on the Brick:
TOP_BUTTON = 0
BOTTOM_BUTTON = 1
LEFT_BUTTON = 2
RIGHT_BUTTON = 3
MIDDLE_BUTTON = 4
BACK_BUTTON = 5

# For buttons on the Beacon:
TOP_RED_BUTTON = 6
BOTTOM_RED_BUTTON = 7
TOP_BLUE_BUTTON = 8
BOTTOM_BLUE_BUTTON = 9
BEACON_BUTTON = 10


# ------------------------------------------------------------------------------
# The same global constants, but done in a way that is better practice.
# Reference them as (for example):   StopAction.BRAKE.value   Color.GREEN.value
# For this Capstone Project, use whichever form you prefer.
# ------------------------------------------------------------------------------
class StopAction(Enum):
    COAST = 'coast'
    BRAKE = 'brake'
    HOLD = 'hold'


class Color(Enum):
    NO_COLOR = 0
    BLACK = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    RED = 5
    WHITE = 6
    BROWN = 7


class Button(Enum):
    # For buttons on the Brick:
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    BACK = 4

    # For buttons on the Beacon:
    TOP_RED = 5
    BOTTOM_RED = 6
    TOP_LEFT = 7
    BOTTOM_LEFT = 8
    BEACON = 9


# ------------------------------------------------------------------------------
# The Snatch3rRobot class, followed by classes for its components.
# A Snatch3rRobot has the following instance variables, with associated classes:
#
# Sensors:
#   self.touch_sensor:   TouchSensor
#   self.color_sensor:   ColorSensor
#   self.camera:         Camera
#
#   self.proximity_sensor:      InfraredAsProximitySensor
#   self.beacon_sensor:         InfraredAsBeaconSensor
#   self.beacon_button_sensor:  InfraredAsBeaconButtonSensor
#
#   self.top_button:      BrickButton    (these are buttons on the EV3 brick)
#   self.bottom_button:   BrickButton
#   self.left_button:     BrickButton
#   self.right_button:    BrickButton
#   self.back_button:     BrickButton
#
# Motors and sensors, combined:
#   self.drive_system:   DriveSystem
#   self.arm:            ArmAndClaw
# ------------------------------------------------------------------------------
class Snatch3rRobot(object):
    """
    An EV3 Snatch3r Robot.
    Primary authors:  The ev3dev authors, David Mutchler, Dave Fisher,
       their colleagues, and the entire team.
    """

    def __init__(self,
                 left_wheel_port=ev3.OUTPUT_B,
                 right_wheel_port=ev3.OUTPUT_C,
                 arm_port=ev3.OUTPUT_A,
                 touch_sensor_port=ev3.INPUT_1,
                 camera_port=ev3.INPUT_2,
                 color_sensor_port=ev3.INPUT_3,
                 ir_sensor_port=ev3.INPUT_4):
        """
        A  Snatch3rRobot  object has other objects as components:
        drive_system, touch_sensor, camera, color_sensor, etc.
        The robot "delegates" its work to the appropriate component.
        """
        self.touch_sensor = TouchSensor(touch_sensor_port)
        self.color_sensor = ColorSensor(color_sensor_port)
        self.camera = Camera(camera_port)

        self.proximity_sensor = InfraredAsProximitySensor(ir_sensor_port)
        # self.beacon_sensor = InfraredAsBeaconSensor(channel=1)
        # self.beacon_button_sensor = InfraredAsBeaconButtonSensor(ir_sensor,
        #                                                          channel=1)

        self.brick_button_sensor = BrickButtonSensor()

        self.drive_system = DriveSystem(left_wheel_port, right_wheel_port)
        self.arm = ArmAndClaw(self.touch_sensor, arm_port)


class DriveSystem(object):
    """
    A class for driving (moving) the robot.
    Primary authors:  The ev3dev authors, David Mutchler, Dave Fisher,
       their colleagues, the entire team, and Owen Land.
    """

    # DONE: In the above line, put the name of the primary author of this class.

    def __init__(self,
                 left_wheel_port=ev3.OUTPUT_B,
                 right_wheel_port=ev3.OUTPUT_C):
        """
        A DriveSystem has   self.left_wheel   and   self.right_wheel.
        """
        self.left_wheel = low_level_rb.Wheel(left_wheel_port)
        self.right_wheel = low_level_rb.Wheel(right_wheel_port)

    def start_moving(self,
                     left_wheel_duty_cycle_percent=100,
                     right_wheel_duty_cycle_percent=100):
        """
        STARTS the robot MOVING at the given wheel speeds
        (-100 to 100, where negative means spinning backward).
        """
        self.left_wheel.start_spinning(left_wheel_duty_cycle_percent)
        self.right_wheel.start_spinning(right_wheel_duty_cycle_percent)

    def stop_moving(self, stop_action=StopAction.BRAKE.value):
        """
        STOPS the robot, using the given StopAction (which defaults to BRAKE).
        """
        self.left_wheel.stop_spinning(stop_action)
        self.right_wheel.stop_spinning(stop_action)

    def move_for_seconds(self,
                         seconds,
                         left_wheel_duty_cycle_percent=100,
                         right_wheel_duty_cycle_percent=100,
                         stop_action=StopAction.BRAKE):
        """
        Makes the robot MOVE for the given number of SECONDS at the given
        wheel speeds (-100 to 100, where negative means spinning backward),
        stopping using the given StopAction (which defaults to BRAKE).
        """
        self.start_moving(left_wheel_duty_cycle_percent,
                          right_wheel_duty_cycle_percent)
        # For pedagogical purposes, we use a WHILE loop to keep going for a
        # given number of seconds, instead of using the simpler alternative:
        #      time.sleep(seconds)
        self.start_moving(left_wheel_duty_cycle_percent,
                          right_wheel_duty_cycle_percent)
        start_time = time.time()
        while True:
            if time.time() - start_time > seconds:
                self.stop_moving(stop_action.value)
                break

    def go_straight_inches(self,
                           inches,
                           duty_cycle_percent=100,
                           stop_action=StopAction.BRAKE):
        """
        Makes the robot GO STRAIGHT for the given number of INCHES
        at the given speed (-100 to 100, where negative means moving backward),
        stopping using the given StopAction (which defaults to BRAKE).
        """
        # DONE: Use one of the Wheel object's   get_degrees_spun   method.
        # DONE: Do a few experiments to determine the constant that converts
        # DONE:   from wheel-DEGREES-spun to robot-INCHES-moved.
        # DONE:   Assume that the conversion is linear with respect to speed.
        # DONE: Don't forget that the Wheel object's position begins wherever
        # DONE:   it last was, not necessarily 0.

        self.left_wheel.reset_degrees_spun()
        self.start_moving(duty_cycle_percent, duty_cycle_percent)

        while True:
            if self.left_wheel.get_degrees_spun() > inches * 85:
                self.stop_moving()
                break

    def spin_in_place_degrees(self,
                              degrees,
                              duty_cycle_percent=100,
                              stop_action=StopAction.BRAKE):
        """
        Makes the robot SPIN IN PLACE for the given number of DEGREES
        at the given speed (-100 to 100, where POSITIVE means CLOCKWISE
        and NEGATIVE means COUNTER-CLOCKWISE),
        stopping using the given StopAction (which defaults to BRAKE).
        "Spinning in place" means that both wheels spin at the same speed
        but in opposite directions.
        """
        # DONE: Use one of the Wheel object's   get_degrees_spun   method.
        # DONE: Do a few experiments to determine the constant that converts
        # DONE:   from WHEEL-degrees-spun to ROBOT-degrees-spun.
        # DONE:   Assume that the conversion is linear with respect to speed.
        # DONE: Don't forget that the Wheel object's position begins wherever
        # DONE:   it last was, not necessarily 0.

        self.left_wheel.reset_degrees_spun(0)
        if degrees > 0:
            z = 1
        else:
            z = -1

        self.start_moving((z * duty_cycle_percent), (-z * duty_cycle_percent))

        while True:
            if self.left_wheel.get_degrees_spun() > 5.5 * abs(degrees):
                self.stop_moving(stop_action)
                break

    def turn_degrees(self,
                     degrees,
                     duty_cycle_percent=100,
                     stop_action=StopAction.BRAKE):
        """
        Makes the robot TURN for the given number of DEGREES
        at the given speed (-100 to 100, where POSITIVE means CLOCKWISE
        and NEGATIVE means COUNTER-CLOCKWISE),
        stopping using the given StopAction (which defaults to BRAKE).
        "Turning" means that both ONE wheel spins at the given speed and the
        other wheel does NOT spin.
        """
        # DONE: Use the Wheel object's   get_degrees_spun   method.
        # DONE: Do a few experiments to determine the constant that converts
        # DONE:   from WHEEL-degrees-SPUN to ROBOT-degrees-TURNED.
        # DONE:   Assume that the conversion is linear with respect to speed.
        # DONE: Don't forget that the Wheel object's position begins wherever
        # DONE:   it last was, not necessarily 0.

        self.left_wheel.reset_degrees_spun(0)
        if degrees > 0:
            z = 1
            self.start_moving((z * duty_cycle_percent), 0)
        else:
            z = -1
            self.start_moving((z * duty_cycle_percent), 0)

        while True:
            if abs(self.left_wheel.get_degrees_spun()) > 10 * abs(degrees):
                self.stop_moving(stop_action)
                break

    def drive_polygon(self, n, duty_cycle):
        for k in range(n):
            self.go_straight_inches(5, duty_cycle)
            self.turn_degrees(180-(180*(n-2)/n), duty_cycle)


class TouchSensor(low_level_rb.TouchSensor):
    """
    A class for an EV3 touch sensor.
    Primary authors:  The ev3dev authors, David Mutchler, Dave Fisher,
       their colleagues, the entire team, and PUT_YOUR_NAME_HERE.
    """

    def __init__(self, port=ev3.INPUT_1):
        super().__init__(port)

    def is_pressed(self):
        """ Returns True if the TouchSensor is currently pressed. """
        if self.get_value() == 1:
            return True
        else:
            return False

    def wait_until_pressed(self):
        """ Waits (doing nothing new) until the touch sensor is pressed. """
        # DONE.

        while True:
            if self.get_value == 1:
                break

    def wait_until_released(self):
        """ Waits (doing nothing new) until the touch sensor is released. """
        # DONE

        while True:
            if self.get_value == 0:
                break


class ColorSensor(low_level_rb.ColorSensor):
    """
    A class for an EV3 color sensor.
    Primary authors:  The ev3dev authors, David Mutchler, Dave Fisher,
       their colleagues, the entire team, and PUT_YOUR_NAME_HERE.
    """

    def __init__(self, port=ev3.INPUT_3):
        super().__init__(port)

    def get_color(self):
        """
        Returns its best guess as to the color of the object upon which it is
        shining R/G/B pulses of light.  The value returned is one of:
          Color.NO_COLOR   Color.BLACK   Color.BLUE    Color.GREEN
          Color.YELLOW     Color.RED     Color.WHITE   Color.BROWN
        """
        return super().get_color()

    def get_reflected_intensity(self):
        """
        Returns how much light is reflected by the light emitted by the sensor,
        ranging from 0 (no light reflected) to 100 (maximum light reflected).
        """
        return super().get_reflected_intensity()

    def get_value(self):
        """
         Returns a 3-tuple (R, G, B) where
          - R/G/B is the amount of Red/Green/Blue light reflected, respectively,
          - each number is in the range from 0 (none reflected) to 1020.
        """
        return super().get_value()

    def red(self):
        """ Returns the amount of light reflected by a RED light. """
        return super().red()

    def green(self):
        """ Returns the amount of light reflected by a GREEN light. """
        return super().green()

    def blue(self):
        """ Returns the amount of light reflected by a BLUE light. """
        return super().blue()

    def wait_until_intensity_is_less_than(self, reflected_light_intensity):
        """
        Waits (doing nothing new) until the sensor's measurement of reflected
        light intensity is less than the given value (threshold), which should
        be between 0 (no light reflected) and 100 (maximum light reflected).
        """
        # DONE.

        while True:
            if self.get_reflected_intensity() < reflected_light_intensity:
                break

    def wait_until_intensity_is_greater_than(self, reflected_light_intensity):
        """
        Waits (doing nothing new) until the sensor's measurement of reflected
        light intensity is greater than the given value (threshold), which
        should be between 0 (no light reflected) and 100 (max light reflected).
        """
        # DONE.

        while True:
            if self.get_reflected_intensity() > reflected_light_intensity:
                break

    def wait_until_color_is(self, color):
        """
        Waits (doing nothing new) until the sensor's measurement
        of what color it sees is the given color.
        The given color must be a Color (as defined above).
        """
        # DONE.

        while True:
            if self.get_color() is color:
                return 9

    def wait_until_color_is_one_of(self, colors):
        """
        Waits (doing nothing new) until the sensor's measurement
        of what color it sees is any one of the given sequence of colors.
        Each item in the sequence must be a Color (as defined above).
        """
        # DONE.

        while True:
            for k in range(len(colors)):
                if self.get_color() is colors[k]:
                    return

    def drive_until_color(self, robot, color):
        robot.drive_system.start_moving(25, 25)
        self.wait_until_color_is(color)
        robot.drive_system.stop_moving()

    def follow_line(self, robot):
        robot.drive_system.start_moving(100, 100)
        x = self.get_reflected_intensity()
        while True:
            if x > 50:
                robot.drive_system.turn_degrees(5, 100)
            x = self.get_reflected_intensity()
            robot.drive_system.start_moving(100, 100)
        robot.drive_system.stop_moving()


class Camera(object):
    """
    A class for a Pixy camera.
    Use the   PixyMon    program to initialize the camera's firmware.
    Download the program from the    Windows   link at:
        http://www.cmucam.org/projects/cmucam5/wiki/Latest_release

    Learn how to use the Pixy camera's "color signatures" to recognize objects
        at: http://www.cmucam.org/projects/cmucam5/wiki/Teach_Pixy_an_object.

    Primary authors:  The ev3dev authors, David Mutchler, Dave Fisher,
       their colleagues, the entire team, and PUT_YOUR_NAME_HERE.
    """

    def __init__(self, port=ev3.INPUT_2):
        try:
            self.low_level_camera = ev3.Sensor(port, driver_name="pixy-lego")
        except AssertionError:
            print("Is the camera plugged into port 2?")
            print("If that is not the problem, then check whether the camera")
            print("has gotten into 'Arduino mode', as follows:")
            print("  In PixyMon, select the gear (Configure) icon,")
            print("  then look for a tab that has 'Arduino' on its page.")
            print("  Make sure it says 'Lego' and not 'Arduino'.")
            print("Note: Only some of the cameras have this option;")
            print("the others are automatically OK in this regard.")
        self.set_signature("SIG1")

    def set_signature(self, signature_name):
        self.low_level_camera.mode = signature_name

    def get_biggest_blob(self):
        """
        A "blob" is a collection of connected pixels that are all in the color
        range specified by a color "signature".  A Blob object stores the Point
        that is the center (actually, centroid) of the blob along with the
        width and height of the blob.  For a Pixy camera, the x-coordinate is
        between 0 and 319 (0 left, 319 right) and the y-coordinate is between
        0 and 199 (0 TOP, 199 BOTTOM).  See the Blob class below.

        A Camera returns the largest Blob whose pixels fall within the Camera's
        current color signature.  A Blob whose width and height are zero
        indicates that no large enough object within the current color signature
        was visible.

        The Camera's color signature defaults to "SIG1", which is the color
        signature set by selecting the RED light when training the Pixy camera.
        """
        return Blob(Point(self.low_level_camera.value(1),
                          self.low_level_camera.value(2)),
                    self.low_level_camera.value(3),
                    self.low_level_camera.value(4))



class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Blob(object):
    """
    Represents a rectangle in the form that a Pixy camera uses:
      upper-left corner along with width and height.
    """

    def __init__(self, center, width, height):
        self.center = center
        self.width = width
        self.height = height
        self.screen_limits = Point(320, 240)  # FIXME

    def __repr__(self):
        return "center: ({:3d}, {:3d})  width, height: {:3d} {:3d}.".format(
            self.center.x, self.center.y, self.width, self.height)

    def get_area(self):
        return self.width * self.height

    def is_against_left_edge(self):
        return self.center.x - (self.width + 1) / 2 <= 0

    def is_against_right_edge(self):
        return self.center.x + (self.width / 2 + 1) / 2 >= self.screen_limits.x

    def is_against_top_edge(self):
        return self.center.y - (self.height + 1) / 2 <= 0

    def is_against_bottom_edge(self):
        return self.center.y + (self.height + 1) / 2 >= self.screen_limits.y

    def is_against_an_edge(self):
        return (self.is_against_left_edge()
                or self.is_against_right_edge()
                or self.is_against_top_edge()
                or self.is_against_bottom_edge())


class InfraredAsProximitySensor(low_level_rb.InfraredSensor):
    """
    A class for the infrared sensor when it is in the mode in which it
    measures distance to the nearest object that it sees.
    Primary authors:  The ev3dev authors, David Mutchler, Dave Fisher,
       their colleagues, the entire team, and Eric Lee.
    """
    # done: In the above line, put the name of the primary author of this class.

    def __init__(self, ir_sensor_port):
        super().__init__(ir_sensor_port)

    def get_distance_to_nearest_object(self):
        """
        Returns the distance to the nearest object in its field of vision,
        as a integer between 0 and 100, where a value N indicates that the
        distance to the nearest object is 70 * (N/100) cm.  For example:
           - numbers < 10 indicate that the object is less than 7 cm away
           - 20 means 1/5 of 70, i.e., 14 cm
           - 40 means 2/5 of 70, i.e., 28 cm
           - 50 means 1/2 of 70, i.e., 35 cm
           - greater than 70 is too far away to be useful
               (more precisely, greater than 49 cm away)
           - 100 is the maximum distance for the sensor, namely, 100 cm.
        """
        return super().get_distance_to_nearest_object()

    def get_distance_to_nearest_object_in_inches(self):
        """
        Returns the distance to the nearest object in its field of vision,
        in inches, where about 39.37 inches (which is 100 cm) means no object
        is within its field of vision.
        """
        inches_per_cm = 1 / 2.54
        return 70 * inches_per_cm * self.get_distance_to_nearest_object() / 100

    def beep_if_in_range(self):
        while True:
            if self.get_distance_to_nearest_object_in_inches() > 9:
                if self.get_distance_to_nearest_object_in_inches() < 15:
                    ev3.Sound.speak('beep')


class InfraredAsBeaconSensor(object):
    """
    A class for the infrared sensor when it is in the mode in which it
    measures the heading and distance to the Beacon when the Beacon is emitting
    its signal continuously ("beacon mode") on one of its 4 channels (1 to 4).
    Primary authors:  The ev3dev authors, David Mutchler, Dave Fisher,
    their colleagues, and the entire team.
    """

    def __init__(self, channel=1):
        self.channel = channel
        self._underlying_ir_sensor = ev3.BeaconSeeker()

    def set_channel(self, channel):
        """
        Makes this sensor look for signals on the given channel. The physical
        Beacon has a switch that can set the channel to 1, 2, 3 or 4.
        """
        self.channel = channel
        self._underlying_ir_sensor = ev3.BeaconSeeker()

    def get_channel(self):
        return self.channel

    def get_heading_and_distance_to_beacon(self):
        """
        Returns a 2-tuple containing the heading and distance to the Beacon.
        Looks for signals at the frequency of the given channel,
        or at the InfraredAsBeaconSensor's channel if channel is None.
         - The heading is in degrees in the range -25 to 25 with:
             - 0 means straight ahead
             - negative degrees mean the Beacon is to the left
             - positive degrees mean the Beacon is to the right
         - Distance is from 0 to 100, where 100 is about 70 cm
         - -128 means the Beacon is not detected.
        """
        return self._underlying_ir_sensor.heading_and_distance

    def get_heading_to_beacon(self):
        """
        Returns the heading to the Beacon.
        Units are per the   get_heading_and_distance_to_beacon   method.
        """
        return self._underlying_ir_sensor.heading

    def get_distance_to_beacon(self):
        """
        Returns the heading to the Beacon.
        Units are per the   get_heading_and_distance_to_beacon   method.
        """
        return self._underlying_ir_sensor.distance


class InfraredAsBeaconButtonSensor(object):
    """
    A class for the infrared sensor when it is in the mode in which it
    measures which (if any) of the Beacon buttons are being pressed.
    Primary authors:  The ev3dev authors, David Mutchler, Dave Fisher,
    their colleagues, the entire team, and PUT_YOUR_NAME_HERE.
    """
    # TODO: In the above line, put the name of the primary author of this class.

    def __init__(self, ir_sensor, channel=1):
        self._underlying_ir_sensor = ir_sensor
        if channel:  # None means use the given InfraredSensor's channel
            self._underlying_ir_sensor.channel = channel
        self._underlying_remote_control = \
            low_level_rb.BeaconButtonController(ir_sensor, channel)
        self.button_names = {
            "red_up": TOP_RED_BUTTON,
            "red_down": BOTTOM_RED_BUTTON,
            "blue_up": TOP_BLUE_BUTTON,
            "blue_down": BOTTOM_BLUE_BUTTON,
            "beacon": BEACON_BUTTON
        }

    def set_channel(self, channel):
        """
        Makes this sensor look for signals on the given channel. The physical
        Beacon has a switch that can set the channel to 1, 2, 3 or 4.
        """
        self._underlying_ir_sensor.channel = channel

    def get_channel(self):
        return self._underlying_ir_sensor.channel

    def get_buttons_pressed(self):
        """
        Returns a list of the numbers corresponding to buttons on the Beacon
        which are currently pressed.
        """
        button_list = self._underlying_remote_control.buttons_pressed
        for k in range(len(button_list)):
            button_list[k] = self.button_names[button_list[k]]

    def is_top_red_button_pressed(self):
        return self._underlying_remote_control.red_up

    def is_bottom_red_button_pressed(self):
        return self._underlying_remote_control.red_down

    def is_top_blue_button_pressed(self):
        return self._underlying_remote_control.blue_up

    def is_bottom_blue_button_pressed(self):
        return self._underlying_remote_control.buttons_pressed

    def is_beacon_button_pressed(self):
        return self._underlying_remote_control.buttons_pressed


class BrickButtonSensor(object):
    """
    A class for the buttons on the Brick.
    Primary authors:  The ev3dev authors, David Mutchler, Dave Fisher,
    their colleagues, the entire team, and PUT_YOUR_NAME_HERE.
    """
    # TODO: In the above line, put the name of the primary author of this class.

    def __init__(self):
        self._underlying_sensor = low_level_rb.BrickButtonSensor()
        self.button_names = {
            "up": TOP_BUTTON,
            "down": BOTTOM_BUTTON,
            "left": LEFT_BUTTON,
            "right": RIGHT_BUTTON,
            "enter": MIDDLE_BUTTON,
            "backspace": BACK_BUTTON
        }

    def process(self):
        self._underlying_sensor.process()

    def get_buttons_pressed(self):
        """
        Returns a list of the numbers corresponding to buttons on the Beacon
        which are currently pressed.
        """
        self.process()
        button_list = self._underlying_sensor.buttons_pressed
        for k in range(len(button_list)):
            button_list[k] = self.button_names[button_list[k]]

    def is_top_button_pressed(self):
        return self._underlying_sensor.up

    def is_bottom_button_pressed(self):
        return self._underlying_sensor.down

    def is_left_button_pressed(self):
        return self._underlying_sensor.left

    def is_right_button_pressed(self):
        return self._underlying_sensor.right

    def is_middle_button_pressed(self):
        return self._underlying_sensor.enter

    def is_back_button_pressed(self):
        return self._underlying_sensor.backspace


class ArmAndClaw(object):
    """
    A class for the arm and its associated claw.
    Primary authors:  The ev3dev authors, David Mutchler, Dave Fisher,
    their colleagues, the entire team, and Michael Kuznicki.
    """
    # DONE: In the above line, put the name of the primary author of this class.

    def __init__(self, touch_sensor, port=ev3.OUTPUT_A):
        # The ArmAndClaw's  motor  is not really a Wheel, of course,
        # but it can do exactly what a Wheel can do.
        self.motor = low_level_rb.Wheel(port, is_arm=True)

        # The ArmAndClaw "has" the TouchSensor that is at the back of the Arm.
        self.touch_sensor = touch_sensor

        # Sets the motor's position to 0 (the DOWN position).
        # At the DOWN position, the robot fits in its plastic bin,
        # so we start with the ArmAndClaw in that position.
        self.calibrate()

    def calibrate(self):
        """
        Raise the arm at a reasonable speed until the touch sensor is pressed.
        Then lower the arm 14.2 revolutions (i.e., 14.2 * 360 degrees),
        again at a reasonable speed. Then set the motor's position to 0.
        (Hence, 0 means all the way DOWN and 14.2 * 360 means all the way UP).
        """
        # DONE: Do this as STEP 2 of implementing this class.

        self.raise_arm_and_close_claw()
        self.motor.reset_degrees_spun()
        self.motor.start_spinning(-100)
        while True:
            if abs(self.motor.get_degrees_spun()) >= 14.2 * 360:
                self.motor.stop_spinning()
                break
        self.motor.reset_degrees_spun()

    def raise_arm_and_close_claw(self):
        """
        Raise the arm (and hence close the claw), by making this ArmAndClaw
        object's motor start spinning at a reasonable speed (e.g. 100).
        Positive speeds make the arm go UP; negative speeds make it go DOWN.
        Stop when the touch sensor is pressed.
        """
        # DONE: Do this as STEP 1 of implementing this class.

        self.motor.start_spinning(100)
        while True:
            if self.touch_sensor.is_pressed() is True:
                self.motor.stop_spinning()
                break

    def move_arm_to_position(self, position):
        """
        Spin the arm's motor until it reaches the given position.
        Move at a reasonable speed.
        """
        # TODO: Do this as STEP 3 of implementing this class.

        self.calibrate()
        self.motor.start_spinning(100)
        while True:
            if abs(self.motor.get_degrees_spun()) >= position:
                self.motor.stop_spinning()
                break