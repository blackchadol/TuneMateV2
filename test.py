import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
LED_PIN = 17  # 사용할 GPIO 핀 번호 (BCM 모드 기준)

GPIO.setmode(GPIO.BCM)  # BCM 모드 사용
GPIO.setup(LED_PIN, GPIO.OUT)  # 핀을 출력 모드로 설정
print("Program started")
# 이후 코드

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED 켜기
        print("LED ON")
        time.sleep(1)  # 1초 대ls
        GPIO.output(LED_PIN, GPIO.LOW)  # LED 끄기
        print("LED OFF")
        time.sleep(1)  # 1초 대기
except KeyboardInterrupt:
    print("프로그램 종료")
finally:
    GPIO.cleanup()  # GPIO 핀 초기화
