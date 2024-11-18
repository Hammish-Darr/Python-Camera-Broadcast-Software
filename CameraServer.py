import socket, pickle, cv2, base64
from threading import Thread


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '0.0.0.0'
print("IP of host: ", host_ip, ", host name: ", host_name)
port = 9999
sock_address = (host_ip, port)
sock.bind(sock_address)
client_dict = {}
client_list = []

client_sock = ""

camera_capture = cv2.VideoCapture(0)

def send_input (client = client_sock, client_list = client_list):

    while True:
        ret, frame = camera_capture.read()
        #cv2.imshow("frame", frame)
        #cv2.waitKey(1)
        message = base64.b64encode(pickle.dumps(frame)).decode('ascii')
        message = message + "|"
        b = message.encode('utf-8')

        for i in client_list:
            i.sendall(b)


send1 = Thread(target=send_input, args=())
send1.daemon = True



print('Socket Successfully Bound')

sock.listen(10)

count = 0
while True:

    sock.listen(10)     

    client_sock, address = sock.accept()
    client_dict[client_sock] = address[0]
    client_list.append(client_sock)
    print("Client " + str(address[0]) + " connected.")
    print("Number of active connections: " + str(len(client_list)) + ".")
    if count == 0:
        send1.start()
        count += 1

