import wpilib
from wpilib.command import Command
from enum import Enum, auto

class Cancel(Enum):
        ARM = auto()
        ELEVATOR = auto()
        DRIVETRAIN = auto()
        
class CancelSubsystem(Command):
    def __init__(self, subsys):
        super().__init__('CancelSubsystem')
        if subsys is Cancel.ARM:
            self._subsys = self.getRobot().arm
        elif subsys is Cancel.ELEVATOR:
            self._subsys = self.getRobot().elevator
        else:
            self._subsys = self.getRobot().drivetrain

        self.requires(self._subsys)

    def initialize(self):
        self._subsys.stop()


