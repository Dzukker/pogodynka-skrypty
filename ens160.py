from db import Database
import board
import adafruit_ens160


db = Database()

i2c = board.I2C()
ens = adafruit_ens160.ENS160(i2c)

bme = db.fetch_latest("bme688")

ens.temperature_compensation = bme["temperature"]
ens.humidity_compensation = bme["humidity"]

print("AQI (1-5):", ens.AQI)
print("TVOC (ppb):", ens.TVOC)
print("eCO2 (ppm):", ens.eCO2)
print()


aqi = int(ens.AQI)
tvoc = int(ens.TVOC)
eco2 = int(ens.eCO2)

db.execute("""
    INSERT INTO jakosc_pogody (AQI, TVOC, eCO2)
    VALUES (%s, %s, %s)
     """, aqi, tvoc, eco2)

db.close()