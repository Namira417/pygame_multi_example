import socket
from _thread import *
import sys

server = "192.168.219.182"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(6)  # enable 2 people to connect server
print("Waiting for a connection, Server Started")


# 하나의 명령어를 계속 기다려서 순차적으로 하기 보다는
# 스레드를 사용하여 동시에 주고 받게 한다.
def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)  # 2048비트는 받을 데이터량
            reply = data.decode("UTF-8")  # 받은 데이터를 우리가 읽는 방식은 UTF-8로 해독

            if not data:
                print("Disconnected")
                break
            else:
                print("Recieved: ", reply)
                print("Sending: ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()  # accept any incoming connection
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, ))
