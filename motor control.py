import RPi.GPIO as GPIO
import tkinter as tk

# 모터 상태
STOP = 0
FORWARD = 1
BACKWARD = 2

# PIN 설정
HIGH = 1
LOW = 0

# 실제 핀 정의
# PWM PIN
ENA = 26  # 37 pin

# GPIO PIN
IN1 = 19  # 37 pin
IN2 = 13  # 35 pin

# 핀 설정 함수
def setPinConfig(EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    pwm = GPIO.PWM(EN, 100)  # 100khz 로 PWM 동작 시킴
    pwm.start(0)  # 우선 PWM 멈춤
    return pwm

# 모터 제어 함수
def setMotorControl(pwm, INA, INB, speed, stat):
    pwm.ChangeDutyCycle(speed)
    if stat == FORWARD:
        GPIO.output(INA, HIGH)
        GPIO.output(INB, LOW)
    elif stat == BACKWARD:
        GPIO.output(INA, LOW)
        GPIO.output(INB, HIGH)
    elif stat == STOP:
        GPIO.output(INA, LOW)
        GPIO.output(INB, LOW)

# 모터 제어함수 간단하게 사용하기 위해 한번 더 래핑
def setMotor(speed, stat):
    setMotorControl(pwmA, IN1, IN2, speed, stat)

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pwmA = setPinConfig(ENA, IN1, IN2)

# tkinter GUI 설정
def create_gui():
    root = tk.Tk()
    root.title("Motor Control")
    
    # 앞으로 버튼
    forward_button = tk.Button(root, text="Forward", command=lambda: setMotor(100, FORWARD))
    forward_button.pack(fill=tk.X)

    # 뒤로 버튼
    backward_button = tk.Button(root, text="Backward", command=lambda: setMotor(100, BACKWARD))
    backward_button.pack(fill=tk.X)

    # 정지 버튼
    stop_button = tk.Button(root, text="Stop", command=lambda: setMotor(0, STOP))
    stop_button.pack(fill=tk.X)

    root.mainloop()

# GUI 실행
if __name__ == "__main__":
    create_gui()

# 종료 시 GPIO 클린업
GPIO.cleanup()