import sensor, image, time
from Driver import DMotor
from pid import PID

class Target():
    def __init__(self):
        self.is_found = False
        self.obj = None
        self.background = None

class Road(Target):
    def __init__(self, size_thrs = 2000, color_thrs = (84, 100, 9, -25, 32, 127)):
        super(Road, self).__init__()
        self.size_threshold = size_thrs
        self.color_threshold = color_thrs

class Car():
    def __init__(self, thopid = PID(p=0.4, i=0), thetapid = PID(p=0.001, i=0)):
        self.motor = DMotor()
        self.lmotor_speed = 0
        self.rmotor_speed = 0
        self.rho_pid = thopid
        self.theta_pid = thetapid
        self._setup()

    def _setup(self):
        sensor.reset() # Initialize the camera sensor.
        sensor.set_pixformat(sensor.RGB565) # use RGB565.
        sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
        sensor.skip_frames(10) # Let new settings take affect.
        sensor.set_auto_whitebal(False) # turn this off.

        return

def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob


def find_road(road):
    road.background = sensor.snapshot().binary([road.color_threshold], invert=True)

    road.obj = road.background.get_regression([(21, 0, 0, 0, 0, 0)], robust = True)
    if road.obj:
        road.is_found = True
        road.background.draw_line(road.obj.line(), color = 127)
    else:
        road.is_found = False
    return

def caculate_car_drive_profile(road, car):
    if road.is_found:
        rho_err = abs(road.obj.rho())-road.background.width()/2
        if road.obj.theta()>90:
            theta_err = road.obj.theta()-180
        else:
            theta_err = road.obj.theta()
        if road.obj.magnitude()>8:
            #if -40<b_err<40 and -30<t_err<30:
            rho_output = int(car.rho_pid.get_pid(rho_err,1))
            theta_output = int(car.theta_pid.get_pid(theta_err,1))
            output = rho_output-theta_output
            car.lmotor_speed = -60+output
            car.rmotor_speed = -60-output
        else:
            car.lmotor_speed = 0
            car.rmotor_speed = 0
    else:
        car.lmotor_speed = 30
        car.rmotor_speed = 0

car = Car()
road = Road(2000, (84, 100, 9, -25, 32, 127))
while(True):
    find_road(road)
    caculate_car_drive_profile(road, car)
    car.motor.set_speed_v2(car.lmotor_speed, car.rmotor_speed)
