from wpilib.command.commandgroup import CommandGroup
from commands import  TurnToHeading, DriveToDistance


__all__ = ['AutoProgram']

class AutoProgram(CommandGroup):
    def __init__(self, heading, speed, distance):
        super().__init__('AutoProgram')
        self.addSequential(TurnToHeading.TurnToHeading(heading))
        self.addSequential(DriveToDistance.DriveToDistance(speed, distance))

