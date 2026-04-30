import time
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
# Wpisz tutaj wartości z Twojej tabelki: (Napięcie w Voltach, Prędkość w m/s)
# Ważne: Napięcia muszą rosnąć z góry na dół!
TABELA_WIATRU = [
(1.00, 0.00),
    (1.25,  2.6),   # Przykładowy punkt 1: 0.4V to 0 m/s
    (1.35,  6.5),   # Przykładowy punkt 2: 0.8V to 5 m/s
    (1.45, 8.0),   # Przykładowy punkt 3
    (1.52, 10.0),   # Przykładowy punkt 4
    (1.65, 17.0)    # Przykładowy punkt 5 (Max)
]
def wylicz_wiatr(napiecie, tabela):
    """Funkcja przeliczająca napięcie na wiatr na podstawie tabeli"""
    # Jeśli napięcie spadnie poniżej minimum tabeli
    if napiecie <= tabela[0][0]:
        return tabela[0][1]
    
    # Jeśli napięcie przekroczy maksimum tabeli
    if napiecie >= tabela[-1][0]:
        return tabela[-1][1]
        
    # Szukanie odpowiedniego przedziału i interpolacja
    for i in range(len(tabela) - 1):
        v_dol, wiatr_dol = tabela[i]
        v_gora, wiatr_gora = tabela[i+1]
        
        if v_dol <= napiecie <= v_gora:
            # Obliczanie dokładnej wartości pomiędzy dwoma punktami z tabeli
            proporcja = (napiecie - v_dol) / (v_gora - v_dol)
            return wiatr_dol + proporcja * (wiatr_gora - wiatr_dol)
            
    return 0.0

print("Uruchamiam stację meteo... Wciśnij Ctrl+C, żeby wyjść.")
print("-" * 40)

try:
    while True:
        aktualne_napiecie = kanal_anemometru.voltage
        
        # Użycie nowej funkcji z tabelą
        predkosc_wiatru = wylicz_wiatr(aktualne_napiecie, TABELA_WIATRU)

        print(f"Napięcie na ADC: {aktualne_napiecie:.3f} V  |  Wiatr: {predkosc_wiatru:.1f} m/s")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nZakończono odczyty.")
