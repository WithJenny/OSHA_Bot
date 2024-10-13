import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

vertical_servo = kit.servo[1]
horizontal_servo = kit.servo[0]

REST_STATE_ANGLE = 120
vertical_servo.actuation_range = 180  # Neutral position for vertical servo
horizontal_servo.actuation_range = 180  # Neutral position for horizontal servo

vertical_servo.angle = REST_STATE_ANGLE
horizontal_servo.angle = 90


def move_servos(servo_motor):
    for i in range(0, 3):
        servo_motor.angle = 150
        time.sleep(0.25)
        servo_motor.angle = 0
        time.sleep(0.25)
        servo_motor.angle = 50
        time.sleep(0.25)


def nod_yes():
    move_servos(vertical_servo)
    vertical_servo.angle = REST_STATE_ANGLE


def nod_no():
    vertical_servo.angle = REST_STATE_ANGLE
    time.sleep(.25)
    move_servos(horizontal_servo)
    horizontal_servo.angle = 90


def thinking():
    vertical_servo.angle = 180
