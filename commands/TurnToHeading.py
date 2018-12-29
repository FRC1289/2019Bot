import wpilib
from wpilib.command import Command
import robotmap

__all__ = ['TurnToHeading']

class TurnToHeading(Command):
    '''
    This command initializes the drivetrain to drive straight
    at a given speed towards a given heading
    '''

    def __init__(self, heading):
        super().__init__('TurnToHeading')

        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        self.speed = 0.1
        self.heading = heading
        self.rotation = 0

        kP = robotmap.gyro_kP
        kD = robotmap.gyro_kD
        kI = robotmap.gyro_kI
        self.pid = wpilib.PIDController(kP, kD, kI,
                                            lambda: self.drivetrain.getGyroAngle(),
                                            lambda r: self.setRotation(r))
        self.pid.setAbsoluteTolerance(0.5)
        self.pid.setInputRange(-360.0, 360.0)
        self.pid.setSetpoint(heading)
        self.pid.setOutputRange(-0.4, 4.0)
        self.pid.setContinuous(True)

    def initialize(self):
        self.drivetrain.reset()
        self.pid.reset()
        self.pid.enable()

    def execute(self):
        self.getRobot().logger.info("heading %f" % self.drivetrain.getGyroAngle())
        self.drivetrain.freeDrive(self.speed, self.rotation)

    def isFinished(self):
        return self.pid.onTarget()

    def end(self):
        self.pid.disable()
        self.drivetrain.freeDrive(0,0)

    def setRotation(self, r):
        self.rotation = r
