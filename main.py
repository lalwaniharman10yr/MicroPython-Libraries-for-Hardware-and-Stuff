# ===============================================================
#   main.py  -  A fun demo for "My first Library"
#   Made by Harman (age 10)  -  Raspberry Pi Pico / Pico W
# ---------------------------------------------------------------
#   This shows a few library functions working together:
#   measure distance, blink an LED, beep a buzzer, move a servo,
#   and read a joystick. Change the pin numbers to match YOUR wiring!
# ===============================================================

import utime

# If you renamed the library file to mylib.py, this import just works.
from mylib import Ultrasonic, LED, ABUZZER, Servo, Joystick

# ---- Change these to match how YOU wired your Pico ----
TRIG_PIN = 3
ECHO_PIN = 2
LED_PIN = "LED"      # use 25 on a normal Pico
BUZZER_PIN = 15
SERVO_PIN = 0
JOY_X = 27
JOY_Y = 26
JOY_SW = 16

# How close (in cm) counts as "something is near!"
NEAR_DISTANCE_CM = 15


def blink_hello():
    """Blink the LED three times to say hello."""
    for _ in range(3):
        LED(LED_PIN, 1)
        utime.sleep_ms(200)
        LED(LED_PIN, 0)
        utime.sleep_ms(200)


def run():
    print("Harman's Pico demo is starting! Press Ctrl-C to stop.")
    blink_hello()

    while True:
        distance = Ultrasonic(TRIG_PIN, ECHO_PIN)
        x, y, pressed = Joystick(JOY_X, JOY_Y, JOY_SW)
        print("Distance:", distance, "cm   Joystick:", x, y, "Button:", pressed)

        if distance < NEAR_DISTANCE_CM:
            print("Something is close! Beep + light ON")
            LED(LED_PIN, 1)
            ABUZZER(BUZZER_PIN, "ON")
        else:
            LED(LED_PIN, 0)
            ABUZZER(BUZZER_PIN, "OFF")

        # Pushing the joystick button waves the servo like a hello
        if pressed == 0:
            Servo(SERVO_PIN, 0)
            utime.sleep_ms(300)
            Servo(SERVO_PIN, 180)
            utime.sleep_ms(300)

        utime.sleep_ms(200)


run()
