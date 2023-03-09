
import socket
from numpysocket import NumpySocket
import numpy as np 
import cv2


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

    cv2.namedWindow('Color', cv2.WINDOW_NORMAL)

    while True:
        color = conn_c.recv()
        depth = conn_d.recv()

        if np.size(color) == 0 or np.size(depth) == 0:
            break
        
        cv2.imshow('Example', color)
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break

    conn_c.close() 
    conn_d.close()
    print("Disconnected")


if __name__=='__main__':
    main()