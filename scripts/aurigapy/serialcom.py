import serial
import glob
import sys

class SerialCom:
    """
    From <https://github.com/Kreativadelar>
    """

    def __init__(self):
        self._serial = None

    def connect(self, port='/dev/tty.Makeblock-ELETSPP'):
        try:
            self._serial = serial.Serial(port, 115200, timeout=4)
        except:
            assert False, "Error: cannot open this port: " + port

    def device(self):
        return self._serial

    @staticmethod
    def scan_serial_ports():
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            s = serial.Serial()
            s.port = port
            s.close()
            result.append(port)
        return result

    def write(self, data):
        self._serial.write(data)

    def read(self):
        return self._serial.read()

    def is_open(self):
        return self._serial.isOpen()

    def in_waiting(self):
        return self._serial.inWaiting()

    def close(self):
        self._serial.close()