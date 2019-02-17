from wpilib.command.commandgroup import CommandGroup
from commands.MoveArm import MoveArmToPosition
from commands.MoveElevator import MoveElevatorToPosition
from subsystems.Elevator import ElevatorPosition
from subsystems.Arm import ArmPosition
from wpilib import Timer 


__all__ = ['DeployArm']

class DeployArm(CommandGroup):
    def __init__(self):
        super().__init__('DeployArm')
        self._timer = Timer()
        self.addSequential(MoveArmToPosition(ArmPosition.INITIAL_DEPLOY))
        self._timer.delay(2)
        self.addSequential(MoveElevatorToPosition(ElevatorPosition.INITIAL_DEPLOY))

        
