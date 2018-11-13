"""
Mini-application:  Buttons on a Tkinter GUI tell the robot to:
  - Go forward at the speed given in an entry box.

This module runs on your LAPTOP.
It uses MQTT to SEND information to a program running on the ROBOT.

Authors:  David Mutchler, his colleagues, and Michael Kuznicki.
"""
# ------------------------------------------------------------------------------
# DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.  Then delete this TODO.
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
# TODO: 3. One team member: change the following in mqtt_remote_method_calls.py:
#                LEGO_NUMBER = 99
# TODO:    to use YOUR robot's number instead of 99.
# TODO:    Commit and push the change, then other team members Update Project.
# TODO:    Then delete this TODO.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# TODO: 4. Run this module.
# TODO:    Study its code until you understand how the GUI is set up.
# TODO:    Then delete this TODO.
# ------------------------------------------------------------------------------

import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def main():
    """ Constructs and runs a GUI for this program. """
    root = tkinter.Tk()

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    setup_gui(root, mqtt_client)

    root.mainloop()
    # --------------------------------------------------------------------------
    # DONE: 5. Add code above that constructs a   com.MqttClient   that will
    # DONE:    be used to send commands to the robot.  Connect it to this pc.
    # DONE:    Test.  When OK, delete this TO DO.
    # --------------------------------------------------------------------------


def setup_gui(root_window, mqtt_client):
    """ Constructs and sets up widgets on the given window. """
    frame = ttk.Frame(root_window, padding=10)
    frame.grid()

    speed_entry_box = ttk.Entry(frame)
    go_forward_button = ttk.Button(frame, text="Go forward")

    speed_entry_box.grid()
    go_forward_button.grid()

    go_forward_button['command'] = \
        lambda: handle_go_forward(speed_entry_box, mqtt_client)


def handle_go_forward(entry_box, mqtt_client):
    """
    Tells the robot to go forward at the speed specified in the given entry box.
    """
    speed_string = entry_box.get()
    print("Sending the go_forward message with speed", speed_string)
    mqtt_client.send_message('go_forward', [speed_string])
    # --------------------------------------------------------------------------
    # DONE: 6. This function needs the entry box in which the user enters
    # DONE:    the speed at which the robot should move.  Make the 2 changes
    # DONE:    necessary for the entry_box constructed in  setup_gui
    # DONE:    to make its way to this function.  When done, delete this TO DO.
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # TODO: 7. For this function to tell the robot what to do, it needs
    # TODO:    the MQTT client constructed in main.  Make the 4 changes
    # TODO:    necessary for that object to make its way to this function.
    # TODO:    When done, delete this TODO.
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # TODO: 8. Add the single line of code needed to get the string that is
    # TODO:    currently in the entry box.
    # TODO:
    # TODO:    Then add the single line of code needed to "call" a method on the
    # TODO:    LISTENER that runs on the ROBOT, where that LISTENER is the
    # TODO:    "delegate" object that is constructed when the ROBOT's code
    # TODO:    runs on the ROBOT.  Send to the delegate the speed to use
    # TODO:    plus a method name that you will implement in the DELEGATE's
    # TODO:    class in the module that runs on the ROBOT.
    # TODO:
    # TODO:    Test by using a PRINT statement.  When done, delete this TODO.
    # --------------------------------------------------------------------------


# main()

def run_game():

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    start_screen()
    # speed_setting(mqtt_client)
    driving_instructions(mqtt_client)


def start_screen():
    root = tkinter.Tk()
    frame = ttk.Frame(root, padding=10)
    frame.grid()

    title = ttk.Label(frame, text='Welcome to Crash Landing!')
    title.grid()

    title_image = tkinter.PhotoImage(file='galaxy.gif')

    pic = ttk.Label(frame, image=title_image)
    pic.grid()

    intro1 = ttk.Label(frame, text='You have crash landed on a strange planet.')
    intro1.grid()
    intro2 = ttk.Label(frame, text='Your ship has broken into three pieces, your leg is broken, and the only thing you '
                                   'can control is your rover.')
    intro2.grid()
    intro3 = ttk.Label(frame, text='Your mission is to reassemble your ship and travel to it using nothing but your '
                                   'rover.')
    intro3.grid()

    start_button = ttk.Button(frame, text='Start!')
    start_button.grid()

    start_button['command'] = lambda: close_window(root)

    root.mainloop()

'''
def speed_setting(mqtt_client):
    root = tkinter.Tk()

    frame = ttk.Frame(root, padding=10)
    frame.grid()

    speed_box = ttk.Entry(frame)
    speed_box.grid()

    set_speed_button = ttk.Button(frame, text='Set Speed')
    set_speed_button.grid()

    set_speed_button['command'] = lambda: set_speed(root, speed_box, mqtt_client)

    root.mainloop()


def set_speed(root, speed_box, mqtt_client):
    speed = speed_box.get()
    mqtt_client.send_message('set_speed', [speed])

    close_window(root)
'''


def driving_instructions(mqtt_client):
    root = tkinter.Tk()
    root.title('Instructions')

    frame = ttk.Frame(root, padding=10)
    frame.grid()

    label_1 = ttk.Label(root, text='This is how you control your rover:')
    label_1.grid()

    label_2 = ttk.Label(root, text='')
    label_2.grid()

    label_3 = ttk.Label(root, text='Press the UP arrow key to move FORWARD.')
    label_3.grid()

    label_4 = ttk.Label(root, text='Press the DOWN arrow key to move BACKWARD.')
    label_4.grid()

    label_5 = ttk.Label(root, text='Press the LEFT arrow key to turn LEFT.')
    label_5.grid()

    label_6 = ttk.Label(root, text='Press the RIGHT arrow key to turn RIGHT.')
    label_6.grid()

    label_7 = ttk.Label(root, text='Press the SPACEBAR to STOP')
    label_7.grid()

    label_8 = ttk.Label(root, text='')
    label_8.grid()

    start_button = ttk.Button(root, text='Begin!')
    start_button.grid()

    label_9 = ttk.Label(root, text='Press this button to gain control of your rover.')
    label_9.grid()

    start_button.bind('<Up>', lambda event: move_forward(mqtt_client))
    start_button.bind('<Down>', lambda event: move_backward(mqtt_client))
    start_button.bind('<Left>', lambda event: turn_left(mqtt_client))
    start_button.bind('<Right>', lambda event: turn_right(mqtt_client))
    start_button.bind('<space>', lambda event: stop(mqtt_client))

    label_10 = ttk.Label(root, text='')
    label_10.grid()

    label_11 = ttk.Label(root, text='Hurry! You are running out of air!')
    label_11.grid()

    root.mainloop()


def move_forward(mqtt_client):
    mqtt_client.send_message('move_forward')


def move_backward(mqtt_client):
    mqtt_client.send_message('move_backward')


def turn_left(mqtt_client):
    mqtt_client.send_message('turn_left')


def turn_right(mqtt_client):
    mqtt_client.send_message('turn_right')


def stop(mqtt_client):
    mqtt_client.send_message('stop')


def close_window(root):
    root.destroy()


run_game()
