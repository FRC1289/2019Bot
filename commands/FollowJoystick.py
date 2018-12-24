from wpilib.command import Command

class FollowJoystick(Command):
    '''
    This command will read the joystick's y axis and use that value to control
    the speed of the SingleMotor subsystem.
    '''

    def __init__(self):
        super().__init__('Follow Joystick')

        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        

    def initialize(self):
        self.drivetrain.freeDrive(0,0)

    def execute(self):
        fwdbk = self.getRobot().joystick.getY()
        rot = self.getRobot().joystick.getX()
        self.drivetrain.freeDrive(fwdbk, rot)
    

    def isFinished(self):
        if self.getRobot().joystick.getRawButton(1):
            return True
        else:
            return False

    def end(self):
        self.drivetrain.freeDrive(0,0)
