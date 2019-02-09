import wpilib
from enum import Enum, auto
from wpilib.command.subsystem import Subsystem
import robotmap

__all__ = ['Arm', 'ArmLimit', 'ArmPosition']

class ArmLimit(Enum):
        LOWER = 1
        UPPER = 2
	
class ArmPosition(Enum):
        GROUND = auto()
        LOWER_HATCH = auto()
        MID_HATCH = auto()
        LOWER_CARGO = auto()
        MID_CARGO = auto()
        STOWED = auto()
        INITIAL_DEPLOY = auto()

class Arm(Subsystem):
	def __init__(self, logger, params):
		super().__init__('Arm')
		self._parameters = params
		self._logger = logger
		self._motor = wpilib.Talon(robotmap.PWM_Arm)
		self._encoder = wpilib.Encoder(robotmap.DIO_armASource, robotmap.DIO_armBsource,
                                               False, wpilib.Encoder.EncodingType.k1X)
		self._encoder.reset()
		self._lowerLimitSwitch = wpilib.DigitalInput(robotmap.DIO_armLowerLimit)
		self._upperLimitSwitch = wpilib.DigitalInput(robotmap.DIO_armUpperLimit)
		self._positionMap = {}
		self.InitializePositionMap()
		
	def InitializePositionMap(self):
		self._positionMap[ArmPosition.GROUND] = self._parameters.getValue('armGround')
		self._positionMap[ArmPosition.LOWER_HATCH] = self._parameters.getValue('armLowerHatch')
		self._positionMap[ArmPosition.MID_HATCH] = self._parameters.getValue('armMidHatch')
		self._positionMap[ArmPosition.LOWER_CARGO] = self._parameters.getValue('armLowerCargo')
		self._positionMap[ArmPosition.MID_CARGO] = self._parameters.getValue('armMidCargo')
		self._positionMap[ArmPosition.STOWED] = self._parameters.getValue('armStowed')
		
	def PositionValue(self, position):
		return self._positionMap[position]

	def currentPosition(self):
		return self._encoder.get()
		
	def atLimit(self, limit):
		if limit == ArmLimit.LOWER:
			return self._lowerLimitSwitch.get()
		elif limit == ArmLimit.UPPER:
			return self._upperLimitSwitch.get()
		else:
			return False
		
	def move(self, speed):
		self._motor.set(speed)
		
	def stop(self):
		self._motor.set(0)
		
