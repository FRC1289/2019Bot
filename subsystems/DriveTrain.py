import wpilib
from wpilib.command.subsystem import Subsystem
import ctre
import wpilib.drive
import robotmap

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

    def __init__(self, logger):
        super().__init__('DriveTrain')

        self.LF_motor = ctre.WPI_TalonSRX(robotmap.CAN_LFmotor)
        self.RF_motor = ctre.WPI_TalonSRX(robotmap.CAN_RFmotor)
        self.LR_motor = ctre.WPI_TalonSRX(robotmap.CAN_LRmotor)
        self.RR_motor = ctre.WPI_TalonSRX(robotmap.CAN_RRmotor)

        self.motorSetup()

        self.leftSCG = wpilib.SpeedControllerGroup(self.LF_motor, self.RF_motor)
        self.rightSCG = wpilib.SpeedControllerGroup(self.RF_motor, self.RR_motor)

        self.driveTrain = wpilib.drive.DifferentialDrive(self.leftSCG, self.rightSCG)
        self.driveTrain.stopMotor()

        self.gyro = wpilib.AnalogGyro(robotmap.AIO_Gyro)
        self.logger = logger
        

    # drive straight
    def driveStraight(self):
        ''' 
        use the gyro & a pid controller to move in a straight direction
        '''
        pass

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
    def freeDrive(self, fwdbk, rot):
        '''
        use the supplied Y & X, drive per arguments
        implement a dead band around 0 to avoid jitter
        '''
        self.driveTrain.arcadeDrive(self.deadBand(fwdbk), self.deadBand(rot), False)
        if self.RF_motor.getSensorCollection().getPulseWidthRiseToRiseUs() == 0:
            self.logger.info("no quad")
        else:
            self.logger.info("%d %d" % (self.RF_motor.getSensorCollection().getQuadraturePosition(),
                                        self.RF_motor.getSensorCollection().getQuadratureVelocity()))
    
    def resetHeading(self):
        self.gyro.reset()

    def getHeading(self):
        return self.gyro.getAngle()

    def motorSetup(self):
        self.LF_motor.setInverted(True)
        self.RR_motor.setInverted(True)

    def deadBand(self, rawInput):
        db = robotmap.deadband
        if abs(rawInput) < db:
            return 0.0
        else:
            return pow(rawInput + db, 3) if rawInput < 0 else pow(rawInput - db, 3)
        