from wpilib.command import Command
import wpilib
from subsystems.Arm import Arm, ArmLimit
from networktables import NetworkTables
import robotmap


__all__ = ['MoveArmUp', 'MoveArmDown', 'CancelArmMotion', 'MoveArmToPosition']

class MoveArmUp(Command):
    def __init__(self):
        super().__init__('MoveArmUp')
        self._arm = self.getRobot().arm
        self.requires(self._arm)
        self._logger = self.getRobot().logger
        self._speed = robotmap.ArmSpeed
        self._smartDashboard = NetworkTables.getTable('SmartDashboard')

    def initialize(self):
        self._arm.stop()

    def execute(self):
        self._logger.info("UP")
        self._arm.move(self._speed)
        self._smartDashboard.putString("ArmPosition", str(self._arm.currentPosition()))
        
    def isFinished(self):
        if self._arm.atLimit(ArmLimit.UPPER):
            return True
        else:
            return False

    def interrupted(self):
        self._logger.info("UP interrupted")
        self.end()
     
    def end(self):
        self._logger.info("UP ended")
        self._arm.stop()

class MoveArmDown(Command):
    def __init__(self):
        super().__init__('MoveArmDown')
        self._arm = self.getRobot().arm
        self.requires(self._arm)
        self._logger = self.getRobot().logger
        self._speed = - robotmap.ArmSpeed   # Negated speed
        self._smartDashboard = NetworkTables.getTable('SmartDashboard')

    def initialize(self):
        self._arm.stop()

    def execute(self):
        self._logger.info("DOWN")
        self._arm.move(self._speed)
        self._smartDashboard.putString("ArmPosition", str(self._arm.currentPosition()))
        
    def isFinished(self):
        if self._arm.atLimit(ArmLimit.LOWER):
            return True
        else:
            return False

    def interrupted(self):
        self._logger.info("DOWN interrupted")
        self.end()
     
    def end(self):
        self._logger.info("DOWN ended")
        self._arm.stop()


class MoveArmToPosition(Command):
    def __init__(self, position):
        super().__init__('MoveArmToPosition')
        self._arm = self.getRobot().arm
        self.requires(self._arm)
        self._logger = self.getRobot().logger
        self._speed = robotmap.ArmSpeed
        self._smartDashboard = NetworkTables.getTable('SmartDashboard')
        self._targetPosition = position

    def initialize(self):
        self._arm.stop()
        if self._arm.currentPosition() > self._targetPosition.value:
            self._speed = - self._speed

    def execute(self):
        self._arm.move(self._speed)
        self._smartDashboard.putString("ArmPosition", str(self._arm.currentPosition()))
        
    def isFinished(self):
        if self._arm.currentPosition == self._targetPosition.value:
            return True
        else:
            return False

    def interrupted(self):
        self.end()
     
    def end(self):
        self._arm.stop()
        
class CancelArmMotion(Command):
    def __init__(self):
        super().__init__('CancelArmMotion')
        self._arm = self.getRobot().arm
        self.requires(self._arm)
        self._logger = self.getRobot().logger

    def initialize(self):
        self._logger.info("Cancel Arm Motion")
        self._arm.stop()
