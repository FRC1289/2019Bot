import wpilib
from wpilib.command.subsystem import Subsystem
import robotmap

__all__ = ['Scooper']

class Scooper(Subsystem):
        def __init__(self, logger, params):
	        super().__init__('Scooper')
	        self._parameters = params
	        self._logger = logger
	        self._motor = wpilib.Talon(robotmap.PWM_Scooper)
		
        def ingest(self):
	        self._motor.set(self._parameters.getValue('ingestSpeed'))
		
        def expel(self):
	        self._motor.set(self._parameters.getValue('expelSpeed'))
		
        def stop(self):
	        self._motor.set(0)
		
