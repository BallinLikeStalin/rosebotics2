"""
Mini-application:  Buttons on a Tkinter GUI tell the robot to:
  - Go forward at the speed given in an entry box.

This module runs on your LAPTOP.
It uses MQTT to SEND information to a program running on the ROBOT.

Authors:  David Mutchler, his colleagues, and Owen Land.
"""
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# TODO: 2. With your instructor, discuss the "big picture" of laptop-robot
# TODO:    communication:
# TODO:      - One program runs on your LAPTOP.  It displays a GUI.  When the
# TODO:        user presses a button intended to make something happen on the
# TODO:        ROBOT, the LAPTOP program sends a message to its MQTT client
# TODO:        indicating what it wants the ROBOT to do, and the MQTT client
# TODO:        SENDS that message TO a program running on the ROBOT.
# TODO:
# TODO:      - Another program runs on the ROBOT. It stays in a loop, responding
# TODO:        to events on the ROBOT (like pressing buttons on the IR Beacon).
# TODO:        It also, in the background, listens for messages TO the ROBOT
# TODO:        FROM the program running on the LAPTOP.  When it hears such a
# TODO:        message, it calls the method in the DELAGATE object's class
# TODO:        that the message indicates, sending arguments per the message.
# TODO:
# TODO:  Once you understand the "big picture", delete this TODO (if you wish).
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
LEGO_NUMBER = 18

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
#.
# ------------------------------------------------------------------------------

import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def main():
    """ Constructs and runs a GUI for this program. """
    root = tkinter.Tk()


    com1 = com.MqttClient()
    com1.connect_to_ev3()

    setup_gui(root, com1)

    root.mainloop()
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------


def setup_gui(root_window, mqtt_client):
    """ Constructs and sets up widgets on the given window. """
    frame = ttk.Frame(root_window, padding=10)
    frame.grid()

    speed_entry_box = ttk.Entry(frame)
    degrees_entry_box = ttk.Entry(frame)
    go_forward_button = ttk.Button(frame, text="Forward")
    go_backward_button = ttk.Button(frame, text="Backward")
    go_left_button = ttk.Button(frame, text="Turn Left")
    go_right_button = ttk.Button(frame, text="Turn Right")

    speed_entry_box.grid()
    degrees_entry_box.grid()
    go_forward_button.grid()
    go_backward_button.grid()
    go_left_button.grid()
    go_right_button.grid()

    go_forward_button['command'] = \
        lambda: handle_go_forward(speed_entry_box, mqtt_client)
    go_backward_button['command'] = \
        lambda: handle_go_backward(speed_entry_box, mqtt_client)
    go_left_button['command'] = \
        lambda: handle_go_left(degrees_entry_box, mqtt_client)
    go_right_button['command'] = \
        lambda: handle_go_right(degrees_entry_box, mqtt_client)


def handle_go_forward(entry_box, mqtt_client):
    """
    Tells the robot to go forward at the speed specified in the given entry box.
    """
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    speed_string = entry_box.get()
    print("Sending the go_forward message with speed", speed_string)
    mqtt_client.send_message('go_forward', [speed_string])


def handle_go_backward(entry_box, mqtt_client):
    """
    Tells the robot to go backward at the speed specified in the given entry box.
    """
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    speed_string = entry_box.get()
    print("Sending the go_backward message with speed", speed_string)
    mqtt_client.send_message('go_backward', [speed_string])


def handle_go_left(entry_box, mqtt_client):
    """
    Tells the robot to turn left
    """
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    degrees_string = entry_box.get()
    print("Sending the turn left", degrees_string)
    mqtt_client.send_message('go_left', [degrees_string])


def handle_go_right(entry_box, mqtt_client):
    """
    Tells the robot to go right
    """
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    degrees_string = entry_box.get()
    print("Sending the go_right", degrees_string)
    mqtt_client.send_message('go_right', [degrees_string])
main()
