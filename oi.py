from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton
import robotmap
from commands.followjoystick import FollowJoystick


def getJoystick():
    '''
    Assign commands to button actions, and publish your joysticks so you
    can read values from them later.
    '''

    joystick = Joystick(robotmap.STK_port)

    # trigger = JoystickButton(joystick, Joystick.ButtonType.kTrigger)
    # trigger.whenPressed(Crash())

    return joystick
