"""
Mini-application:  Buttons on a Tkinter GUI tell the robot to:
  - Go forward at the speed given in an entry box.

This module runs on your LAPTOP.
It uses MQTT to SEND information to a program running on the ROBOT.

Authors:  David Mutchler, his colleagues, and Owen Land.
"""
# ------------------------------------------------------------------------------
LEGO_NUMBER = 18

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
    go_forward_button = ttk.Button(frame, text="Forward", padding=10)
    go_backward_button = ttk.Button(frame, text="Backward", padding=10)
    go_left_button = ttk.Button(frame, text="Turn Left", padding=10)
    go_right_button = ttk.Button(frame, text="Turn Right", padding=10)
    stop_button = ttk.Button(frame, text="Stop")

    speed_entry_box.grid(row=1, column=1, columnspan=2)
    degrees_entry_box.grid(row=1, column=3, columnspan=2)
    go_forward_button.grid(row=2, column=1, pady=10)
    go_backward_button.grid(row=2, column=2, pady=10)
    go_left_button.grid(row=2, column=3, pady=10)
    go_right_button.grid(row=2, column=4, pady=10)
    stop_button.grid(row=4, column=2, columnspan=2, pady=10)

    go_forward_button['command'] = \
        lambda: handle_go_forward(speed_entry_box, mqtt_client)
    go_backward_button['command'] = \
        lambda: handle_go_backward(speed_entry_box, mqtt_client)
    go_left_button['command'] = \
        lambda: handle_go_left(degrees_entry_box, mqtt_client)
    go_right_button['command'] = \
        lambda: handle_go_right(degrees_entry_box, mqtt_client)
    stop_button['command'] = \
        lambda: handle_stop(mqtt_client)


def handle_go_forward(entry_box, mqtt_client):
    """
    Tells the robot to go forward at the speed specified in the given entry box.
    """
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
    speed_string = entry_box.get()
    print("Sending the go_backward message with speed", speed_string)
    mqtt_client.send_message('go_backward', [speed_string])


def handle_go_left(entry_box, mqtt_client):
    """
    Tells the robot to turn left
    """
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
    degrees_string = entry_box.get()
    print("Sending the go_right", degrees_string)
    mqtt_client.send_message('go_right', [degrees_string])


def handle_stop(mqtt_client):
    """
    Tells the robot to stop moving
    """
    print("Sending the stop message")
    mqtt_client.send_message('stop_moving')


main()
