# Connect Mahjong Panel to PC as USB keyboard.
# 
# Build using CircuitPython, with adafruit_hid library and put on a Raspberry Pi Pico.
#
# Instructions:
# - Hook up COM pins to GP0-5
# - Hook up KEY pins to GP6-10
# - Connect USB to PC.
# - See button_mappings dictionary if you want to modify keys.
#
# buffi - 2022

import board
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from digitalio import DigitalInOut, Direction, Pull

key_pins = list(map(DigitalInOut, [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5]))
com_pins = list(map(DigitalInOut, [board.GP6, board.GP7, board.GP8, board.GP9, board.GP10]))

for pin in key_pins:
    pin.direction, pin.pull  = Direction.INPUT,  Pull.UP
for pin in com_pins:
    pin.direction, pin.value = Direction.OUTPUT, 1  

kbd = Keyboard(usb_hid.devices)

button_mappings = {
    # First four COM pins are used for all Mahjong games.
    #   A          E          I          M                 KAN                   START
    0: [Keycode.A, Keycode.E, Keycode.I, Keycode.M,        Keycode.LEFT_CONTROL, Keycode.ONE],
    #   B          F          J          N                 REACH                 BET
    1: [Keycode.B, Keycode.F, Keycode.J, Keycode.N,        Keycode.LEFT_SHIFT,   Keycode.THREE],
    #   C          G          K          CHI               PON                   NOT_USED
    2: [Keycode.C, Keycode.G, Keycode.K, Keycode.SPACE,    Keycode.Z,            Keycode.PERIOD],
    #   D          H          L          PON               NOT_USED              NOT_USED
    3: [Keycode.D, Keycode.H, Keycode.L, Keycode.LEFT_ALT, Keycode.PERIOD,       Keycode.PERIOD],

    # COM 4 is only used for Betting style games.
    #   LAST               TAKE                   WUP                  F.F.       BIG            SMALL
    4: [Keycode.RIGHT_ALT, Keycode.RIGHT_CONTROL, Keycode.RIGHT_SHIFT, Keycode.Y, Keycode.ENTER, Keycode.BACKSPACE]
}

pressed = set()  # Keycodes currently pressed.

def set_press_state(button, is_pressed):
    if is_pressed and button not in pressed:
        print ("Pressing keycode: " + str(button))
        pressed.add(button)
        kbd.press(button)
    if not is_pressed and button in pressed:
        print ("Unpressing keycode: " + str(button))
        pressed.remove(button)
        kbd.release(button)
  
while True:
    for com_idx, com in enumerate(com_pins):
        com.value = 0
        for key_idx, key in enumerate(key_pins):
            set_press_state(button_mappings[com_idx][key_idx], not key.value)
        com.value = 1
    time.sleep(0.01)
