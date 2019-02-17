import wpilib
from wpilib.command.subsystem import Subsystem
import robotmap

__all__ = ['Scooper']

class Scooper(Subsystem):
        def __init__(self, logger):
                super().__init__('Scooper')
                self._logger = logger
                self._motor = wpilib.Talon(robotmap.PWM_Scooper)
                self._limit = wpilib.DigitalInput(robotmap.DIO_scooperLimit)
                
        def ingest(self):
                self._motor.set(- robotmap.IngestSpeed)
                
        def expel(self):
                self._motor.set(robotmap.ExpelSpeed)
                
        def stop(self):
                self._motor.set(0)

        def atLimit(self):
                return not self._limit.get()
                
