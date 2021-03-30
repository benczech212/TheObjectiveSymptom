import board
import neopixel

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

NUM_PIXELS = 10
np = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.1)
next_pixel = 0


while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    while ble.connected:
        packet = Packet.from_stream(uart)
        if isinstance(packet, ColorPacket):
            print(packet.color)
            np[next_pixel] = packet.color
            np[(next_pixel + 1) % NUM_PIXELS] = (0, 0, 0)
        next_pixel = (next_pixel + 1) % NUM_PIXELS
