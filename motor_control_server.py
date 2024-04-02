from flask import Flask, request
import RPi.GPIO as GPIO

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

# GPIO 모드 설정 및 경고 메시지 끄기
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 핀 설정 함수
def setPinConfig(EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    pwm = GPIO.PWM(EN, 100)  # 100kHz로 PWM 동작 시킴
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

pwmA = setPinConfig(ENA, IN1, IN2)

app = Flask(__name__)

@app.route('/motor', methods=['POST'])
def motor_control():
    data = request.get_json()
    command = data['command']
    speed = data.get('speed', 100)  # 기본 속도 설정

    if command == 'forward':
        setMotor(speed, FORWARD)
    elif command == 'backward':
        setMotor(speed, BACKWARD)
    elif command == 'stop':
        setMotor(0, STOP)
    else:
        return "Invalid command", 400

    return "Command executed: {}".format(command), 200

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        GPIO.cleanup()  # 프로그램 종료시 GPIO 핀 상태 초기화
