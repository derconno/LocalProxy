import sys
import socket
import threading


def transmit(s1: socket.socket, s2: socket.socket):
    while True:
        buf = s1.recv(1024)
        if len(buf) == 0:
            return
        try:
            s2.sendall(buf)
        except BrokenPipeError:
            return


def printHelp():
    print(f"{sys.argv[0]} <port1> <port2>")


def main(port1, port2):
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.bind(('', port1))
    s1.listen()
    (s1Client, address1) = s1.accept()
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind(('', port2))
    s2.listen()
    (s2Client, address2) = s2.accept()
    send = threading.Thread(target=transmit, args=(s1Client, s2Client))
    rcv = threading.Thread(target=transmit, args=(s2Client, s1Client))
    send.start()
    rcv.start()
    send.join()
    rcv.join()
    s1.close()
    s2.close()


if __name__ == '__main__':
    try:
        port1 = int(sys.argv[1])
        port2 = int(sys.argv[2])
        main(port1, port2)
    except IndexError:
        printHelp()
        sys.exit(1)
