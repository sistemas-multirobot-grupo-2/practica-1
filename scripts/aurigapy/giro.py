from aurigapy import *
from time import sleep
from time import gmtime, strftime


def timestamp():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


ap = AurigaPy(debug=False)

bluetooth = "/dev/tty.Makeblock-ELETSPP"
usb = "/dev/tty.wchusbserial1420"
usb_Pilar = "COM7"
ap.connect(usb_Pilar)
print("Conectado")

sleep(2)

for i in range(100):
    x = ap.get_gyro_sensor_onboard("x")
    y = ap.get_gyro_sensor_onboard("y")
    z = ap.get_gyro_sensor_onboard("z")
    data = str((x, y, z))
    print("%r > %r " % (timestamp(), data))

ap.reset_robot()
ap.close()
