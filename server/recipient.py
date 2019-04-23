import socket
from converter import Converter


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

    def call_save_as_image(self, img, width, height):
        from PIL import Image

        image = Image.frombytes("RGB", (width, height), img)

        return Converter(image).convert()

    def receive_images(self):
        img = b''
        while True:
            temp = self.client_socket.recvfrom(65520)
            self.client_socket.sendto(bytearray("message", "utf-8"), (self.tcp_ip, self.tcp_port))
            if temp[0] and temp[0][0] == 197 and temp[0][1] == 147 and temp[0][2] == 197 and temp[0][3] == 147 and temp[0][4] == 197 and temp[0][5] == 147:
                size = temp[0][6:]
                width, height = str(size, "utf-8").split(":")
                width, height = int(width), int(height)

                return self.call_save_as_image(img, width, height)
            else:
                img += temp[0]
