from aurigapy import *
import time

def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


ap = AurigaPy(debug=False)

bluetooth = "/dev/rfcomm1" #/dev/rfcomm8 COM7

ap.connect(bluetooth)
print("Conectado")

for i in range(10):
    ap.play_sound(sound=i * 5 + 131, duration_ms=100)

ap.reset_robot()
print("Closing")
ap.close()
