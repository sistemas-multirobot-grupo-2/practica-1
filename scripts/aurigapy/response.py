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
import threading


class Response:
    def __init__(self, timestamp, timeout, response_type, response_callback, response_event=None):
        self.timestamp = timestamp
        self.timeout = timeout
        self.response_type = response_type
        self.response_callback = response_callback
        self.response_event = response_event
        self.response_event_data = None

    @staticmethod
    def generate_response_async(callback, response_type, timeout=0.3):
        """

        :param callback: función con 2 parámetros (valor_respuesta, timeout). Timeout es true si se ha llamado
        por timeout y no por respuesta
        :param response_type:
        :param timeout:
        :return:
        """
        return Response(time.time(), timeout, response_type, callback, None)

    @staticmethod
    def generate_response_block(response_type, timeout=0.3):
        return Response(time.time(), timeout, response_type, None, threading.Event())

    def is_timeout(self):
        t_max = self.timestamp + self.timeout
        # print(self.timestamp, self.timeout, t_max,time.time())

        if t_max < time.time():
            return True
        else:
            return False

    def wait_blocking(self):
        assert self.response_event is not None, "Error, response is not blocking"
        self.response_event.wait()
