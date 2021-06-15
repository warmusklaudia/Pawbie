from RPi import GPIO
import time
import sys
from repositories.DataRepository import DataRepository

motor_channel = (22, 27, 17, 4)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_channel, GPIO.OUT, initial=GPIO.LOW)


class Motor:
    def setup(self):
        GPIO.setup(motor_channel, GPIO.OUT, initial=GPIO.LOW)

    def start(self, seconds):
        start = time.time()

        while time.time() < start + seconds:
            try:
                GPIO.output(motor_channel, (GPIO.HIGH,
                                            GPIO.LOW, GPIO.LOW, GPIO.HIGH))
                time.sleep(0.002)
                GPIO.output(motor_channel, (GPIO.HIGH,
                            GPIO.LOW, GPIO.LOW, GPIO.HIGH))
                time.sleep(0.002)
                GPIO.output(motor_channel, (GPIO.LOW,
                            GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
                time.sleep(0.002)
                GPIO.output(motor_channel, (GPIO.LOW,
                            GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
                time.sleep(0.002)
                GPIO.output(motor_channel, (GPIO.HIGH,
                            GPIO.HIGH, GPIO.LOW, GPIO.LOW))
                time.sleep(0.002)
            except KeyboardInterrupt as e:
                print(e)

    def stop(self):
        print('motor stopped')
        sys.exit(0)
