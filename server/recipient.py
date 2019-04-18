import socket


def call_save_as_image(fname, img, width, height):
    from PIL import Image

    image = Image.frombytes("RGB", (width, height), img)
    with open(fname + ".png", "wb") as file:
        image.save(file)

UDP_IP = "127.0.0.1"
UDP_PORT = 5001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((UDP_IP, UDP_PORT))
server_socket.listen(1)

client_socket, address = server_socket.accept()

while True:
    fname = "picture"
    img = b''
    while True:
        temp = client_socket.recvfrom(512)
        client_socket.sendto(bytearray("message", "utf-8"), (UDP_IP, UDP_PORT))
        if temp[0] and temp[0][0] == 35:
            print(len(img))
            size = temp[0][1:]
            width, height = str(size, "utf-8").split(":")
            width, height = int(width), int(height)
            print(width, height)
            call_save_as_image(fname, img, width, height)
            img = b''
            fname = "1"
        else:
            img += temp[0]
        
    exit()
