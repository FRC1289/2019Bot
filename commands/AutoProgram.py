from wpilib.command.commandgroup import CommandGroup
from commands import DockRobot


__all__ = ['AutoProgram']

class AutoProgram(CommandGroup):
    def __init__(self):
        super().__init__('AutoProgram')
        #self.setInterruptible(False)
        self.addSequential(DockRobot.DockRobot())
        
