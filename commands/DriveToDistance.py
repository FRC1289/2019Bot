import wpilib
from wpilib.command import Command
import robotmap

__all__ = ['DriveToDistance']

class DriveToDistance(Command):
    '''
    This command initializes the drivetrain to drive straight
    at the commanded speed for a commanded distance.
    It's assumed that the heading to track to will already
    have been set (TurnToHeading), so this command just
    needs to track to zero.
    '''

    def __init__(self, speed, distance):
        super().__init__('DriveToDistance')

        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        self.speed = speed
        self.heading = 0
        self.rotation = 0
        self.targetDistance = distance

        kP = robotmap.gyro_kP
        kD = robotmap.gyro_kD
        kI = robotmap.gyro_kI
        self.pid = wpilib.PIDController(kP, kD, kI,
                                            lambda: self.drivetrain.getGyroAngle(),
                                            lambda r: self.setRotation(r))
        self.pid.setAbsoluteTolerance(0.5)
        self.pid.setInputRange(-360.0, 360.0)
        self.pid.setSetpoint(self.heading)
        self.pid.setOutputRange(-1.0, 1.0)
        self.pid.setContinuous(True)

    def initialize(self):
        self.getRobot().logger.info("Drive To Distance")
        self.drivetrain.reset()
        self.pid.reset()
        self.pid.enable()

    def execute(self):
        self.getRobot().logger.info("heading %f speed %f rot %f, dist %f" % (
            self.drivetrain.getGyroAngle(), self.speed, self.rotation, self.drivetrain.getDistanceDriven()))
        self.drivetrain.freeDrive(self.speed, self.rotation)

    def isFinished(self):
        return True if self.drivetrain.getDistanceDriven() > self.targetDistance else False

    def end(self):
        self.pid.disable()
        self.drivetrain.freeDrive(0,0)

    def setRotation(self, r):
        self.rotation = r
