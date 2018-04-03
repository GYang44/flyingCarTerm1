import time
from enum import Enum
import numpy as np
from udacidrone import Drone
from udacidrone.connection import MavlinkConnection
from udacidrone.messaging import MsgID

class Phases(Enum):
    MANUAL = 0
    ARMING = 1
    TAKEOFF = 2
    FLY = 3
    IDLE = 4
    LANDING = 5
    DISARMING = 6

class UpAndDownFlyer(Drone):
    mission = [[],[]]
    def __init__(self, connection):
        super().__init__(connection)
        self.target_position = np.array([0.0, 0.0, 0.0])
        self.in_mission = True

        # initial state
        self.flight_phase = Phases.MANUAL

        # register all your callbacks here
        self.register_callback(MsgID.LOCAL_POSITION,
                               self.local_position_callback)
        self.register_callback(MsgID.LOCAL_VELOCITY,
                               self.velocity_callback)
        self.register_callback(MsgID.STATE,
                               self.state_callback)
        
    def distance(self, pt_1, pt_2):
        pt_1[2] = - pt_1[2]
        val = np.sqrt( sum(np.square(pt_1 - pt_2)))
        return val

    def local_position_callback(self):
        if self.flight_phase == Phases.TAKEOFF:

            # coordinate conversion 
            altitude = -1.0 * self.local_position[2]

            # check if altitude is within 95% of target
            if altitude > 0.95 * self.target_position[2]:
                self.flight_phase = Phases.IDLE

        elif self.flight_phase == Phases.FLY:
            if (self.distance(self.local_position, self.target_position) < 0.1) :
                self.flight_phase = Phases.IDLE
                
    def velocity_callback(self):
        if self.flight_phase == Phases.LANDING:
            if ((self.global_position[2] - self.global_home[2] < 0.01) and
            abs(self.local_position[2]) < 0.01):
                self.disarming_transition()

    def state_callback(self):
        if not self.in_mission:
            return
        if self.flight_phase == Phases.MANUAL:
            self.arming_transition()
        elif self.flight_phase == Phases.ARMING:
            if self.armed:
                self.takeoff_transition()
        elif self.flight_phase == Phases.IDLE:
            self.fly_next()
        elif self.flight_phase == Phases.DISARMING:
            if not self.armed:
                self.manual_transition()
        

    def arming_transition(self):
        print("arming transition")
        self.take_control()
        self.arm()

        # set the current location to be the home position
        self.set_home_position(self.global_position[0],
                               self.global_position[1],
                               self.global_position[2])

        self.flight_phase = Phases.ARMING

    def takeoff_transition(self):
        print("takeoff transition")
        target_altitude = 3.0
        self.target_position[2] = target_altitude
        self.takeoff(target_altitude)
        self.flight_phase = Phases.TAKEOFF

    def landing_transition(self):
        print("landing transition")
        self.land()
        self.flight_phase = Phases.LANDING

    def disarming_transition(self):
        print("disarm transition")
        self.disarm()
        self.flight_phase = Phases.DISARMING

    def manual_transition(self):
        print("manual transition")
        self.release_control()
        self.stop()
        self.in_mission = False
        self.flight_phase = Phases.MANUAL

    def start(self):
        self.start_log("Logs", "NavLog.txt")
        print("starting connection")
        super().start()
        print(self.mission)
        self.stop_log()
        
    def fly_next(self):
        if self.mission: #if there are still mission to accomplish
            self.target_position = self.mission[0]
            self.fly_to_point(self.mission[0])
            del self.mission[0]
        else:
            self.landing_transition()
        return
    
    def fly_to_point(self, destination):
        n, e, a = destination
        print("flying to next waypoint {} {} {}".format(n, e, a))
        drone.cmd_position(n,e,a,0)
        self.flight_phase = Phases.FLY
        return
        
    def load_mission(self, wayPoints):
        self.mission = wayPoints
        return



if __name__ == "__main__":
    wayPoints = [[0,0,3], [0,20,3], [20,20,3], [20,0,3], [0,0,3]]
    conn = MavlinkConnection('tcp:127.0.0.1:5760', 
                             threaded=False, 
                             PX4=False)
    drone = UpAndDownFlyer(conn)
    time.sleep(2)
    drone.load_mission(wayPoints)
    drone.start()

