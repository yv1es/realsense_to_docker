from numpysocket import NumpySocket
import numpy as np 
import cv2 
import socket

FRAME_HEIGHT = 480
FRAME_WIDTH = 640

HOST = socket.gethostname()  
PORT = 5000 

def server_program():
    

    server_socket = NumpySocket()  
    server_socket.bind((HOST, PORT)) 

    server_socket.listen()
    conn, address = server_socket.accept()  # accept new connection

    color_image = conn.recv()


    cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
    cv2.imshow('Align Example', color_image)
    while True:
        cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
        cv2.imshow('Align Example', color_image)
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
