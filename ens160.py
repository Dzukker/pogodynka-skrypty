from db import Database
import board
import adafruit_ens160


db = Database()

i2c = board.I2C()
ens = adafruit_ens160.ENS160(i2c)

bme = db.fetch_latest("bme688")

print("read temp:", int(bme["temperature"]))
print("read humid:",int(bme["humidity"]))

ens.temperature_compensation = int(bme["temperature"])
ens.humidity_compensation = int(bme["humidity"])

print("AQI (1-5):", ens.AQI)
print("TVOC (ppb):", ens.TVOC)
print("eCO2 (ppm):", ens.eCO2)
print()


aqi = int(ens.AQI)
tvoc = int(ens.TVOC)
eco2 = int(ens.eCO2)

sql = "INSERT INTO `ens160` (`AQI`, `TVOC`, `eCO2`) VALUES (%s, %s, %s)"
db.execute(sql, (aqi, tvoc, eco2))

db.close()
