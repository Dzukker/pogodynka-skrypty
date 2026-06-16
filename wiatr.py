from db import Database
import board
import busio
from adafruit_ads1x15.ads1015 import ADS1015
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15 import ads1x15


# ==========================================
# KONFIGURACJA SPRZĘTU
# ==========================================
i2c = busio.I2C(board.SCL, board.SDA)
adc = ADS1015(i2c)
kanal_anemometru = AnalogIn(adc, ads1x15.Pin.A2)


# ==========================================
# TABELA POMIARÓW ANEMOMETRU
# ==========================================
# Format: (napięcie w V, prędkość wiatru w m/s)
# Napięcia muszą rosnąć od góry do dołu.
TABELA_WIATRU = [
    (1.00, 0.00),
    (1.25, 2.6),
    (1.35, 6.5),
    (1.45, 8.0),
    (1.52, 10.0),
    (1.65, 17.0)
]


def wylicz_wiatr(napiecie, tabela):
    """Funkcja przeliczająca napięcie na prędkość wiatru na podstawie tabeli."""

    if napiecie <= tabela[0][0]:
        return tabela[0][1]

    if napiecie >= tabela[-1][0]:
        return tabela[-1][1]

    for i in range(len(tabela) - 1):
        v_dol, wiatr_dol = tabela[i]
        v_gora, wiatr_gora = tabela[i + 1]

        if v_dol <= napiecie <= v_gora:
            proporcja = (napiecie - v_dol) / (v_gora - v_dol)
            return wiatr_dol + proporcja * (wiatr_gora - wiatr_dol)

    return 0.0


db = Database()

try:
    aktualne_napiecie = kanal_anemometru.voltage
    predkosc_wiatru = wylicz_wiatr(aktualne_napiecie, TABELA_WIATRU)

    print("Napięcie anemometru: {:.3f} V".format(aktualne_napiecie))
    print("Prędkość wiatru: {:.1f} m/s".format(predkosc_wiatru))

    sql = "INSERT INTO `wiatr` (`voltage`, `wind_speed`) VALUES (%s, %s)"
    db.execute(sql, (aktualne_napiecie, predkosc_wiatru))

finally:
    db.close()
