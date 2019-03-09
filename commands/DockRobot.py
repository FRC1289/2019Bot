from wpilib.command.commandgroup import CommandGroup
from commands.FollowCamera import FollowCamera
from commands.EncoderDrive import EncoderDrive
import robotmap

__all__ = ['DockRobot']

class DockRobot(CommandGroup):
    def __init__(self):
        super().__init__('DockRobot')
        self.addSequential(FollowCamera(robotmap.approachSpeed))
       # self.addSequential(EncoderDrive(robotmap.approachSpeed, robotmap.dockingDistance))
