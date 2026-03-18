import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)      # numeracja GPIO (BCM)
GPIO.setup(17, GPIO.IN)     # GPIO17 jako wejście

try:
    while True:
        state = GPIO.input(17)
        print(state)        # 0 lub 1
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
