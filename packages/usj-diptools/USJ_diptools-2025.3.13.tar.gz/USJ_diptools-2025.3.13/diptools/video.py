"""
-----------------------------------------------------------------------------------------
video module
-----------------------------------------------------------------------------------------
Provides basic video loading tools. 
"""

import os

import cv2 as cv
import numpy as np

def play_video(file_name: str) -> None:
    """Play videos with Open-CV

    Suppported formats: .avi
    Unsupported formats: .mov

    Args:
        fileName (str): Path to the file to be loaded.

    Raises:
        Exception: Errors related with file loading
    """
    _, ext = os.path.splitext(file_name)

    if ext != ".mov":  # Mov files give problems

        video = cv.VideoCapture(file_name)
        if not video.isOpened():
            raise Exception("Error loading file.")

        frameCount = int(video.get(cv.CAP_PROP_FRAME_COUNT))
        fps = int(video.get(cv.CAP_PROP_FPS))

        f = 0
        ret = True
        while f < frameCount and ret:
            ret, frame = video.read()
            if not ret:
                raise Exception("Error loading file.")

            cv.imshow("frame", frame)
            f += 1

            cv.waitKey(int(np.round(1e3 / fps)))

        video.release()
        cv.destroyAllWindows()
    else:
        raise Exception("%s format cannot be played" % ext)
    
def extract_video(file_name: str, resize: int = 1) -> tuple[np.ndarray, int]:
    """Extract videos with Open-CV and NumPy

    Suppported formats: .avi
    Unsupported formats: .mov

    Args:
        fileName (str): Path to the file to be loaded.

        resize (int, optional): Factor (>1) for resizing the video output.
        Defaults to 1 (no resizing).

    Raises:
        Exception: Errors related with file loading

    Returns:
        tuple[np.ndarray,int]: Results tuple:
            buf (element 0 np.ndarray): 4-dimensional array including the video.
            fps (element 1 int): Frames per second of the exported video.
    """
    _, ext = os.path.splitext(file_name)

    if ext != ".mov":  # Mov files give problems

        video = cv.VideoCapture(file_name)
        if not video.isOpened():
            raise Exception("Error loading file.")

        frameCount = int(video.get(cv.CAP_PROP_FRAME_COUNT))
        frameWidth = int(video.get(cv.CAP_PROP_FRAME_WIDTH)) // resize
        frameHeight = int(video.get(cv.CAP_PROP_FRAME_HEIGHT)) // resize
        fps = int(video.get(cv.CAP_PROP_FPS))

        buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype("uint8"))

        ret = True
        frame = 0
        while frame < frameCount and ret:
            ret, image = video.read()
            if not ret:
                raise Exception("Error loading file.")

            buf[frame] = cv.resize(
                cv.cvtColor(image, cv.COLOR_BGR2RGB), (frameWidth, frameHeight)
            )
            frame += 1

        video.release()
    else:
        raise Exception("%s format cannot be read." % ext)

    return (buf, fps)