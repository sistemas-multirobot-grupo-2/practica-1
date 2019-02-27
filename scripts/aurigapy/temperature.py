from aurigapy import *
from time import sleep
from time import gmtime, strftime


def timestamp():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


ap = AurigaPy(debug=False)

bluetooth = "/dev/tty.Makeblock-ELETSPP"
usb = "/dev/tty.wchusbserial1420"

ap.connect(bluetooth)
print("Conectado")

sleep(2)

for i in range(100):
    r = ap.get_temperature_sensor_onboard()
    print("%r > %r " % (timestamp(), r))

ap.reset_robot()
ap.close()
