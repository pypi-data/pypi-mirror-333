from odrive.enums import AxisState, ControlMode
import time

# Motor class
class Motor:
    COUNTS_PER_REV: int
    KV: int
    KT: float
    MAX_CURRENT: int
    GEARBOX_RATIO: int
    direction: int
    TORQUE_OFFSET: float
    trapTraj: bool
    zeroPosition: float
    zeroIsSet: bool
    odrvAxis: any

    # init
    def __init__(self, TORQUE_OFFSET=0, trapTraj=False, zeroPos=0):
        self.TORQUE_OFFSET = TORQUE_OFFSET
        self.trapTraj = trapTraj
        self.zeroPosition = zeroPos
        self.zeroIsSet = False
    
    #set axis to torque control
    def setTorqueControl(self):
        time.sleep(0.5)
        self.odrvAxis.requested_state = AxisState.CLOSED_LOOP_CONTROL
        time.sleep(0.2)
        self.odrvAxis.controller.config.control_mode = ControlMode.TORQUE_CONTROL
        time.sleep(0.2)
        self.odrvAxis.controller.config.input_mode = 1
        time.sleep(0.2)
    
    # Set axis to position control
    def setPositionControl(self):
        time.sleep(0.5)
        self.odrvAxis.requested_state = AxisState.CLOSED_LOOP_CONTROL
        time.sleep(0.2)
        self.odrvAxis.controller.config.control_mode = ControlMode.POSITION_CONTROL
        time.sleep(0.2)
        if self.trapTraj:
            self.odrvAxis.controller.config.input_mode = 5 # InputMode.TRAP_TRAJ
        else:
            self.odrvAxis.controller.config.input_mode = 1 # InputMode.PASSTHROUGH
        time.sleep(0.2)

    # Return estimated position of motor in degrees
    def getPosition(self):
        return (self.odrvAxis.encoder.pos_estimate / self.GEARBOX_RATIO) * 360 * self.direction
    
    # Return estimated velocity of motor in degrees
    def getVelocity(self):
        return (self.odrvAxis.encoder.vel_estimate / self.GEARBOX_RATIO) * 360 * self.direction
    
    #set trapezoidal control parameters in degrees
    def setTrapParams(self, maxSpeed:float, acceleration: float):
        self.odrvAxis.trap_traj.config.vel_limit = maxSpeed * self.GEARBOX_RATIO / 360
        self.odrvAxis.trap_traj.config.accel_limit = acceleration * self.GEARBOX_RATIO / 360
        self.odrvAxis.trap_traj.config.decel_limit = acceleration * self.GEARBOX_RATIO / 360

    #enable trpezoidal trajectory
    def enableTrapTraj(self):
        self.trapTraj = True
        #self.odrvAxis.controller.config.input_mode = 5 # InputMode.TRAP_TRAJ

    #enable trpezoidal trajectory
    def disableTrapTraj(self):
        self.trapTraj = False
        #self.odrvAxis.controller.config.input_mode = 1 # InputMode.PASSTHROUGH

    # Set torque for torque control
    def setTorque(self, torqueSetting:float):
        if torqueSetting < 0:
            torqueSetting -= self.TORQUE_OFFSET
        elif torqueSetting > 0:
            torqueSetting += self.TORQUE_OFFSET
        self.odrvAxis.controller.input_torque = torqueSetting / self.GEARBOX_RATIO * self.direction

    # Set position for position control in degrees
    def setPosition(self, positionSetting:float):
        self.odrvAxis.controller.input_pos = (positionSetting * self.GEARBOX_RATIO / 360 * self.direction) + self.zeroPosition

    def setPositionAndWait(self, positionSetting:float):
        # Set new setpoint and wait till motor is within 1 degree of desired position
        self.odrvAxis.controller.input_pos = (positionSetting * self.GEARBOX_RATIO / 360 * self.direction) + self.zeroPosition
        while abs((positionSetting * self.GEARBOX_RATIO / 360 * self.direction) + self.zeroPosition - self.odrvAxis.encoder.pos_estimate) > 1 * self.GEARBOX_RATIO / 360 :
            time.sleep(0.05)
    
    # Set position relative to current motor position in degrees
    def setRelativePosition(self, positionSetting:float):
        # Get current position
        currentPos = self.odrvAxis.encoder.pos_estimate
        self.odrvAxis.controller.input_pos = currentPos + (positionSetting * self.GEARBOX_RATIO / 360) * self.direction
    
    # Set current position as zero
    def setCurrentAsZero(self):
        self.zeroPosition = self.odrvAxis.encoder.pos_estimate
        self.zeroIsSet = True

    # Check if the odrive has any errors
    def error(self):
        if self.odrvAxis.error or self.odrvAxis.motor.error or self.odrvAxis.encoder.error or self.odrvAxis.controller.error:
            return True
        else:
            return False

    # Get all error codes and return as string 
    def getError(self):
        error = 'ODrive error state: ' + str(self.odrvAxis.error) + "\n" + 'ODrive motor error: ' + str(self.odrvAxis.motor.error) + "\n" + 'ODrive encoder error: ' + str(self.odrvAxis.encoder.error) + "\n" + 'ODrive controller error:: ' + str(self.odrvAxis.controller.error)
        return error

    # Set axis to idle
    def setIdle(self):
        self.odrvAxis.requested_state = AxisState.IDLE