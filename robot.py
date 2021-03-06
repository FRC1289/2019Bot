#!/usr/bin/env python3

import wpilib
from wpilib.command import Command, Scheduler
from wpilib.command.subsystem import Subsystem
from commandbased import CommandBasedRobot
from networktables import NetworkTables

from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton

from commands.DeployArm import DeployArm
from commands.Ingest import Ingest
from commands.Expel import Expel
from commands.DockRobot import DockRobot
from commands.AutoProgram import *
from commands.MoveArm import *
from commands.MoveElevator import *
from commands.CancelSubsystem import *

from subsystems.DriveTrain import DriveTrain
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
        
        #self.motor = SingleMotor.SingleMotor(2, self.logger)
        self.drivetrain = DriveTrain(self.logger)
        self.elevator = Elevator(self.logger)
        self.arm = Arm(self.logger)
        self.scooper = Scooper(self.logger)

        self.startCommand = DeployArm()

        self.joystick = Joystick(robotmap.STK_port)
        self.halfPowerModeButton = JoystickButton(self.joystick, robotmap.STK_halfPowerMode)
      #  self.automaticMode = JoystickButton(self.joystick, robotmap.STK_automode)
       # self.automaticMode.whenPressed(DockRobot())
       # self.automaticMode.whenReleased(CancelSubsystem(Cancel.DRIVETRAIN))
        
        self.buttonBoard = Joystick(robotmap.BB_port)
        self.armUpButton = JoystickButton(self.buttonBoard, robotmap.BB_ArmUp)
        self.armDownButton = JoystickButton(self.buttonBoard, robotmap.BB_ArmDown)
        self.stowArmButton = JoystickButton(self.buttonBoard, robotmap.BB_StowArm)
        self.elevatorUpButton = JoystickButton(self.buttonBoard, robotmap.BB_ElevatorUp)
        self.elevatorDownButton = JoystickButton(self.buttonBoard, robotmap.BB_ElevatorDown)
        self.ingestButton = JoystickButton(self.buttonBoard, robotmap.BB_ingest)
        self.expelButton = JoystickButton(self.buttonBoard, robotmap.BB_expel)
        self.deployArmButton = JoystickButton(self.buttonBoard, robotmap.BB_DeployArm)
        self.midHatchButton = JoystickButton(self.buttonBoard, robotmap.BB_MidHatch)
        self.lowCargoButton = JoystickButton(self.buttonBoard, robotmap.BB_LowCargo)
        self.midCargoButton = JoystickButton(self.buttonBoard, robotmap.BB_MidCargo)

        self.armUpButton.whenPressed(MoveArmUp())
        self.armDownButton.whenPressed(MoveArmDown())
        self.armUpButton.whenReleased(CancelSubsystem(Cancel.ARM))
        self.armDownButton.whenReleased(CancelSubsystem(Cancel.ARM))
        self.stowArmButton.whenPressed(StowArm())
        #self.deployArmButton.whenPressed(DeployArm())
        
        self.elevatorUpButton.whenPressed(MoveElevatorUp())
        self.elevatorDownButton.whenPressed(MoveElevatorDown())
        self.elevatorUpButton.whenReleased(CancelSubsystem(Cancel.ELEVATOR))
        self.elevatorDownButton.whenReleased(CancelSubsystem(Cancel.ELEVATOR))

        self.ingestButton.whenPressed(Ingest())
        self.expelButton.whenPressed(Expel())

        # self.lowHatchButton.whenPressed(PositionLowHatch())
        # self.midHatchButton.whenPressed(PositionMidHatch())
        # self.lowCargoButton.whenPressed(PositionLowCargo())
        # self.midCargoButton.whenPressed(PositionMidCargo())

        self._smartDashboard = NetworkTables.getTable('SmartDashboard')
        self._smartDashboard.putString("ArmLimit", "InGame")
 

    # def autonomousInit(self):
    #      self.startCommand.start()
        
    # def autonomousPeriodic(self):
    #    Scheduler.getInstance().run()


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
