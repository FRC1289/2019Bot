from wpilib.command import Command
import wpilib
from subsystems.Scooper import Scooper

__all__ = ['Ingest']

class Ingest(Command):
    def __init__(self):
        super().__init__('Ingest')
        self._scooper = self.getRobot().scooper
        self.requires(self._scooper)
        self._logger = self.getRobot().logger

    def initialize(self):
        self._scooper.stop()

    def execute(self):
        self._scooper.ingest()
             
    def end(self):
        self._scooper.stop()
