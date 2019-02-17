import wpilib
from enum import Enum
from wpilib.command.subsystem import Subsystem
import robotmap

__all__ = ['Arm', 'ArmLimit', 'ArmPosition']

class ArmLimit(Enum):
        LOWER = 1
        UPPER = 2
	
class ArmPosition(Enum):
        GROUND = 10
        LOWER_HATCH = 20
        MID_HATCH = 30
        LOWER_CARGO = 40
        MID_CARGO = 50
        STOWED = 60
        INITIAL_DEPLOY = 70

class Arm(Subsystem):
	def __init__(self, logger):
		super().__init__('Arm')
		self._logger = logger
		self._motor = wpilib.Talon(robotmap.PWM_Arm)
		self._encoder = wpilib.Encoder(robotmap.DIO_armASource, robotmap.DIO_armBsource,
                                               False, wpilib.Encoder.EncodingType.k1X)
		self._encoder.reset()
		self._lowerLimitSwitch = wpilib.DigitalInput(robotmap.DIO_armLowerLimit)
		self._upperLimitSwitch = wpilib.DigitalInput(robotmap.DIO_armUpperLimit)

		
	def currentPosition(self):
		return self._encoder.get()
		
	def atLimit(self, limit):
		if limit == ArmLimit.LOWER:
			return not self._lowerLimitSwitch.get()
		elif limit == ArmLimit.UPPER:
			return not self._upperLimitSwitch.get()
		else:
			return False
		
	def move(self, speed):
		self._motor.set(speed)
		
	def stop(self):
		self._motor.set(0)
		
