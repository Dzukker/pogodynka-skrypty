from db import Database
import board
import adafruit_bme680


db = Database()

i2c = board.I2C()
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)


print('Temperature: {} degrees C'.format(sensor.temperature))
print('Gas: {} ohms'.format(sensor.gas))
print('Humidity: {}%'.format(sensor.humidity))
print('Pressure: {}hPa'.format(sensor.pressure))

sql = "INSERT INTO `bme688` (`temperature`, `gas`, `humidity`, `pressure`) VALUES (%s, %s, %s, %s)"
db.execute(sql, (sensor.temperature, sensor.gas, sensor.humidity, sensor.pressure))

db.close()
