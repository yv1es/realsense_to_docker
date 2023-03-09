

import pyrealsense2 as rs
import numpy as np

from numpysocket import NumpySocket
import socket

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

HOST = socket.gethostname() 
PORT = 5000 



def setup_rl_pipeline():

    # Create a pipeline
    pipeline = rs.pipeline()

    # Create a config and configure the pipeline to stream
    #  different resolutions of color and depth streams
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

    # Start streaming
    profile = pipeline.start(config)
    return pipeline



def get_aligned_images(pipeline, align_obj):
    while True:
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = align_obj.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        return depth_image, color_image
        # Remove background - Set pixels further than clipping_distance to grey
        # grey_color = 153
        # depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        # bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)


def sender(data):

    
    client_socket = NumpySocket()  # instantiate
    client_socket.connect((HOST, PORT))  # connect to the server

    client_socket.sendall(data)  # send message

    client_socket.close()  # close the connection   


def main():
    
    # setup align object 
    align_to = rs.stream.color
    align_obj = rs.align(align_to)
    

    pipeline = setup_rl_pipeline()

    depth_image, color_image = get_aligned_images(pipeline, align_obj)

    # print(depth_image.shape)
    # print(color_image.shape)

    # sender(depth_image.tobytes())
    sender(color_image)

    pipeline.stop()



if __name__=='__main__':
    main()