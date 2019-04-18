import socket


def call_save_as_image(fname, img):
    from PIL import Image

    image = Image.frombytes("RGB", (10, 10), img)
    with open(fname + ".png", "wb") as file:
        image.save(file)

UDP_IP = "127.0.0.1"
UDP_PORT = 5006

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((UDP_IP, UDP_PORT))
server_socket.listen(1)

client_socket, address = server_socket.accept()

while True:
    fname = "picture"
    client_socket.sendto(bytearray(fname, "utf-8"), (UDP_IP, UDP_PORT))
    img = b''
    while True:
        temp = client_socket.recvfrom(512)
        print(temp)
        if not temp[0]:
            break

        img += temp[0]
        
    call_save_as_image(fname, img)
    print("Data Received successfully")
    exit()
