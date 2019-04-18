import socket


def get_img_1():
    from PIL import Image

    roiImg = Image.new("RGB", [5, 5], "red")

    image = roiImg.tobytes()

    return image


def get_img_2():
    from PIL import Image

    roiImg = Image.new("RGB", [5, 5], "blue")

    image = roiImg.tobytes()

    return image


UDP_IP = "127.0.0.1"
UDP_PORT = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((UDP_IP, UDP_PORT))
size = 1024

def test(img):
    for i in range(round(len(img) / 64) + 2):
        part_img = img[i * 64:(i + 1) * 64]
        client_socket.sendto(part_img, (UDP_IP, UDP_PORT))
        if not part_img:
            client_socket.sendto(bytearray("#5:5", "utf-8"), (UDP_IP, UDP_PORT))
            client_socket.recvfrom(1000)
            break
        client_socket.recvfrom(1000)

test(get_img_1())
test(get_img_2())