import wpilib
from enum import Enum
from wpilib.command.subsystem import Subsystem
import robotmap

__all__ = ['Elevator', 'ElevatorLimit', 'ElevatorPosition']

class ElevatorLimit(Enum):
        LOWER = 1
        UPPER = 2
	
class ElevatorPosition(Enum):
        GROUND = 10
        LOWER_HATCH = 20
        MID_HATCH = 30
        LOWER_CARGO = 40
        MID_CARGO = 50
        STOWED = 60
        INITIAL_DEPLOY = 70
	
class Elevator(Subsystem):
	def __init__(self, logger):
		super().__init__('Elevator')
		self._logger = logger
		self._motor = wpilib.Talon(robotmap.PWM_Elevator)
		self._encoder = wpilib.Encoder(robotmap.DIO_elevatorASource, robotmap.DIO_elevatorBsource,
                                               False, wpilib.Encoder.EncodingType.k1X)
		self._encoder.reset()
		self._lowerLimitSwitch = wpilib.DigitalInput(robotmap.DIO_elevatorLowerLimit)
		self._upperLimitSwitch = wpilib.DigitalInput(robotmap.DIO_elevatorUpperLimit)

	def currentPosition(self):
		return self._encoder.get()
		
	def atLimit(self, limit):
		if limit == ElevatorLimit.LOWER:
			return not self._lowerLimitSwitch.get()
		elif limit == ElevatorLimit.UPPER:
			return not self._upperLimitSwitch.get()
		else:
			return False
		
	def move(self, speed):
                self._motor.set(speed)
                #self._logger.info("%d" % self._encoder.get())
		
	def stop(self):
		self._motor.set(0)
