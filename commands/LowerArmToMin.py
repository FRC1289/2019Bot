from wpilib.command import Command
import wpilib
from subsystems.Arm import Arm, ArmLimit

__all__ = ['LowerArmToMin']

class LowerArmToMin(Command):
    def __init__(self):
        super().__init__('LowerArmToMin')
        self._arm = self.getRobot().arm
        self.requires(self._arm)
        self._logger = self.getRobot().logger

    def initialize(self):
        self._arm.stop()

    def execute(self):
        self._arm.move(0.5)
        
    def isFinished(self):
        if self._arm.atLimit(ArmLimit.LOWER):
            return True
        else:
            return False
     
    def end(self):
        self._arm.stop()
