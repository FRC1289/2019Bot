from wpilib.command import Command
from networktables import NetworkTables
import wpilib
import robotmap

__all__ = ['FollowCamera']

class FollowCamera(Command):
    
    def __init__(self, speed):
        super().__init__(name='FollowCamera')

        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        self.logger = self.getRobot().logger
        self.angle = 0.0
        self.speed = -speed
        self.rotation = 0.0
        self.pidOutput = 0.0
        self.distance = 0
        
        NetworkTables.addConnectionListener(self.connectionListener, immediateNotify=True)
        self.smartDashboard = NetworkTables.getTable('SmartDashboard')
        self.smartDashboard.addEntryListener(self.valueChanged)

        kP = robotmap.camera_kP
        kD = robotmap.camera_kD
        kI = robotmap.camera_kI
        self.pid = wpilib.PIDController(kP, kI, kD,
                                            lambda: self.getAngle(),
                                            lambda r: self.setRotation(r))
        self.pid.setAbsoluteTolerance(0.01)
        self.pid.setInputRange(0, 640)
        self.pid.setSetpoint(320)
        self.pid.setOutputRange(-1.0, 1.0)
        self.pid.setContinuous(True)
        
    def getAngle(self):
        return self.angle

    def setRotation(self, r):
        self.rotation = r
        
    def initialize(self):
        self.drivetrain.reset()
        self.pid.reset()
        self.pid.enable()
        
    def execute(self):
        self.logger.info('center %d %d %0.2f' % (self.angle, self.distance, self.rotation))
        self.drivetrain.drive(-0.3, self.rotation)#self.speed, self.rotation)
        
    def isFinished(self):
        if self.distance > robotmap.targetDistance:
            return True
        else:
            return False
     
    def end(self):
        self.drivetrain.reset()
        self.pid.disable()
        
    def valueChanged(self, table, key, value, isNew):
        if key == 'cameraAngle':
            self.angle = value
        elif key == 'distance':
           self.distance = value
        else:
            pass
        
    def connectionListener(self, connected, info):
        print(info, connected)
