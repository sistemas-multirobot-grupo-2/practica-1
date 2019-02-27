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

from time import sleep, time
import threading

from frame import Frame
from frame import short2bytes, long2bytes

from serialcom import SerialCom
from response import Response


class AurigaPy:
    def __init__(self, debug: object = False) -> object:

        self._serial = SerialCom()
        self.th = None
        self.exiting = False
        self._read_buffer = []
        self._responsers = []
        self.debug = debug

    def add_responder(self, responder):
        self._responsers.append(responder)

    def connect(self, port):

        rp = Response.generate_response_block(Frame.FRAME_TYPE_VERSION, timeout=5)
        self.add_responder(rp)

        self._serial.connect(port)
        self.th = threading.Thread(target=self._data_reader, args=())
        self.th.start()

        rp.wait_blocking()
        self.set_led_onboard(0, 125, 125, 125)
        sleep(0.1)
        self.set_led_onboard(0, 0, 0, 0)
        sleep(0.1)

    def _process_frame(self, frame):

        # Hay callbacks?
        if len(self._responsers) > 0:

            # Callback timeout?
            r = self._responsers.pop(0)

            if r.is_timeout():
                # El tiempo del callback ha pasado. Notifico que muere

                if r.response_callback is None:
                    r.response_event.set()  # Se trata de una llamada blocking. Le doy paso
                else:
                    r.response_callback(value=None, timeout=True)  # Llamo al callback

                # Se descarta este callbacl pero se vuelve a procesar el paquete
                self._process_frame(frame)

            # Callback vivo
            else:
                # Es compatible el timestamp de este frame con el callback?
                if r.timestamp > frame.timestamp:
                    # El frame es mas nuevo que el callback, no es compatible
                    if self.debug:
                        print("Frame of type %r discarted (timeout): %r" % (frame.frame_type, frame))
                else:
                    # Es compatible por tipo?
                    if r.response_type == frame.frame_type:
                        # Es compatible por tipo

                        if r.response_callback is None:
                            if self.debug:
                                print("Processed callback event (data %r)" % frame.frame_value)
                            r.response_event_data = frame.frame_value
                            r.response_event.set()  # Se trata de una llamada blocking. Le doy paso
                        else:
                            if self.debug:
                                print("Processed callback")
                            r.response_callback(value=frame.frame_value, timeout=False)  # Llamo el callback
                    else:
                        # No compatible por tipo
                        # Existe un callback posterior que pueda manejar este frame?
                        discart_callback = False

                        if len(self._responsers) > 1:
                            for tr in self._responsers[1:]:
                                if tr.timestamp > frame.timestamp and tr.response_type == frame.frame_type:
                                    # Hay un callback posterior compatible. Descarto este
                                    discart_callback = True
                                    break
                        else:
                            print("Discart callback")
                            discart_callback = True

                        # Hay un callback posterior compatible. Descarto este
                        if discart_callback:
                            if self.debug:
                                print("Callback of type %r discarted: %r" % (r.response_type, r.response_callback))

                            if r.response_callback is None:
                                r.response_event.set()  # Se trata de una llamada blocking. Le doy paso
                            else:
                                r.response_callback(value=None, timeout=True)  # Llamo el callback
                        else:
                            # Proceso el paquete con callback posterior
                            self._process_frame(frame)
        else:
            # No hay callbacks. Se descarta el frame
            if self.debug:
                print("Frame of type %r discarted (no callbacks): %r" % (frame.frame_type, frame))

    def _data_reader(self):
        """
        Thread que procesa la lectura del puerto serie. Se encarga de detectar paquetes y someterlos a
        _process_pkg
        :return:
        """
        while True:

            if self._serial.is_open() is True:
                n = self._serial.in_waiting()
                for i in range(n):
                    data = self._serial.read()
                    if len(data) != 0:
                        r = ord(data)
                        self._read_buffer.append(r)

                # sleep(0.01)

                # Si existe un paquete lo proceso y borro el bufer de lectura
                if Frame.is_frame(self._read_buffer):
                    if self.debug:
                        print('Processing [{}]'.format(', '.join(hex(x) for x in self._read_buffer)))

                    frame = Frame.generate_from_data(list(self._read_buffer))
                    self._process_frame(frame)
                    self._read_buffer = []
            else:
                sleep(0.1)
                # Nota: se podrian perder paquetes si no se mandase seguido.
                self._read_buffer = []

            # Verifico el timeout de los callbacks
            for r in self._responsers:
                if r.is_timeout():
                    if self.debug:
                        print("Callback timeout")
                    if r.response_callback is None:
                        r.response_event.set()  # Se trata de una llamada blocking. Le doy paso
                    else:
                        r.response_callback(value=None, timeout=True)  # Llamo al callback
                    self._responsers.remove(r)

            if self.exiting is True:
                # Notifico callbacks y muero
                for r in self._responsers:
                    if r.response_callback is None:
                        r.response_event.set()  # Se trata de una llamada blocking. Le doy paso
                    else:
                        r.response_callback(value=None, timeout=True)  # Llamo al callback
                    self._responsers.remove(r)

                break

    def _write(self, data):
        if self.debug:
            print('Writing [{}]'.format(', '.join(hex(x) for x in data)))
        self._serial.write(data)

    def reset_robot(self):
        rp = Response.generate_response_block(Frame.FRAME_TYPE_ACK, timeout=2)
        self.add_responder(rp)

        self._serial.write(bytearray([0xff, 0x55, 0x2, 0x0, 0x4]))
        self._read_buffer = []

        rp.wait_blocking()

    # ff 55 08 00 02 22 2d <short2 sound_pitch> <short2 duration>
    def play_sound(self, sound=131, duration_ms=1000, callback=None):

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_ACK, timeout=0.1)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_ACK)

        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 0x08, 0x00, 0x02, 0x22, 0x2d] +
                         short2bytes(sound) +
                         short2bytes(duration_ms))
        # print '[{}]'.format(', '.join(hex(x) for x in data))
        self._write(data)

        if callback is None:
            rp.wait_blocking()

    # ff 55 09 00 02 08 00 02
    # Led 0 son todos
    def set_led_onboard(self, led, r, g, b, callback=None):
        assert led >= 0 and led < 12, "Error, led fuera de rango"

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_ACK, timeout=0.1)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_ACK)

        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 0x09, 0x00, 0x02, 0x08, 0x00, 0x02,
                          led, r, g, b])
        # print '[{}]'.format(', '.join(hex(x) for x in data))
        self._write(data)

        if callback is None:
            rp.wait_blocking()

    # ff 55 0b 00 02 3e 01 <slot> <long4 degrees> 0 0 <short2 vel>
    def set_encoder_motor_rotate_until(self, slot, degrees, speed, callback=None):
        assert slot == 1 or slot == 2, "Error, slot not defined"

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_ACK, timeout=0.1)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_ACK)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 0x0b, 0x00, 0x02, 0x3e, 0x01, slot] +
                         long2bytes(degrees) +
                         short2bytes(speed))
        #print ('[{}]'.format(', '.join(hex(x) for x in data)))
        self._write(data)

        if callback is None:
            rp.wait_blocking()

    # ff 55 07 00 02 3e 02 <slot> 64 00
    def set_encoder_motor_rotate(self, slot, speed, callback=None):
        assert slot == 1 or slot == 2, "Error, slot not defined"

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_ACK, timeout=0.1)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_ACK)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 0x07, 0x00, 0x02, 0x3e, 0x02, slot] +
                         short2bytes(speed))
        # print '[{}]'.format(', '.join(hex(x) for x in data))
        self._write(data)

        if callback is None:
            rp.wait_blocking()

    def set_command_until(self, command, degrees, speed, callback=None):
        # ff 55 0b 00 02 3e 05 <cmd> <4long degrees> <2short speed>
        commands = ["forward", "backward", "left", "right"]
        assert command in commands, "Error, %r command not in %r" % (command, str(commands))
        ind = 1 + commands.index(command)

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_ACK, timeout=2)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_ACK)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 0x0b, 0x00, 0x02, 0x3e, 0x05, ind] +
                         long2bytes(degrees) +
                         short2bytes(speed))

        # print '[{}]'.format(', '.join(hex(x) for x in data))
        self._write(data)

        if callback is None:
            rp.wait_blocking()

    def move_to(self, command, degrees, speed):
        """
        Execute the movement and return when finished
        :param command:
        :param degrees:
        :param speed:
        :param callback:
        :return:
        """
        self.set_command_until(command, degrees, speed, None)
        sleep(0.5)

        vel = 0.01
        # Espero a que termine de moverse
        while vel != 0:
            e1 = abs(self.get_encoder_motor_speed(1))
            e2 = abs(self.get_encoder_motor_speed(2))
            vel = e1 + e2 if e1 is not None and e2 is not None else 0.01
            sleep(0.1)

    def set_command(self, command, speed, callback=None):
        # ff 55 07 00 02 05 <2short speedleft> <2short speedright>
        commands = ["forward", "backward", "right", "left"]
        assert command in commands, "Error, %r command not in %r" % (command, str(commands))

        if command == "forward":
            speed_left = -speed
            speed_right = speed
        elif command == "backward":
            speed_left = speed
            speed_right = -speed
        elif command == "left":
            speed_left = -speed
            speed_right = -speed
        elif command == "right":
            speed_left = speed
            speed_right = speed
        else:
            assert True, "Error in set_command"

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_ACK, timeout=2)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_ACK)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 0x07, 0x00, 0x02, 0x5] +
                         short2bytes(speed_left) +
                         short2bytes(speed_right))

        # print '[{}]'.format(', '.join(hex(x) for x in data))
        self._write(data)

        if callback is None:
            rp.wait_blocking()

    # ff 55 06 00 01 3d 00 <slot> 01
    def get_encoder_motor_degrees(self, slot: object, callback: object = None) -> object:
        assert slot == 1 or slot == 2, "Error, slot not defined"

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_LONG, timeout=3)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_LONG)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 6, 0, 1, 0x3d, 0, slot, 1])
        # print '[{}]'.format(', '.join(hex(x) for x in data))
        self._write(data)

        if callback is None:
            rp.wait_blocking()

        return rp.response_event_data

    # ff 55 06 00 01 3d 00 <slot> 02
    def get_encoder_motor_speed(self, slot, callback=None):
        assert slot == 1 or slot == 2, "Error, slot not defined"

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_FLOAT, timeout=3)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_FLOAT)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 6, 0, 1, 0x3d, 0, slot, 2])
        # print '[{}]'.format(', '.join(hex(x) for x in data))
        self._write(data)

        if callback is None:
            rp.wait_blocking()

        return rp.response_event_data

    # ff 55 04 00 01 01 <port>
    def get_ultrasonic_reading(self, port, callback=None):

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_FLOAT, timeout=0.3)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_FLOAT)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 4, 0, 1, 1, port])
        self._write(data)

        if callback is None:
            rp.wait_blocking()

        return rp.response_event_data

    # ff 55 04 00 01 03 <port>
    def get_light_sensor(self, port, callback=None):

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_FLOAT, timeout=0.3)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_FLOAT)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 4, 0, 1, 3, port])
        self._write(data)

        if callback is None:
            rp.wait_blocking()

        return rp.response_event_data

    def get_light_sensor_onboard(self, port, callback=None):
        assert port == 1 or port == 2, "Error, port not defined"
        port = 0x0c if port == 1 else 0x0b
        return self.get_light_sensor(port, callback)

    # ff 55 04 00 01 07 <port>
    def get_sound_sensor(self, port, callback=None):

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_FLOAT, timeout=0.3)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_FLOAT)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 4, 0, 1, 7, port])
        self._write(data)

        if callback is None:
            rp.wait_blocking()

        return rp.response_event_data

    def get_sound_sensor_onboard(self, callback=None):
        port = 0x0e
        return self.get_light_sensor(port, callback)

    # ff 55 04 00 01 1b 0d
    def get_temperature_sensor_onboard(self, callback=None):

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_FLOAT, timeout=0.3)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_FLOAT)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 4, 0, 1, 0x1b, 0x0d])
        self._write(data)

        if callback is None:
            rp.wait_blocking()

        return rp.response_event_data

    # ff 55 04 00 01 11 <port>
    def get_line_sensor(self, port, callback=None):

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_FLOAT, timeout=0.3)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_FLOAT)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 4, 0, 1, 0x11, port])
        self._write(data)

        if callback is None:
            rp.wait_blocking()

        return rp.response_event_data

    # ff 55 04 00 01 1a <port>
    def get_compass_sensor(self, port, callback=None):

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_FLOAT, timeout=0.3)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_FLOAT)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 4, 0, 1, 0x1a, port])
        self._write(data)

        if callback is None:
            rp.wait_blocking()

        return rp.response_event_data



    # ff 55 05 00 01 06 01 <axis>
    def get_gyro_sensor_onboard(self, axis, callback=None):
        axis_opt = ["x", "y", "z"]
        assert axis in axis_opt, "Error, axis %r not defined in %r" % (axis, axis_opt)
        axis_ind = 1 + axis_opt.index(axis)

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_FLOAT, timeout=0.3)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_FLOAT)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 5, 0, 1, 6, 1, axis_ind])
        self._write(data)

        if callback is None:
            rp.wait_blocking()

        return rp.response_event_data

    # ff 55 04 00 01 0f <port>
    def get_pir_sensor(self, port, callback=None):

        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_FLOAT, timeout=0.3)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_FLOAT)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 4, 0, 1, 0x0f, port])
        self._write(data)

        if callback is None:
            rp.wait_blocking()

        return rp.response_event_data

    # ff 55 06 00 02 0b <port> <slot> <degrees>
    def set_servo_grades(self, port: object, slot: object, degrees: object, callback: object = None) -> object:
        assert slot == 1 or slot == 2, "Slot is not defined"
        assert degrees >= 0 or degrees <= 180, "Not possible degrees"


        if callback is None:
            rp = Response.generate_response_block(Frame.FRAME_TYPE_FLOAT, timeout=0.3)
        else:
            rp = Response.generate_response_async(callback, Frame.FRAME_TYPE_FLOAT)
        self.add_responder(rp)

        data = bytearray([0xff, 0x55, 6, 0, 2, 0x0b, port, slot]+long2bytes(degrees))
        self._write(data)

        if callback is None:
            rp.wait_blocking()

        return rp.response_event_data

    def gripper(self, command, port, slot):
        commands = ["open", "close"]
        assert command in commands, "Error, %r command not in %r" % (command, str(commands))
        assert slot == 1 or slot == 2, "Slot is not defined"

        if command == "open":
            degrees = 10
        elif command == "close":
            degrees = 90
        else:
            assert True, "Error in set_command"

        self.set_servo_grades(port = port, slot = slot, degrees =degrees)



    def close(self):

        print("Waiting 2 seconds to kill reader thread...")

        sleep(2)
        self.exiting = True

    def __del__(self):
        self.exiting = True
        self._serial.close()
