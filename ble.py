import bluetooth



ble = bluetooth.BLE()
ble.active(True)

SERVICE_UUID = bluetooth.UUID("d0bfbeee-d560-471b-a94c-f136d5540f8e")
COLOR_UUID   = bluetooth.UUID("d0bfbeee-d561-471b-a94c-f136d5540f8e")
BRIGHT_UUID  = bluetooth.UUID("d0bfbeee-d562-471b-a94c-f136d5540f8e")

ble.gap_advertise(None)  # arrêt impératif pour configurer le service Gatt

#((h_color, h_bright),) = ble.gatts_register_services((
handles = ble.gatts_register_services((
    (SERVICE_UUID, (
        (COLOR_UUID, bluetooth.FLAG_WRITE),
        (BRIGHT_UUID, bluetooth.FLAG_WRITE),
    )),
))
print(handles)
((h_color, h_bright),)=handles

flags = b'\x02\x01\x06' 
uuid16 = b'\x03\x03\xAA\xFE' 
name = b"Xavier" 
name_block = bytes([len(name)+1, 0x09]) + name 
adv_data = flags + uuid16 + name_block 
assert len(adv_data) <= 31
ble.gap_advertise(100_000, adv_data)





