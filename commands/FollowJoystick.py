from wpilib.command import Command

__all__ = ['FollowJoystick']

class FollowJoystick(Command):
    '''
    This command will read the joystick's y axis and use that value to control
    the speed of the SingleMotor subsystem.
    '''

    def __init__(self):
        super().__init__('Follow Joystick')

        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        self.logger = self.getRobot().logger
        self.setInterruptible(True)
        

    def initialize(self):
        self.drivetrain.reset()

    def execute(self):
        fwdbk = self.getRobot().joystick.getY()
        rot = self.getRobot().joystick.getX()
        #(a1, a2) = self.drivetrain.getEncoderCount()
        #self.count = self.count + a1 + a2
        self.drivetrain.freeDrive(fwdbk, rot)
    

    def isFinished(self):
        return False
    #     if self.getRobot().joystick.getRawButton(1):
    #         return True
    #     else:
    #         return False

    def end(self):
        self.drivetrain.freeDrive(0,0)

    def interrupted(self):
        self.logger.info('FS interrupted')
        self.end()
