# ============================================================
# ESP32 MicroPython – BLE GATT + Neopixel
# Architecture orientée état
# ============================================================

import bluetooth
import neopixel
import time
from machine import Pin

# ----------------------------
# Configuration matérielle
# ----------------------------
NEOPIXEL_PIN = 8
NEOPIXEL_COUNT = 1

np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NEOPIXEL_COUNT)

# ----------------------------
# État global du système
# ----------------------------
state = {
    "connected": False,
    "color": (255, 0, 0),     # RGB
    "brightness": 50          # %
}

# ----------------------------
# UUID (À PERSONNALISER PAR ELEVE)
# ----------------------------
SERVICE_UUID = bluetooth.UUID("d0bfbeee-d560-471b-a94c-f136d5540f8e")
COLOR_UUID   = bluetooth.UUID("d0bfbeee-d561-471b-a94c-f136d5540f8e")
BRIGHT_UUID  = bluetooth.UUID("d0bfbeee-d562-471b-a94c-f136d5540f8e")
# ----------------------------
# BLE initialisation
# ----------------------------
ble = bluetooth.BLE()
ble.active(True)
ble.gap_advertise(None)
handles = ble.gatts_register_services((
    (SERVICE_UUID, (
        (COLOR_UUID, bluetooth.FLAG_WRITE),
        (BRIGHT_UUID, bluetooth.FLAG_WRITE),
    )),
))
print(handles)
((h_color, h_bright),)=handles

# ----------------------------
# Neopixel update
# ----------------------------
def apply_state():
    r, g, b = state["color"]
    k = state["brightness"] / 100
    np[0] = (int(r * k), int(g * k), int(b * k))
    np.write()

# ----------------------------
# Advertising
# ----------------------------
def start_advertising():
    
    flags = b'\x02\x01\x06' 
    uuid16 = b'\x03\x03\xAA\xFE' 
    name = b"Xavier" 
    name_block = bytes([len(name)+1, 0x09]) + name 
    adv_data = flags + uuid16 + name_block 
    assert len(adv_data) <= 31
    ble.gap_advertise(100_000, adv_data)
# ----------------------------
# IRQ handler
# ----------------------------
def ble_irq(event, data):
    if event == 1:  # _IRQ_CENTRAL_CONNECT
        state["connected"] = True

    elif event == 2:  # _IRQ_CENTRAL_DISCONNECT
        state["connected"] = False
        start_advertising()

    elif event == 3:  # _IRQ_GATTS_WRITE
        conn_handle, value_handle = data

        if value_handle == h_color:
            raw = ble.gatts_read(h_color)
            if len(raw) == 3:
                state["color"] = tuple(raw)
                apply_state()

        elif value_handle == h_bright:
            raw = ble.gatts_read(h_bright)
            if len(raw) == 1:
                state["brightness"] = raw[0]
                apply_state()

# ----------------------------
# Lancement BLE
# ----------------------------
ble.irq(ble_irq)
start_advertising()

# ----------------------------
# Boucle principale (état stable)
# ----------------------------
while True:
    time.sleep(1)




