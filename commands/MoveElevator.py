from wpilib.command import Command
import wpilib
from subsystems.Elevator import Elevator

__all__ = ['MoveElevator']

class MoveElevator(Command):
    def __init__(self, targetPosition):
        super().__init__('MoveElevator')
        self._elevator = self.getRobot().elevator
        self.requires(self._elevator)
        self._logger = self.getRobot().logger
        self._targetPosition = targetPosition

    def initialize(self):
        self._elevator.stop()
        self._currentPosition = self._elevator.currentPosition()
        if self._currentPosition < self._targetPosition.value:
            self._speed = 0.5
        else:
            self._speed = - 0.5

    def execute(self):
        self._elevator.move(self._speed)
        
    def isFinished(self):
        if self._targetPosition.value == self._elevator.currentPosition():
            return True
        else:
            return False
     
    def end(self):
        self._elevator.stop()
