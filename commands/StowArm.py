from wpilib.command.commandgroup import CommandGroup
from commands import RaiseElevatorToMax, LowerArmToMin


__all__ = ['StowArm']

class StowArm(CommandGroup):
    def __init__(self):
        super().__init__('StowArm')
        self.addSequential(RaiseElevatorToMax.RaiseElevatorToMax())
        self.addSequential(LowerArmToMin.LowerArmToMin())
        
