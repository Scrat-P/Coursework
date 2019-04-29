import socket
from converter import Converter
from PIL import Image


TCP_IP = "127.0.0.1"
TCP_PORT = 5001


class Recipient:
    def __init__(self):
        self.tcp_ip = TCP_IP
        self.tcp_port = TCP_PORT

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.tcp_ip, self.tcp_port))
        self.server_socket.listen(1)

        self.client_socket, _ = self.server_socket.accept()

    def change_image(self, scale, contrast):
        self.scale = scale
        self.contrast = contrast

        return (Converter(self.img, self.scale, self.contrast)
                .convert()
                .resize((self.width, self.height), Image.LANCZOS))

    def call_save_as_image(self, img, width, height):
        self.img = Image.frombytes("RGB", (width, height), img)

        return (Converter(self.img, self.scale, self.contrast)
                .convert()
                .resize((width, height), Image.LANCZOS))

    def receive_images(self, scale, contrast):
        self.scale = scale
        self.contrast = contrast

        img = b''
        while True:
            temp = self.client_socket.recvfrom(65520)
            self.client_socket.sendto(bytearray("message", "utf-8"),
                                      (self.tcp_ip, self.tcp_port))

            condition = (
                all([temp[0][even] == 197 for even in range(0, 6, 2)]) and
                all([temp[0][odd] == 147 for odd in range(1, 6, 2)])
            )

            if temp[0] and condition:
                size = temp[0][6:]
                self.width, self.height = str(size, "utf-8").split(":")
                self.width, self.height = int(self.width), int(self.height)

                return self.call_save_as_image(img, self.width, self.height)
            else:
                img += temp[0]
