# coding=utf-8
from aurigapy import *
from time import *
from time import gmtime, strftime

ap = AurigaPy(debug=False)

bluetooth = "/dev/tty.Makeblock-ELETSPP"
usb = "/dev/tty.wchusbserial1420"

def timestamp():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


print("%r Conectando..." % timestamp())
ap.connect(usb)
print("%r Conectado!" % timestamp())


print("Moving up...")
ap.set_led_onboard(0,0,0xff,0)
ap.move_to(command="forward", degrees=10000, speed=125)
print("End Moving up...")
ap.set_led_onboard(0,0xff,0,0)
print("Moving right...")
ap.move_to(command="right", degrees=2000, speed=125)
print("End Moving right...")
ap.set_led_onboard(0,0,0,0)
print("Closing...")

ap.reset_robot()
print("Reset robot...")
ap.close()
