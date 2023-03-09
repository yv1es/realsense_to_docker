#!/usr/bin/python3


from numpysocket import NumpySocket
import numpy as np 
import cv2 
import socket

FRAME_HEIGHT = 480
FRAME_WIDTH = 640

HOST = socket.gethostname()  # as both code is running on same pc
PORT = 5000  # socket server port number

def server_program():
    

    server_socket = NumpySocket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((HOST, PORT))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen()
    conn, address = server_socket.accept()  # accept new connection
    # print("Connection from: " + str(address))
    
    # depth_bytes = conn.recv(2**26)
    color_image = conn.recv()

    # print(color_bytes.shape)
    # depth_image = np.frombuffer(depth_bytes, dtype=np.uint16)
    # depth_image.shape = (FRAME_HEIGHT, FRAME_WIDTH)

    # color_image = np.frombuffer(color_bytes, dtype=np.uint8)
    # color_image.shape = (FRAME_HEIGHT, FRAME_WIDTH, 3)

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
