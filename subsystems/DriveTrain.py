import wpilib
from wpilib.command.subsystem import Subsystem
import ctre
import wpilib.drive
import robotmap
import math
from commands import FollowJoystick

__all__ = ['DriveTrain']

pulsesPerRotation = 600
wheelDiameter = 6 #inches
distancePerPulse = (wheelDiameter * math.pi) / pulsesPerRotation

class DriveTrain(Subsystem):
    '''
    This subsystem controls the device that constitute the drive train
    - 4x CAN motors
    - gyro
    - 2x Quad Encoders

    Use encoders to let commands judge distance, velocity
    use gyro to let commands judge drive angle (or use internally via
    pid to drive straight)
    May also get vision angle from coprocessor camera to drive to target
    '''

    def __init__(self, logger, params):
        super().__init__('DriveTrain')
        self._logger = logger
        self._parameters = params

        self.LF_motor = ctre.WPI_TalonSRX(robotmap.CAN_LFmotor)
        self.RF_motor = ctre.WPI_TalonSRX(robotmap.CAN_RFmotor)
        self.LR_motor = ctre.WPI_TalonSRX(robotmap.CAN_LRmotor)
        self.RR_motor = ctre.WPI_TalonSRX(robotmap.CAN_RRmotor)
        self.motorSetup()
        self.leftSCG = wpilib.SpeedControllerGroup(self.LF_motor, self.LR_motor)
        self.rightSCG = wpilib.SpeedControllerGroup(self.RF_motor, self.RR_motor)
        self.driveTrain = wpilib.drive.DifferentialDrive(self.leftSCG, self.rightSCG)
        self.driveTrain.stopMotor()

        self.gyro = wpilib.AnalogGyro(robotmap.AIO_Gyro)
        self.gyro.setPIDSourceType(wpilib.PIDController.PIDSourceType.kDisplacement)
        self.gyro.calibrate()

    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick.FollowJoystick())

    def getGyroAngle(self):
        #self._logger.info("heading: %f" % self.gyro.getAngle())
        return self.gyro.getAngle()

    # drive to target
    def driveToTarget(self):
        '''
        use the angle supplied by the coprocessor to drive to the target
        May need an ultrasonic sensor to detect distance
        Will need to do the math to make sure angle of approach is 
        purpendicular, and not oblique
        '''
        pass

    # arcade drive
    def drive(self, fwdbk, rot):
        self.driveTrain.arcadeDrive(fwdbk, rot)

    def freeDrive(self, fwdbk, rot):
        '''
        use the supplied forwawrd and rotational args, drive per arguments
        implement a dead band around 0 to avoid jitter
        '''
        self.driveTrain.arcadeDrive(self.deadBand(fwdbk), self.deadBand(rot), False)
  
    def reset(self):
        self.freeDrive(0,0)
        self.gyro.reset()

    def motorSetup(self):
        self.LR_motor.setInverted(False)
        self.RF_motor.setInverted(False) 
        self.LF_motor.setInverted(False) 
        self.LF_motor.setSafetyEnabled(False) #should be True
        self.RF_motor.setSafetyEnabled(False)
        self.LR_motor.setSafetyEnabled(False)
        self.RR_motor.setSafetyEnabled(False)
        

    def deadBand(self, rawInput):
        db = self._parameters.getValue('joystickDeadband')
        if abs(rawInput) < db:
            return 0.0
        else:
            return pow(rawInput + db, 3) if rawInput < 0 else pow(rawInput - db, 3)

    def getDistanceDriven(self):
        return self.RR_encoder.getDistance()
