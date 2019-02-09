#!/usr/bin/env python3

import wpilib
from wpilib.command import Command, Scheduler
from wpilib.command.subsystem import Subsystem
from commandbased import CommandBasedRobot

from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton

from commands.DeployArm import DeployArm
from commands.StowArm import StowArm
from commands.Ingest import Ingest
from commands.Expel import Expel
from commands.AutoProgram import AutoProgram

from subsystems.DriveTrain import DriveTrain
from subsystems.ParameterManager import ParameterManager
from subsystems.Elevator import Elevator
from subsystems.Arm import Arm
from subsystems.Scooper import Scooper
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
        
        self._parameters = ParameterManager(self.logger)
        #self.motor = SingleMotor.SingleMotor(2, self.logger)
        self.drivetrain = DriveTrain(self.logger, self._parameters)
        self.elevator = Elevator(self.logger, self._parameters)
        self.arm = Arm(self.logger, self._parameters)
        self.scooper = Scooper(self.logger, self._parameters)

        self.startCommand = DeployArm()

        self.joystick = Joystick(robotmap.STK_port)
        self.automaticMode = JoystickButton(self.joystick, robotmap.STK_automode)
        self.automaticMode.whileHeld(AutoProgram())
        
        self.buttonBoard = Joystick(robotmap.BB_port)
        #self.stowButton = JoystickButton(self.joystick, robotmap.STK_Stow)
        #self.stowButton.whenPressed(StowArm())

        #self.ingestButton = JoystickButton(self.buttonBoard, robotmap.BB_ingest)
        #self.ingestButton.whenPressed(Ingest())

        #self.expelButton = JoystickButton(self.buttonBoard, robotmap.BB_expel)
        #self.expelButton.whileHeld(Expel())


    def autonomousInit(self):
         self.startCommand.start()
        
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
