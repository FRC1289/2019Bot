from wpilib.command import TimedCommand
import wpilib

class RunMotor(TimedCommand):
    def __init__(self):
        super().__init__('RunMotor', 10.0)
        self.motor = self.getRobot().motor
        self.requires(self.motor)
        self.logger = self.getRobot().logger

    def initialize(self):
        self.motor.setSpeed(0)

    def execute(self):
        self.motor.setSpeed(0.1)

        
#    def isFinished(self):
 #       return True
     
    def end(self):
        self.motor.setSpeed(0)

