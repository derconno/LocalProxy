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
    print(f"{sys.argv[0]} <host1> <port1> <host2> <port2>")


def main(host1, port1, host2, port2):
    s1 = socket.create_connection((host1, port1))
    s2 = socket.create_connection((host2, port2))
    send = threading.Thread(target=transmit, args=(s1, s2))
    rcv = threading.Thread(target=transmit, args=(s2, s1))
    send.start()
    rcv.start()
    send.join()
    rcv.join()
    s1.close()
    s2.close()


if __name__ == '__main__':
    try:
        host1 = sys.argv[1]
        port1 = int(sys.argv[2])
        host2 = sys.argv[3]
        port2 = int(sys.argv[4])
        main(host1, port1, host2, port2)
    except IndexError:
        printHelp()
        sys.exit(1)
    except ConnectionRefusedError:
        print("Could not connect, are you sure both Services are running and reachable?")
        sys.exit(2)
