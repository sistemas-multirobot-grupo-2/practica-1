from aurigapy import *
from time import gmtime, strftime
import threading


def timestamp():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


def play_sound_to(port):
    ap = AurigaPy(debug=False)
    ap.connect(port)
    print("Conectado")

    for i in range(10):
        ap.play_sound(sound=i * 5 + 131, duration_ms=100)

    for i in range(10):
        l = i * 5
        print(l)
        ap.set_led_onboard(0, r=l, g=l, b=l)
        sleep(0.1)

    ap.set_led_onboard(0, r=0, g=0, b=0)

    ap.reset_robot()
    print("Closing")
    ap.close()


t1 = threading.Thread(target=play_sound_to, args=("/dev/tty.Makeblock-ELETSPP",))
t2 = threading.Thread(target=play_sound_to, args=("/dev/tty.Makeblock-ELETSPP-1",))

t1.start()
t2.start()
t1.join()
t2.join()
