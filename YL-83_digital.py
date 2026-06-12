from db import Database
import RPi.GPIO as GPIO
import time

db = Database()

GPIO.setmode(GPIO.BCM)      # numeracja GPIO (BCM)
GPIO.setup(17, GPIO.IN)     # GPIO17 jako wejście

pada = False
start_zero = None  # moment wykrycia 0

while True:
    sensor = GPIO.input(17)  # tu wstaw swoją funkcję

    if sensor == 0:
        if start_zero is None:
            start_zero = time.time()  # zapamiętaj kiedy zaczęło być 0
        
        # sprawdź ile czasu już jest 0
        if time.time() - start_zero >= 5:
            pada = 1
    else:
        start_zero = None  # reset licznika
        pada = 0       # opcjonalnie, zależy czy ma się resetować

    print("sensor:", sensor, "pada:", pada)

    time.sleep(0.1)  # małe opóźnienie, żeby nie zjadać CPU
    

sql = "INSERT INTO `yl83` (`pada`) VALUES (%s)"
db.execute(sql, (int(pada)))

db.close()