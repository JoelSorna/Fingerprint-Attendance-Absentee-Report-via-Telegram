import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

lcd = CharLCD(
pin_rs=25,
pin_rw=None,
pin_e=24,
pins_data=[23,17,18,22],
numbering_mode=GPIO.BCM,
cols=16,
rows=2
)

def display_message(l1="",l2=""):
    lcd.clear()
    lcd.cursor_pos=(0,0)
    lcd.write_string(l1[:16])
    lcd.cursor_pos=(1,0)
    lcd.write_string(l2[16:])