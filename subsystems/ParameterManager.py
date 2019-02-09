from networktables import NetworkTables
import robotmap

__all__ = ['ParameterManager']

class ParameterManager():
        def __init__(self, logger):
            self._map = {}
            self._logger = logger
            NetworkTables.addConnectionListener(self.connectionListener, immediateNotify=True)
            self._smartDashboard = NetworkTables.getTable('SmartDashboard')
            self._smartDashboard.addEntryListener(self.valueChanged)
            self.PopulateMap()
		
        def valueChanged(self, table, key, value, isNew):
                self._map[key] = value
        
        def connectionListener(self, connected, info):
                self._logger.info("%s %s" % (info, connected))

	# smartdash does not store integers, only floats or strings.
	# So, store everything as a string and cast to appropriate
	# type (based on the key) when asked for. Assumed that values
	# are either float or integer - the subsystem/command 
	# will not use strings.
        def getValue(self, key):
	        floatKeys = ('joystickDeadband', 'gyro_kP', 'gyro_kI', 'gyro_kD',
			     'camera_kP', 'camera_kI', 'camera_kD',
			     'elevatorSpeed', 'armSpeed', 'ingestSpeed', 'expelSpeed')
	        if key in self._map:
		        value = self._map[key]
		        if key in floatKeys:
			        return float(value)
		        else:
			        return int(value)
	        else:
		        self.logger.info('no key %s' % key)
		        return ''
			
        def PopulateMap(self):
	        self._map['joystickDeadband'] = '0.05'	#float
	        self._map['gyro_kP'] = '0.1'			#float
	        self._map['gyro_kI'] = '0'
	        self._map['gyro_kD'] = '0'
	        self._map['camera_kP'] = '0.03'			#float
	        self._map['camera_kI'] = '0'
	        self._map['camera_kD'] = '0'
	        self._map['elevatorGround'] = '0'
	        self._map['elevatorLowerHatch'] = '0'
	        self._map['elevatorMidHatch'] = '0'
	        self._map['elevatorLowerCargo'] = '0'
	        self._map['elevatorMidCargo'] = '0'
	        self._map['elevatorStowed'] = '0'
	        self._map['elevatorSpeed'] = '0.5'		#float
	        self._map['armGround'] = '0'
	        self._map['armLowerHatch'] = '0'
	        self._map['armMidHatch'] = '0'
	        self._map['armLowerCargo'] = '0'
	        self._map['armMidCargo'] = '0'
	        self._map['armStowed'] = '0'
	        self._map['armSpeed'] = '0.5'			#float
	        self._map['ingestSpeed'] = '0.3'		#float
	        self._map['expelSpeed'] = '0.9'			#float
	        self._map['targetSpread'] = '370'
		
	        for key, value in self._map.items():
		        self._smartDashboard.putString(key, value)
