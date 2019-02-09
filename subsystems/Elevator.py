import wpilib
from enum import Enum, auto
from wpilib.command.subsystem import Subsystem
import robotmap

__all__ = ['Elevator', 'ElevatorLimit', 'ElevatorPosition']

class ElevatorLimit(Enum):
        LOWER = 1
        UPPER = 2
	
class ElevatorPosition():
        GROUND = auto()
        LOWER_HATCH = auto()
        MID_HATCH = auto()
        LOWER_CARGO = auto()
        MID_CARGO = auto()
        STOWED = auto()
        INITIAL_DEPLOY = auto()
	
class Elevator(Subsystem):
	def __init__(self, logger, params):
		super().__init__('Elevator')
		self._parameters = params
		self._logger = logger
		self._motor = wpilib.Talon(robotmap.PWM_Elevator)
		self._encoder = wpilib.Encoder(robotmap.DIO_elevatorASource, robotmap.DIO_elevatorBsource,
                                               False, wpilib.Encoder.EncodingType.k1X)
		self._encoder.reset()
		self._lowerLimitSwitch = wpilib.DigitalInput(robotmap.DIO_elevatorLowerLimit)
		self._upperLimitSwitch = wpilib.DigitalInput(robotmap.DIO_elevatorUpperLimit)
		self._positionMap = {}
		self.InitializePositionMap()
		
	def InitializePositionMap(self):
		self._positionMap[ElevatorPosition.GROUND] = self._parameters.getValue('elevatorGround')
		self._positionMap[ElevatorPosition.LOWER_HATCH] = self._parameters.getValue('elevatorLowerHatch')
		self._positionMap[ElevatorPosition.MID_HATCH] = self._parameters.getValue('elevatorMidHatch')
		self._positionMap[ElevatorPosition.LOWER_CARGO] = self._parameters.getValue('elevatorLowerCargo')
		self._positionMap[ElevatorPosition.MID_CARGO] = self._parameters.getValue('elevatorMidCargo')
		self._positionMap[ElevatorPosition.STOWED] = self._parameters.getValue('elevatorStowed')
		
	def PositionValue(self, position):
		return self._positionMap[position]
		
	def currentPosition(self):
		return self._encoder.get()
		
	def atLimit(self, limit):
		if limit == ElevatorLimit.LOWER:
			return self._lowerLimitSwitch.get()
		elif limit == ElevatorLimit.UPPER:
			return self._upperLimitSwitch.get()
		else:
			return False
		
	def move(self, speed):
		self._motor.set(speed)
		
	def stop(self):
		self._motor.set(0)
