import socket
import sys
import threading
import logging


class SocketThread(threading.Thread):
    def __init__(self, call_back_method, port=9100, host="localhost"):
        threading.Thread.__init__(self)
        self.HOST = host
        self.PORT = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.call_back_method = call_back_method
        self._stop_event = threading.Event()

    def stop(self):
        logging.info("Executed Stop")
        self._stop_event.set()
        self.s.close()
        logging.info("Done Executing Stop")

    def run(self):
        try:
            self.s.bind((self.HOST, self.PORT))

        except socket.error as msg:
            logging.error("Bind failed. Error Code : " + str(msg))
            sys.exit()

        logging.info("Socket bind complete")

        self.s.listen(1)
        self.s.settimeout(2)
        while not self._stop_event.is_set():
            try:
                conn, addr = self.s.accept()
            except socket.timeout:
                continue
            except OSError as e:
                if self._stop_event.is_set():
                    continue
                else:
                    raise e
            buff_size = 4096
            data = b''
            while True:
                part = conn.recv(buff_size)
                data += part
                if len (part) < buff_size:
                    break
            zpl_code = data.decode("utf-8").strip()
            self.call_back_method(self, zpl_code)
        logging.info("Socket closed")
