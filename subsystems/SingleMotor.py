import wpilib
from wpilib.command.subsystem import Subsystem
import ctre
import robotmap

class SingleMotor(Subsystem):
    '''
    This example subsystem controls a single Talon in PercentVBus mode.
    '''

    def __init__(self, id, logger):
        '''Instantiates the motor object.'''

        super().__init__('SingleMotor')
        self.motor = ctre.WPI_TalonSRX(id)
        self.logger = logger


    def setSpeed(self, speed):
        self.logger.info("%d" % self.motor.getDeviceNumber())
        self.motor.set(speed)


