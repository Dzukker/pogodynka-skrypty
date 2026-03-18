# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time

import board

import adafruit_ens160

import pymysql


i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

ens = adafruit_ens160.ENS160(i2c)

# Set the temperature compensation variable to the ambient temp
# for best sensor calibration
ens.temperature_compensation = 25
# Same for ambient relative humidity
ens.humidity_compensation = 50


while True:
    conn = pymysql.connect(
        host='localhost',
        user='pogodynka',
        password='pogoda2026',
        db='dane-pogodowe',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


    print("AQI (1-5):", ens.AQI)
    print("TVOC (ppb):", ens.TVOC)
    print("eCO2 (ppm):", ens.eCO2)
    print()
    aqi = int(ens.AQI)
    tvoc = int(ens.TVOC)
    eco2 = int(ens.eCO2)
    # new data shows up every second or so
    time.sleep(1)
    try:
        with conn.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `jakosc_pogody` (`AQI`, `TVOC`, `eCO2`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (aqi, tvoc, eco2))

        # Commit changes
        conn.commit()

        print("Record inserted successfully")
    finally:
        conn.close()

