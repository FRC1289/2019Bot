from wpilib.command.commandgroup import CommandGroup
from subsystems.Arm import ArmPosition
from subsystems.Elevator import ElevatorPosition
from commands.MoveArm import *
from commands.MoveElevator import *

__all__ = ['PositionLowHatch',
           'PositionMidHatch',
           'PositionLowCargo',
           'PositionMidCargo',
           'StowArm',
           'DeployArm']
           
class StowArm(CommandGroup):
    def __init__(self):
        super().__init__('StowArm')
        self.addSequential(MoveElevatorUp())
        self.addSequential(MoveArmDownToBottom())

class DeployArm(CommandGroup):
    def __init__(self):
        super().__init__('DeployArm')
        self.addSequential(MoveArmToInitialPosition())
        self.addSequential(MoveElevatorToInitialPosition())
        
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
        
        
