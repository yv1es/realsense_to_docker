
import socket
from numpysocket import NumpySocket
import numpy as np 


FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

HOST = socket.gethostname() 
PORT_C = 5000 
PORT_D = 5001


def setup_sockets():
    socket_c = NumpySocket()  
    socket_c.bind((HOST, PORT_C)) 
    socket_c.listen()

    socket_d = NumpySocket()  
    socket_d.bind((HOST, PORT_D)) 
    socket_d.listen()

    return socket_c, socket_d



def main():
    print("Listening for connections")
    socket_c, socket_d = setup_sockets()
    conn_c, address = socket_c.accept()
    conn_d, address = socket_d.accept()  
    print("Connected")

    while True:
        color = conn_c.recv()
        depth = conn_d.recv()

        if np.size(color) == 0 or np.size(depth) == 0:
            break
        
        # do whatever with color and depth
        print(color.shape)
        print(depth.shape)

    conn_c.close() 
    conn_d.close()
    print("Disconnected")


if __name__=='__main__':
    main()