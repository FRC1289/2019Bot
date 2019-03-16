from wpilib.command import Command
from wpilib.driverstation import DriverStation
import wpilib
from wpilib import Timer
from subsystems.Arm import Arm, ArmLimit
from networktables import NetworkTables
import robotmap


__all__ = ['MoveArmUp', 'MoveArmDown', 'CancelArmMotion', 'MoveArmToPosition', 'MoveArmDownToBottom', 'MoveArmToInitialPosition']

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
        self._smartDashboard.putString("ArmPosition", str(self._arm.currentPosition()))

    def execute(self):
        #self._logger.info("UP")
        self._arm.move(self._speed)
        self._smartDashboard.putString("ArmPosition", str(self._arm.currentPosition()))
        
    def isFinished(self):
        if self._arm.atLimit(ArmLimit.UPPER):
            return True
        else:
            return False

    def interrupted(self):
        #self._logger.info("UP interrupted")
        self.end()
     
    def end(self):
        #self._logger.info("UP ended")
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
        self._smartDashboard.putString("ArmPosition", str(self._arm.currentPosition()))

    def execute(self):
        #self._logger.info("DOWN")
        self._arm.move(self._speed)
        self._smartDashboard.putString("ArmPosition", str(self._arm.currentPosition()))
        
    def isFinished(self):
        if self._arm.atLimit(ArmLimit.IN_GAME_LOWER):
            return True
        else:
            return False

    def interrupted(self):
        #self._logger.info("DOWN interrupted")
        self.end()
     
    def end(self):
        #self._logger.info("DOWN ended")
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
        self._smartDashboard.putString("ArmPosition", str(self._arm.currentPosition()))
        if self._arm.currentPosition() > self._targetPosition.value:
            self._speed = - self._speed

    def execute(self):
        self._arm.move(self._speed)
        self._smartDashboard.putString("ArmPosition", str(self._arm.currentPosition()))
        
    def isFinished(self):
        rtn = False
        if self._arm.atLimit(ArmLimit.UPPER):
            rtn = True
        elif self._arm.currentPosition == self._targetPosition.value:
            rtn = True
        elif self._speed < 0 and self._arm.atLimit(ArmLimit.IN_GAME_LOWER):
            rtn = True
        else:
            return rtn
    
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

class MoveArmDownToBottom(Command):
    def __init__(self):
        super().__init__('MoveArmDownToBottom')
        self._arm = self.getRobot().arm
        self.requires(self._arm)
        self._logger = self.getRobot().logger
        self._smartDashboard = NetworkTables.getTable('SmartDashboard')
        self._speed = robotmap.ArmSpeed

    def initialize(self):
        #self._logger('arm to bottom init')
        self._arm.stop()
        self._smartDashboard.putString("ArmPosition", str(self._arm.currentPosition()))

    def execute(self):
        #self._logger.info("arm to bottom")
        self._arm.move(self._speed)
        self._smartDashboard.putString("ArmPosition", str(self._arm.currentPosition()))
        
    def isFinished(self):
        if self._arm.atLimit(ArmLimit.LOWER):
            return True
        else:
            return False

    def interrupted(self):
        #self._logger.info("DOWN interrupted")
        self.end()
     
    def end(self):
        #self._logger.info("DOWN ended")
        self._arm.stop()

class MoveArmToInitialPosition(Command):
    def __init__(self):
        super().__init__('MoveArmToInitialPosition')
        self._arm = self.getRobot().arm
        self.requires(self._arm)
        self._logger = self.getRobot().logger
        self._smartDashboard = NetworkTables.getTable('SmartDashboard')
        self._speed = - robotmap.ArmSpeed
        self._timer = Timer()

    def initialize(self):
        self._arm.stop()
        # self._timer.reset()
       # self._timer.start()
        self._smartDashboard.putString("ArmPosition", str(self._arm.currentPosition()))

    def execute(self):
        #self._logger.info("DOWN")
        #if self._timer.get() > 1.0:
        self._arm.move(self._speed)
        self._smartDashboard.putString("ArmPosition", str(self._arm.currentPosition()))
        
    def isFinished(self):
        if self._arm.atLimit(ArmLimit.IN_GAME_LOWER):
            return True
        else:
            return False

    def interrupted(self):
        #self._logger.info("DOWN interrupted")
        self.end()
     
    def end(self):
        #self._logger.info("DOWN ended")
        self._arm.stop()
        
