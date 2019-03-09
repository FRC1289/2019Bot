CAN_RRmotor = 1
CAN_RFmotor = 4
CAN_LRmotor = 2
CAN_LFmotor = 3

PWM_Elevator = 0
PWM_Arm = 1
PWM_Scooper = 2

AIO_Gyro = 0

DIO_elevatorASource = 0
DIO_elevatorBsource = 1
DIO_elevatorLowerLimit = 2 
DIO_elevatorUpperLimit = 3
DIO_armASource = 4
DIO_armBsource = 5
DIO_scooperLimit = 6
DIO_armLowerLimit = 7
DIO_armUpperLimit = 8
DIO_armInGameLowerLimit = 9

STK_port = 0
BB_port = 1

STK_automode = 1

BB_ingest = 1
BB_expel = 2
BB_ArmUp = 4  
BB_ArmDown = 3
BB_ElevatorUp = 5
BB_ElevatorDown = 6
BB_LowHatch = 7
BB_MidHatch = 8
BB_LowCargo = 9
BB_MidCargo = 10
BB_ArmMaxDown = 11

camera_kP = 0.006
camera_kI = 0
camera_kD = 0.0
targetDistance = 300 # calibrate such that stops with 10" to go, then use encoders
dockingDistance = 100 # encoder clicks to get to final position
approachSpeed = 0.4

ArmSpeed = 0.5
ElevatorSpeed = 0.5
IngestSpeed = 0.2
ExpelSpeed = 1.0
JoystickDeadband = 0.05

Deploy_Delay = 2.0

motorSafetyTimeout = 0.2
