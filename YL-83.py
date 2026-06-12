from db import Database
import time
import board
import RPi.GPIO as GPIO
from adafruit_ads1x15 import ADS1015, AnalogIn, ads1x15


DIGITAL_PIN = 26
DIGITAL_CONFIRM_SECONDS = 5
DIGITAL_CHECK_INTERVAL = 0.1


def rain_status_from_voltage(voltage):
    if voltage >= 3.60:
        return "brak opadów"
    elif voltage >= 3.10:
        return "bardzo lekkie opady / wilgoć"
    elif voltage >= 2.50:
        return "lekkie opady"
    elif voltage >= 1.80:
        return "umiarkowane opady"
    elif voltage >= 1.00:
        return "silne opady"
    else:
        return "bardzo silne opady / zalany czujnik"


def read_digital_rain():
    start_zero = None
    last_physical_value = 1
    end_time = time.time() + DIGITAL_CONFIRM_SECONDS

    while time.time() < end_time:
        physical_value = GPIO.input(DIGITAL_PIN)
        last_physical_value = physical_value

        if physical_value == 0:
            if start_zero is None:
                start_zero = time.time()

            if time.time() - start_zero >= DIGITAL_CONFIRM_SECONDS:
                digital = 1
                pada = 1
                return digital, pada
        else:
            start_zero = None

        time.sleep(DIGITAL_CHECK_INTERVAL)

    # Odwrócenie ostatniego fizycznego odczytu:
    # fizyczne 1 -> digital 0
    # fizyczne 0 -> digital 1
    digital = 1 if last_physical_value == 0 else 0
    pada = 0

    return digital, pada


db = Database()

try:
    # Analog przez ADS1015, kanał A1
    i2c = board.I2C()
    ads = ADS1015(i2c)
    chan = AnalogIn(ads, ads1x15.Pin.A1)

    raw = chan.value
    voltage = chan.voltage
    rain_status = rain_status_from_voltage(voltage)

    # Digital przez GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIGITAL_PIN, GPIO.IN)

    digital_value, pada = read_digital_rain()

    print('Rain raw value: {}'.format(raw))
    print('Rain voltage: {:.3f} V'.format(voltage))
    print('Rain status: {}'.format(rain_status))
    print('Digital value after invert: {}'.format(digital_value))


    sql = """
        INSERT INTO `yl83` (`intensywnosc`, `pada`)
        VALUES (%s, %s)
    """
    db.execute(sql, (rain_status, digital_value))

finally:
    GPIO.cleanup()
    db.close()
