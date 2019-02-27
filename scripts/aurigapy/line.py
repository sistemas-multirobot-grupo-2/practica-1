from aurigapy import *
from time import sleep
from time import gmtime, strftime


def timestamp():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


ap = AurigaPy(debug=False)

bluetooth = "/dev/tty.Makeblock-ELETSPP"
usb = "/dev/tty.wchusbserial1420"

ap.connect(usb)
print("Conectado")

sleep(2)

for i in range(100):
    r = ap.get_line_sensor(9)
    print("%r > %r " % (timestamp(), r))

ap.reset_robot()
ap.close()
