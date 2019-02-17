from wpilib.command import Command
from wpilib import Timer
import wpilib
from subsystems.Scooper import Scooper

__all__ = ['Expel']

class Expel(Command):
    def __init__(self):
        super().__init__('Expel')
        self._scooper = self.getRobot().scooper
        self.requires(self._scooper)
        self._logger = self.getRobot().logger
        self._timer = Timer()

    def initialize(self):
        self._scooper.stop()
        self._timer.reset()
        self._timer.start()

    def execute(self):
        self._scooper.expel()

    def isFinished(self):
        return True if self._timer.get() > 0.5 else False
             
    def end(self):
        self._scooper.stop()
