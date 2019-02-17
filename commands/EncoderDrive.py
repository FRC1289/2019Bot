import wpilib
from wpilib.command import Command
import robotmap

__all__ = ['EncoderDrive']

class EncoderDrive(Command):
    def __init__(self, speed, distance):
        super().__init__('EncoderDrive')
        self._drivetrain = self.getRobot().drivetrain
        self.requires(self._drivetrain)
        self._speed = speed
        self._logger = self.getRobot().logger
        self._targetDistance = distance

    def initialize(self):
        current = self._drivetrain.encoderPosition()
        self._target = current + self._targetDistance
    
    def execute(self):
        self._logger.info("encoder %d" % self._drivetrain.encoderPosition())
        self._drivetrain.freeDrive(self._speed, 0)

    def isFinished(self):
        current = self._drivetrain.encoderPosition()
        return True if current > self._target else False

    def end(self):
        self._drivetrain.freeDrive(0,0)
