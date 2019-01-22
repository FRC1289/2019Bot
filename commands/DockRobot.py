from wpilib.command import Command
import wpilib

__all__ = ['DockRobot']

class DockRobot(Command):
    def __init__(self):
        super().__init__('DockCommand', 10)
        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        self.logger = self.getRobot().logger

    def initialize(self):
        self.logger.info('init %s' % id(self))

    def execute(self):
        self.logger.info('DR exec')
        self.drivetrain.freeDrive(0.5, 0)

    def isFinished(self):
        return False
    #     if self.isTimedOut:
    #         return True
    #     else:
    #         return False
     
    def end(self):
        self.logger.info('ended')
        
    def interrupted(self):
        self.logger.info('interrupted')

    def cancel(self):
        self.logger.info('cancel')
