import socket
import numpy as np 
import cv2 

FRAME_HEIGHT = 480
FRAME_WIDTH = 640


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    
    # depth_bytes = conn.recv(2**26)
    color_bytes = conn.recv(2**30)

    # depth_image = np.frombuffer(depth_bytes, dtype=np.uint16)
    # depth_image.shape = (FRAME_HEIGHT, FRAME_WIDTH)

    color_image = np.frombuffer(color_bytes, dtype=np.uint8)
    color_image.shape = (FRAME_HEIGHT, FRAME_WIDTH, 3)

    cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
    cv2.imshow('Align Example', color_image)

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()