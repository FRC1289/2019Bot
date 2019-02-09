from wpilib.command.commandgroup import CommandGroup
from commands import FollowCamera


__all__ = ['AutoProgram']

class AutoProgram(CommandGroup):
    def __init__(self):
        super().__init__('AutoProgram')
        #self.setInterruptible(False)
        self.addSequential(FollowCamera.FollowCamera(0.4))
        
        
