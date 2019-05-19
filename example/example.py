import pyb
import time
import _thread
from Sensor import TP, Button
from Driver import DMotor, LED
from KTLcd import *
	
       
def real_time_temp(n, dt):
	temp = TP()
	cnt = 0
	while 1:
		val = temp.get_temp()
		time.sleep(dt)
		print(cnt, val)
		cnt = cnt + 1

def run_motor(n, dt):
	motor = DMotor()
	while 1:
		val = motor.set_speed(45, 1, 45, 1)
		time.sleep(dt)
		val = motor.set_speed(45, 2, 45, 2)
		time.sleep(dt)
		
def exled(id, dt):
	led = LED()
	while 1:
		led.set_color(80, 0, 0)
		time.sleep(dt)
		led.set_color(0, 80, 0)
		time.sleep(dt)
		led.set_color(0, 0, 80)
		time.sleep(dt)

def get_button(id, dt):
	but = Button()
	while 1:
		status = but.get_status()
		print(status)
		time.sleep(dt)

def draw_face(id, dt):
	lcd = KTLcd()
	while 1:
		lcd.clear_text()
		lcd.draw_face('smile', 2, 10)
		time.sleep(dt)
		lcd.clear_text()
		lcd.draw_face('cry', 2, 10)
		time.sleep(dt)
		lcd.clear_text()
		lcd.draw_face('normal', 2, 10)
		time.sleep(dt)
		

time.sleep(2000)
_thread.start_new_thread(real_time_temp, (1, 1000))
_thread.start_new_thread(run_motor, (1, 1000))
_thread.start_new_thread(draw_face, (1, 5000))
_thread.start_new_thread(exled, (3, 200))
time.sleep(200)
_thread.start_new_thread(get_button, (3, 5000))