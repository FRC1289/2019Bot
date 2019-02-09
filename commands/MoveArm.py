from wpilib.command import Command
import wpilib
from subsystems.Arm import Arm

__all__ = ['MoveArm']

class MoveArm(Command):
    def __init__(self, targetPosition):
        super().__init__('MoveArm')
        self._arm = self.getRobot().arm
        self.requires(self._arm)
        self._logger = self.getRobot().logger
        self._parameters = self.getRobot()._parameters
        self._targetPosition = targetPosition
        self._speed = self._parameters.getValue('armSpeed')

    def initialize(self):
        self._arm.stop()
        self._currentPosition = self._arm.currentPosition()
        if self._currentPosition < self._targetPosition.value:
            self._speed = 0.5
        else:
            self._speed = - 0.5

    def execute(self):
        self._arm.move(self._speed)
        
    def isFinished(self):
        if self._targetPosition.value == self._arm.currentPosition():
            return True
        else:
            return False
     
    def end(self):
        self._arm.stop()
