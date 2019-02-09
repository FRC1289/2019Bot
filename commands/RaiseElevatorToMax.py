from wpilib.command import Command
import wpilib
from subsystems.Elevator import Elevator, ElevatorLimit

__all__ = ['RaiseElevatorToMax']

class RaiseElevatorToMax(Command):
    def __init__(self):
        super().__init__('RaiseElevatorToMax')
        self._elevator = self.getRobot().elevator
        self.requires(self._elevator)
        self._logger = self.getRobot().logger

    def initialize(self):
        self._elevator.stop()

    def execute(self):
        self._elevator.move(0.5)
        
    def isFinished(self):
        if self._elevator.atLimit(ElevatorLimit.UPPER):
            return True
        else:
            return False
     
    def end(self):
        self._elevator.stop()
