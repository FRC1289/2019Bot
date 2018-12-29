#!/usr/bin/env python3

import wpilib
from wpilib.command import Command, Scheduler
from wpilib.command.subsystem import Subsystem
from commandbased import CommandBasedRobot

import oi
from subsystems import *
from commands import *

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
        
        self.motor = SingleMotor.SingleMotor(3, self.logger)
        self.drivetrain = DriveTrain.DriveTrain(self.logger)

        self.autonomousProgram = AutoProgram.AutoProgram(10, 0.4, 125)
        self.teleopProgram = FollowJoystick.FollowJoystick()
        
        '''
        Since OI instantiates commands and commands need access to subsystems,
        OI must be initialized after subsystems.
        '''
        self.joystick = oi.getJoystick()

    def autonomousInit(self):
        self.autonomousProgram.start()
        
    #def autonomousPeriodic(self):
        #Scheduler.getInstance().run()
        

    def teleopInit(self):
        if self.autonomousProgram is not None:
            self.autonomousProgram.cancel()
        self.teleopProgram.start()
        
    # def teleopPeriodic(self):
    #     Scheduler.getInstance().run()
    #     if self.teleopProgram.isFinished():
    #         #self.logger.info('finished')
    #         self.teleopProgram = CW_CCW(self.logger)
    #         self.teleopProgram.start()

if __name__ == '__main__':
    wpilib.run(PyBot)
