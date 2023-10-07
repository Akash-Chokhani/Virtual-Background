import numpy as np
import cv2
import time
import utils


cam = None
func = None
height = None
width = None


# Determine the camera function
def cam_function(config):
    global func

    if 'blur' in config:
        func = utils.blur_bg

    elif 'image' in config:
        utils.init_image(config['image'])
        func = utils.replace_with_image

    elif 'video' in config:
        utils.init_video(config['video'])
        func = utils.replace_with_video

    else:
        func = utils.hq_cam


# Webcam settings
def cam_setings():
    global cam, height, width

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FPS, 30)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))

    cv2.namedWindow('My Cam', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('My Cam', 600, 600)


def play(config):
    global cam, func, width, height

    cam_function(config)
    cam_setings()

    utils.frame_size = (height, height)

    left_offset = (width-height)//2
    right_offset = (width+height)//2

    cur_time = int(time.monotonic())
    no_of_frames = 0

    while (cam.isOpened()):

        ret, frame = cam.read()
        frame = frame[:, left_offset: right_offset]
        frame = cv2.flip(frame, 1)

        # Get the modified frame
        frame = func(frame)

        cv2.imshow('My Cam', frame)
        if cv2.waitKey(1) == ord('q'):
            break

        # Compute the fps
        no_of_frames += 1
        if cur_time < int(time.monotonic()):
            print('fps:', no_of_frames, '\t', end='\r')
            no_of_frames = 0
            cur_time += 1

    cam.release()
    cv2.destroyAllWindows()
