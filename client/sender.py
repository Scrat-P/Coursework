import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 5001

class Sender:
    def __init__(self):
        self.tcp_ip = TCP_IP
        self.tcp_port = TCP_PORT

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.tcp_ip, self.tcp_port))


    def convert_to_bytes(self, img):
        return img.tobytes()


    def send_image(self, canvas, width, height):
        img = self.convert_to_bytes(canvas)

        for i in range(round(len(img) / 64) + 2):
            part_img = img[i * 64:(i + 1) * 64]
            self.client_socket.sendto(part_img, (self.tcp_ip, self.tcp_port))
            if not part_img:
                self.client_socket.sendto(bytearray(f"#{width}:{height}", "utf-8"), (self.tcp_ip, self.tcp_port))
                self.client_socket.recvfrom(1000)

                break
            self.client_socket.recvfrom(1000)
