import numpy as np
import cv2
import mediapipe as mp
import sys

BaseOptions = mp.tasks.BaseOptions
ImageSegmenterOptions = mp.tasks.vision.ImageSegmenterOptions
ImageSegmenter = mp.tasks.vision.ImageSegmenter

# Get the model file path
model_asset_path = 'data/selfie_segmenter.tflite'

# Create the options for image segmenter
base_options = BaseOptions(
    model_asset_path=model_asset_path
)

options = ImageSegmenterOptions(
    base_options=base_options,
    output_category_mask=True
)

# Create the image segmenter
segmenter = ImageSegmenter.create_from_options(options)


frame_size = None
bg_image = None
bg_video = None


# Function to segment the image
def get_image_mask(image):

    # Create the MediaPipe image that will be segmented
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

    # Retrieve the masks for the segmented image
    segmentation_result = segmenter.segment(mp_image)
    mp_mask = segmentation_result.category_mask

    mask = mp_mask.numpy_view()
    mask = np.dstack((mask,)*3)

    return mask


def hq_cam(frame):
    return frame


# Blur the image background
def blur_bg(frame):

    # Get the segmented mask
    mask = get_image_mask(frame)

    # Blur the background based on segmented mask
    bg_image = cv2.GaussianBlur(frame, (25, 25), 100)
    image = np.where(mask == 0, frame, bg_image)

    return image


# initialize background image
def init_image(image_path):
    global bg_image

    bg_image = cv2.imread(image_path)
    if bg_image is None:
        sys.exit('Error opening image file')


# Replace the background with an image
def replace_with_image(frame):
    global bg_image

    # Get the segmented mask
    mask = get_image_mask(frame)

    bg_image = cv2.resize(bg_image, frame_size)

    # Replace the background based on segmented mask
    image = np.where(mask == 0, frame, bg_image)

    return image


# Initialize background video
def init_video(video_path):
    global bg_video

    bg_video = cv2.VideoCapture(video_path)

    if bg_video.isOpened() == False:
        sys.exit('Error opening video file')


# Replace the background with a video
def replace_with_video(fg_frame):
    global bg_video

    ret, bg_frame = bg_video.read()
    if ret == False:
        bg_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, bg_frame = bg_video.read()

    bg_frame = cv2.resize(bg_frame, frame_size)

    # Get the segmented mask
    mask = get_image_mask(fg_frame)

    # Replace the background based on segmented mask
    image = np.where(mask == 0, fg_frame, bg_frame)

    return image
