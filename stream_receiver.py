
import socket
from numpysocket import NumpySocket
import numpy as np 
import cv2


FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

HOST = socket.gethostname() 
PORT = 5000 




def setup_socket():
    socket = NumpySocket()  
    socket.bind((HOST, PORT)) 
    socket.listen()
    return socket 


def main():
    
    socket = setup_socket()
    conn, address = socket.accept()  
    print("Connected")

    cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
    
    while True:
        data = conn.recv()
        print("Received")

        if np.size(data) == 0:
            break
        
        
        
        
        cv2.imshow('Align Example', data)
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break

    print("Disconnected")
    conn.close()  # close the connection


if __name__=='__main__':
    main()