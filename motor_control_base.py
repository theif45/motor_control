import RPi.GPIO as GPIO
import time

Button_PIN = 21
A1A_PIN = 23
A1B_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(A1A_PIN, GPIO.OUT)
GPIO.setup(A1B_PIN, GPIO.OUT)
GPIO.setup(Button_PIN, GPIO.IN)

PWM_FREQ = 50
A1A = GPIO.PWM(A1A_PIN, PWM_FREQ)
A1B = GPIO.PWM(A1B_PIN, PWM_FREQ)

try:
    while 1:
        if GPIO.input(Button_PIN) == True:
            print('Power On')
            for i in range(50, 100, 1):
                print(i)
                A1A.start(0)
                A1A.ChangeDutyCycle(i)
                time.sleep(0.1)
            A1A.stop()

            time.sleep(1.2)

            for i in range(50, 100, 1):
                print(i)
                A1B.start(0)
                A1B.ChangeCutyCycle(i)
                time.sleep(0.1)
            A1B.stop()

finally:
    GPIO.cleanup()
