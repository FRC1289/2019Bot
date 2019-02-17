from wpilib.command.commandgroup import CommandGroup
from subsystems.Arm import ArmPosition
from subsystems.Elevator import ElevatorPosition
from commands.MoveArm import MoveArmToPosition
from commands.MoveElevator import MoveElevatorToPosition

__all__ = ['PositionLowHatch',
           'PositionMidHatch',
           'PositionLowCargo',
           'PositionMidCargo']

class PositionLowHatch(CommandGroup):
    def __init__(self):
        super().__init__('PositionLowHatch')
        self.addParallel(MoveArmToPosition(ArmPosition.LOWER_HATCH))
        self.addParallel(MoveElevatorToPosition(ElevatorPosition.LOWER_HATCH))

class PositionMidHatch(CommandGroup):
    def __init__(self):
        super().__init__('PositionMidHatch')
        self.addParallel(MoveArmToPosition(ArmPosition.MID_HATCH))
        self.addParallel(MoveElevatorToPosition(ElevatorPosition.MID_HATCH))

class PositionLowCargo(CommandGroup):
    def __init__(self):
        super().__init__('PositionLowCargo')
        self.addParallel(MoveArmToPosition(ArmPosition.LOWER_CARGO))
        self.addParallel(MoveElevatorToPosition(ElevatorPosition.LOWER_CARGO))

class PositionMidCargo(CommandGroup):
    def __init__(self):
        super().__init__('PositionMidCargo')
        self.addParallel(MoveArmToPosition(ArmPosition.MID_CARGO))
        self.addParallel(MoveElevatorToPosition(ElevatorPosition.MID_CARGO))
        
        
