import socket, time, threading, pickle, cv2, base64
from threading import Thread

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "192.168.9.12"
host_port = 9999

image_data = ""

print("Initiating connection")

def connect_to_host():
    connection_attempt_count = 1
    while True:

        try:
            sock.connect((host_ip, host_port))
            print("Connection Successful")
            break
        except:
            connection_attempt_count += 1
            print("Previous attempt unsuccessful. Initiating attempt number " + str(connection_attempt_count) + ".")
connect_to_host()



def receive_input (image_data = image_data):
    while True:

        data = sock.recv(1024)
        if data:
            decoded_data = data.decode('utf-8')
            decoded_data_list = decoded_data.split("|")
            if len(decoded_data_list) == 2:

                image_data += decoded_data_list[0]
                
                frame = pickle.loads(base64.b64decode(image_data))
                cv2.imshow("frame", frame)
                cv2.waitKey(1)
                image_data = decoded_data_list[1]
            elif decoded_data[0] == "|":
                frame = pickle.loads(base64.b64decode(image_data))
                cv2.imshow("frame", frame)
                cv2.waitKey(1)
                image_data = decoded_data_list[0]
            elif decoded_data[(len(decoded_data) - 1)] == "|":
                image_data += decoded_data_list[0]
                frame = pickle.loads(base64.b64decode(image_data))
                cv2.imshow("frame", frame)
                cv2.waitKey(1)
                image_data = ""
            else:
                image_data += decoded_data


            

receive1 = threading.Thread(target=receive_input, args=())
receive1.daemon = True

receive1.start() 
while True:
    time.sleep(1)
