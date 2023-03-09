import pyrealsense2 as rs
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
    socket_c = NumpySocket()  # instantiate
    socket_c.connect((HOST, PORT_C))  # connect to the server

    socket_d = NumpySocket()  # instantiate
    socket_d.connect((HOST, PORT_D))  # connect to the server
    return socket_c, socket_d


def setup_realsense():
    pipeline = rs.pipeline()

    config = rs.config()

    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break
    if not found_rgb:
        print("The demo requires Depth camera with Color sensor")
        exit(0)


    config.enable_stream(rs.stream.depth, FRAME_WIDTH, FRAME_HEIGHT,  rs.format.z16, FPS)
    config.enable_stream(rs.stream.color, FRAME_WIDTH, FRAME_HEIGHT, rs.format.bgr8, FPS)

    profile = pipeline.start(config)
    return pipeline



def main():

    print("Setting up RealSense")
    pipeline = setup_realsense()

    print("Connecting to receiver")
    socket_c, socket_d = setup_sockets()
    
    # setup aligner
    align_to = rs.stream.color
    aligner = rs.align(align_to)

    print("Connected, starting stream")
    try:
        while True:
            # Get frameset of color and depth
            frames = pipeline.wait_for_frames()
            # frames.get_depth_frame() is a 640x360 depth image

            # Align the depth frame to color frame
            aligned_frames = aligner.process(frames)

            # Get aligned frames
            aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
            color_frame = aligned_frames.get_color_frame()

            # Validate that both frames are valid
            if not aligned_depth_frame or not color_frame:
                continue

            depth_image = np.asanyarray(aligned_depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            socket_c.sendall(color_image)
            socket_d.sendall(depth_image)

    finally:
        socket_c.close()
        socket_d.close()
        pipeline.stop()
        print("Disconnected")



if __name__=='__main__':
    main()