
from acomms.modem_connections import ModemConnection
from time import sleep
from threading import Thread

import socket

class UdpConnection(ModemConnection):

    def __init__(self, modem, remote_host, remote_port, local_host=None, local_port=None, timeout=0.1):
        self._incoming_line_buffer = ""

        self.connection_type = "udp"

        self.modem = modem
        self.timeout = timeout

        self._remote_host = remote_host
        self._remote_port = remote_port

        if local_host is None:
            self._local_host = ""
        else:
            self._local_host = local_host

        if local_port is None:
            self._local_port = remote_port
        else:
            self._local_port = local_port

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind((self._local_host, self._local_port))

        self._listen_thread = Thread(target=self._listen)
        self._listen_thread.setDaemon(True)
        self._listen_thread.start()

        self._send_thread = Thread(target=self._send)
        self._send_thread.setDaemon(True)
        self._send_thread.start()

    @property
    def is_connected(self):
        return True # UDP is connectionless...

    @property
    def can_change_baudrate(self):
        return False

    def change_baudrate(self,baudrate):
        return None


    def close(self):
        self._thread.stop()

    def _listen(self):
        while True:
            msg_lines = self.readlines()
            # We are connected, so pass through to NMEA
            if msg_lines:
                for line in msg_lines:
                    self.modem._process_incoming_nmea(line)
            self.modem._process_outgoing_nmea()

    def _send(self):
        while True:
            self.modem._process_outgoing_nmea()
            sleep(0.05)

    def readlines(self):
        """Returns a \n terminated line from the modem.  Only returns complete lines (or None on timeout)"""
        rl = self._socket.recv(1024)

        if rl == "":
            return None

        try:
            self._incoming_line_buffer += rl.decode('ascii')
        except UnicodeDecodeError:
            self.modem._daemon_log.warn("Error decoding incoming UDP stream, likely corruption")
            return None

        # Make sure we got a complete line.  Serial.readline may return data on timeout.
        if '\n' in self._incoming_line_buffer:
            # is there a newline at the end?
            lines = self._incoming_line_buffer.splitlines(True)
            # See if the last line has a newline at the end.
            if lines[-1][-1] != '\n':
                self._incoming_line_buffer = lines[-1]
                lines.pop() # remove it from the list to passed on
            else:
                self._incoming_line_buffer = ''
            # return the list of complete lines
            return lines
        else:
            return None

    def write(self, data):
        if type(data) == str:
            data = data.encode('ascii')
        self._socket.sendto(data, (self._remote_host, self._remote_port))

    def __repr__(self):
        return "UDPConnection: remote_host={} remote_port={} local_host={} local_port={}".format(self._remote_host,
                                                                                                 self._remote_port,
                                                                                                 self._local_host,
                                                                                                 self._local_port)
