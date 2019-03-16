from wpilib.command import Command
import wpilib
from wpilib import Timer 
from subsystems.Elevator import *
from networktables import NetworkTables
import robotmap

__all__ = ['MoveElevatorUp', 'MoveElevatorDown', 'MoveElevatorToPosition', 'CancelElevatorMotion', 'MoveElevatorToInitialPosition']

class MoveElevatorUp(Command):
    def __init__(self):
        super().__init__('MoveElevatorUp')
        self._elevator = self.getRobot().elevator
        self.requires(self._elevator)
        self._logger = self.getRobot().logger
        self._speed = robotmap.ElevatorSpeed
        self._smartDashboard = NetworkTables.getTable('SmartDashboard')

    def initialize(self):
        self._elevator.stop()
        self._smartDashboard.putString("ElevatorPosition", str(self._elevator.currentPosition()))

    def execute(self):
        self._elevator.move(self._speed)
        self._smartDashboard.putString("ElevatorPosition", str(self._elevator.currentPosition()))
        
    def isFinished(self):
        if self._elevator.atLimit(ElevatorLimit.UPPER):
            self._logger.info('elev up at max')
            return True
        else:
            return False

    def interrupted(self):
        self.end()
     
    def end(self):
        self._logger.info('elev up done')
        self._elevator.stop()


class MoveElevatorDown(Command):
    def __init__(self):
        super().__init__('MoveElevatorDown')
        self._elevator = self.getRobot().elevator
        self.requires(self._elevator)
        self._logger = self.getRobot().logger
        self._speed = - robotmap.ElevatorSpeed  #Negated
        self._smartDashboard = NetworkTables.getTable('SmartDashboard')

    def initialize(self):
        self._elevator.stop()
        self._smartDashboard.putString("ElevatorPosition", str(self._elevator.currentPosition()))

    def execute(self):
        self._elevator.move(self._speed)
        self._smartDashboard.putString("ElevatorPosition", str(self._elevator.currentPosition()))
        
    def isFinished(self):
        if self._elevator.atLimit(ElevatorLimit.LOWER):
            return True
        else:
            return False

    def interrupted(self):
        self.end()
     
    def end(self):
        self._elevator.stop()

class MoveElevatorToPosition(Command):
    def __init__(self, position):
        super().__init__('MoveElevatorDown')
        self._elevator = self.getRobot().elevator
        self.requires(self._elevator)
        self._logger = self.getRobot().logger
        self._speed = robotmap.ElevatorSpeed
        self._smartDashboard = NetworkTables.getTable('SmartDashboard')
        self._targetPosition = position
        self._timer = Timer()

    def initialize(self):
        self._elevator.stop()
        self._timer.reset()
        self._timer.start()
        self._smartDashboard.putString("ElevatorPosition", str(self._elevator.currentPosition()))
        if self._elevator.currentPosition() > self._targetPosition.value:
            self._speed = - self._speed
        if self._targetPosition == ElevatorPosition.INITIAL_DEPLOY:
            while not self._timer.hasPeriodPassed(robotmap.Deploy_Delay):
                continue
            

    def execute(self):
        self._elevator.move(self._speed)
        self._smartDashboard.putString("ElevatorPosition", str(self._elevator.currentPosition()))
        
    def isFinished(self):
        if self._elevator.currentPosition() == self._targetPosition.value:
            return True
        elif self._elevator.atLimit(ElevatorLimit.LOWER) or self._elevator.atLimit(ElevatorLimit.UPPER):
            return True
        else:
            return False

    def interrupted(self):
        self.end()
     
    def end(self):
        self._elevator.stop()


class CancelElevatorMotion(Command):
    def __init__(self):
        super().__init__('CancelElevatorMotion')
        self._elevator = self.getRobot().elevator
        self.requires(self._elevator)
        self._logger = self.getRobot().logger

    def initialize(self):
        self._logger.info("Cancel elevator motion")
        self._elevator.stop()

class MoveElevatorToInitialPosition(Command):
    def __init__(self):
        super().__init__('MoveElevatorToInitialPosition')
        self._elevator = self.getRobot().elevator
        self.requires(self._elevator)
        self._logger = self.getRobot().logger
        self._speed = - robotmap.ElevatorSpeed  #Negated
        self._smartDashboard = NetworkTables.getTable('SmartDashboard')
        self._timer = Timer()

    def initialize(self):
        self._elevator.stop()
        self._smartDashboard.putString("ElevatorPosition", str(self._elevator.currentPosition()))
        self._timer.reset()
        self._timer.start()

    def execute(self):
        self._elevator.move(self._speed)
        self._smartDashboard.putString("ElevatorPosition", str(self._elevator.currentPosition()))
        
    def isFinished(self):
        if self._timer.get() > 1.0   :
            return True
        else:
            return False

    def interrupted(self):
        self.end()
     
    def end(self):
        self._elevator.stop()
