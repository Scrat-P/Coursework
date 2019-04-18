import socket


def get_img():
    from PIL import Image

    roiImg = Image.new("RGB", [10, 10], "red")

    image = roiImg.tobytes()

    return image


UDP_IP = "127.0.0.1"
UDP_PORT = 5006

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((UDP_IP, UDP_PORT))
size = 1024

while True:
    temp = client_socket.recvfrom(1024)
    data = temp[0].decode("utf-8")
    print("The following data was received - ", data)
    print("Opening file - ", data)
    img = get_img()

    for i in range(round(len(img) / 64)):
        part_img = img[i * 64:(i + 1) * 64]
        print(i)
        if not img:
            break
        client_socket.sendto(img, (UDP_IP, UDP_PORT))
    print("Data sent successfully")
    exit()
