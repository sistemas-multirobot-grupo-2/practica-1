# coding=utf-8

"""

Fidel Aznar Gregori (fidel@dccia.ua.es)
Departamento de Ciencia de la Computación e Inteligencia Artificial.
Universidad de Alicante


The MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import time
import struct


def float2bytes(fval):
    """
    From <https://github.com/Kreativadelar>
    """
    val = struct.pack("f", fval)
    return [val[0], val[1], val[2], val[3]]


def long2bytes(lval):
    """
    From <https://github.com/Kreativadelar>
    """
    val = struct.pack("=l", lval)
    return [val[0], val[1], val[2], val[3]]


def bytes2long(data):
    return struct.unpack('<l', struct.pack('4B', *data))[0]


def bytes2double(data):
    return struct.unpack('<f', struct.pack('4B', *data))[0]


def bytes2short(data):
    return struct.unpack('<h', struct.pack('2B', *data))[0]


def short2bytes(sval):
    """
    From <https://github.com/Kreativadelar>
    """
    val = struct.pack("h", sval)
    return [val[0], val[1]]


def char2byte(cval):
    """
    From <https://github.com/Kreativadelar>
    """
    val = struct.pack("b", cval)
    return val[0]


class Frame:
    FRAME_TYPE_BYTE = 0x01
    FRAME_TYPE_FLOAT = 0x02
    FRAME_TYPE_SHORT = 0x03
    FRAME_TYPE_STRING = 0x04
    FRAME_TYPE_DOUBLE = 0x05
    FRAME_TYPE_LONG = 0x06
    FRAME_TYPE_ACK = 0xF0
    FRAME_TYPE_VERSION = 0xF1
    FRAME_TYPE_UNKNOWN = 0xFF

    def __init__(self, timestamp, frame_type, frame_data, frame_value):
        """

        :param timestamp:
        :param frame_type:
        :param frame_data: Raw frame data
        :param frame_value: Return value inside de frame (if exist)
        """
        self.timestamp = timestamp
        self.frame_type = frame_type
        self.frame_data = frame_data
        self.frame_value = frame_value

    def __str__(self):
        print('[{}]'.format(', '.join(hex(x) for x in self.frame_data)))

    @staticmethod
    def is_frame(data):
        if len(data) >= 4:
            # Verifico el fin de la trama
            if data[-2:] == [0x0d, 0x0a]:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def generate_from_data(data):

        f_value = None
        f_type = None
        f_data = data
        f_timestamp = time.time()

        if data[0:2] == [0xff, 0x55]:
            if data[2:4] == [0x00, 0x01]:  # Byte
                f_type = Frame.FRAME_TYPE_BYTE
                f_value = data[4:]
            elif data[2:4] == [0x00, 0x02]:  # 2Byte Float
                f_type = Frame.FRAME_TYPE_FLOAT
                f_value = bytes2double(data[4:8])
                if f_value < -512 or f_value > 1023:
                    f_value = 0
            elif data[2:4] == [0x00, 0x03]:  # Short
                f_type = Frame.FRAME_TYPE_SHORT
                f_value = bytes2short(data[4:8])
            elif data[2:4] == [0x00, 0x04]:  # String
                s = ''.join([chr(s) for s in data[4:]])
                f_type = Frame.FRAME_TYPE_STRING
                f_value = s
            elif data[2:4] == [0x00, 0x05]:  # Double
                f_type = Frame.FRAME_TYPE_DOUBLE
                f_value = bytes2double(data[4:8])
            elif data[2:4] == [0x00, 0x06]:  # Long
                f_type = Frame.FRAME_TYPE_LONG
                f_value = bytes2long(data[4:8])
            elif data == [0xff, 0x55, 0x0d, 0x0a]:
                f_type = Frame.FRAME_TYPE_ACK
        else:
            if data[0:4] == [0x56, 0x65, 0x72, 0x73]:
                f_type = Frame.FRAME_TYPE_VERSION
                s = ''.join([chr(s) for s in data])
                f_value = s
            else:
                assert False, "generate_from_data: provided data is not a frame"

        return Frame(timestamp=f_timestamp, frame_type=f_type, frame_data=f_data, frame_value=f_value)
