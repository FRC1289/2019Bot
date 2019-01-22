#!/usr/bin/env python3

import wpilib
from wpilib.command import Command, Scheduler
from wpilib.command.subsystem import Subsystem
from commandbased import CommandBasedRobot

from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton

from subsystems import *
from commands import *
from commands import DockRobot
import robotmap

class PyBot(CommandBasedRobot):
    '''
    The CommandBasedRobot base class implements almost everything you need for
    a working robot program. All you need to do is set up the subsystems and
    commands. You do not need to override the "periodic" functions, as they
    will automatically call the scheduler. You may override the "init" functions
    if you want to do anything special when the mode changes.
    '''

    def robotInit(self):
        '''
        Subsystem, Command, OperatorInterface Instantiation
        IN THAT ORDER
        '''

        Command.getRobot = lambda x=0: self
        
        self.motor = SingleMotor.SingleMotor(2, self.logger)
        self.drivetrain = DriveTrain.DriveTrain(self.logger)

        self.mainCommand = FollowJoystick.FollowJoystick()

        self.joystick = Joystick(robotmap.STK_port)
        self.trigger = JoystickButton(self.joystick, Joystick.ButtonType.kTrigger)
        self.trigger.whileHeld(AutoProgram.AutoProgram())


    # def autonomousInit(self):
    #     self.mainCommand.start()
        
    #def autonomousPeriodic(self):
    #    Scheduler.getInstance().run()
    #     if self.mainCommand.isCompleted():
    #         self.logger.info('main is done')
    #         self.mainCommand = FollowJoystick.FollowJoystick()
    #         self.mainCommand.start()
        

    # def teleopInit(self):
    #     self.mainCommand.start()
        
    # def teleopPeriodic(self):
    #     Scheduler.getInstance().run()
    #     if self.teleopProgram.isFinished():
    #         #self.logger.info('finished')
    #         self.teleopProgram = CW_CCW(self.logger)
    #         self.teleopProgram.start()

if __name__ == '__main__':
    wpilib.run(PyBot)
