import sensor, image, time
from Driver import DMotor
from pid import PID

class Target():
    def __init__(self):
        self.is_found = False
        self.obj = None
        self.background = None

class Ball(Target):
    def __init__(self, size_thrs = 2000, color_thrs = (48, 78, -71, -30, 0, 53)):
        super(Ball, self).__init__()
        self.size_threshold = size_thrs
        self.color_threshold = color_thrs

class Car():
    def __init__(self, xpid = PID(p=0.3, i=0.07, imax=10), ypid = PID(p=0.03, i=0.01, imax=20)):
        self.motor = DMotor()
        self.lmotor_speed = 0
        self.rmotor_speed = 0
        self.x_pid = xpid
        self.h_pid = ypid
        self._setup()

    def _setup(self):
        sensor.reset() # Initialize the camera sensor.
        sensor.set_pixformat(sensor.RGB565) # use RGB565.
        sensor.set_framesize(sensor.QVGA) # use QQVGA for speed.
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

def find_ball(ball):
    ball.background = sensor.snapshot() # Take a picture and return the image.

    blobs = ball.background.find_blobs([ball.color_threshold])
    if blobs:
        ball.is_found = True
        ball.obj = find_max(blobs)
        ball.background.draw_rectangle(ball.obj[0:4]) # rect
        ball.background.draw_cross(ball.obj[5], ball.obj[6]) # cx, cy
    else:
        ball.is_found = False
    return

def caculate_car_drive_profile(ball, car):
    if ball.is_found:
        x_error = ball.obj.cx() - ball.background.width()/2
        h_error = ball.obj.pixels() - ball.size_threshold

        x_output = int(car.x_pid.get_pid(x_error,1))
        h_output = int(car.h_pid.get_pid(h_error,1))

        car.lmotor_speed = h_output+x_output
        car.rmotor_speed = h_output-x_output
    else:
        car.lmotor_speed = 30
        car.rmotor_speed = 0

car = Car()
ball = Ball(2000, (48, 78, -71, -30, 0, 53))
while(True):
    find_ball(ball)
    caculate_car_drive_profile(ball, car)
    car.motor.set_speed_v2(car.lmotor_speed, car.rmotor_speed)
