from wpilib.command.commandgroup import CommandGroup
from commands import MoveArm, MoveElevator
from subsystems.Elevator import ElevatorPosition
from subsystems.Arm import ArmPosition


__all__ = ['DeployArm']

class DeployArm(CommandGroup):
    def __init__(self):
        super().__init__('DeployArm')
        self.addSequential(MoveArm.MoveArm(ArmPosition.INITIAL_DEPLOY))
        self.addSequential(MoveElevator.MoveElevator(ElevatorPosition.INITIAL_DEPLOY))

        
