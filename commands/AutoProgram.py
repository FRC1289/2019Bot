from wpilib.command.commandgroup import CommandGroup
from commands import TurnToHeading
from commands import DriveToDistance

class AutoProgram(CommandGroup):
    def __init__(self, heading, speed, distance):
        super().__init__('AutoProgram')
        self.addSequential(TurnToHeading.TurnToHeading(heading))
        self.addSequential(DriveToDistance.DriveToDistance(speed, distance))

