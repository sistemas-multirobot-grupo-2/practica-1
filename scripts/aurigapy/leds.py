from aurigapy import *
from time import sleep
from time import gmtime, strftime
from random import randrange


def timestamp():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


def onColor(value,timeout):
    if timeout:
        print("Timeout")



ap = AurigaPy(debug=False)

bluetooth = "/dev/tty.Makeblock-ELETSPP"
usb = "/dev/tty.wchusbserial1420"
usb_Pilar="COM7"

ap.connect(usb_Pilar)
print("Conectado")

sleep(2)

for i in range(10):
    l = i * 25
    print(l)
    ap.set_led_onboard(0, r=l, g=l, b=l)
    sleep(0.1)

print("Colors")
ap.set_led_onboard(0, r=0, g=0, b=0)

for i in range(400):
    lid = randrange(1, 11)
    rr = randrange(0, 10)
    rb = randrange(0, 10)
    rg = randrange(0, 10)
    ap.set_led_onboard(lid, r=rr, g=rg, b=rb, callback=onColor)

sleep(3)


print("Reset")
ap.reset_robot()
print("Closing")
ap.close()
