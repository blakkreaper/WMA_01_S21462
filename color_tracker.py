"""
This an example of object tracking (we are not expecting more than
one object on the same recording).
"""


import cv2
import numpy as np
import random as rng

from processing_type import ProcessingType


class ColorTracker:
    """
    Class that will handle color tracking.
    """

    def __init__(self, video_path: str) -> None:
        self._video = cv2.VideoCapture(video_path)
        if not self._video.isOpened():
            raise ValueError(f'Unable to open video at path {video_path}')
        self._frame: None | np.ndarray = None
        self._tracked_colors = []
        self._processed_frame: None | np.ndarray = None
        self._processing_type: ProcessingType = ProcessingType.RAW

    def set_processing_type(self, p_type: ProcessingType) -> None:
        self._processing_type = p_type

    def set_reference_color_by_position(self, x: int, y: int) -> None:
        """
        Function that gets the color in RGB from the position on video and append it to list of
        tracked colors. If the list is overloaded it is cleared.
        :param x: int - X color coordinate
        :param y: int - Y color coordinate
        :return: None
        """
        if len(self._tracked_colors) < 3:  # Limit to 3 tracked colors
            hsv_frame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2HSV)
            self._tracked_colors.append((hsv_frame[y, x, 0], hsv_frame[y, x, 1], hsv_frame[y, x, 2]))
        else:
            self._tracked_colors.clear()

    def update_frame(self) -> bool:
        """
        Function that updates the frame variable.
        :return: bool - info whether it was successful or not
        """
        read_successful, self._frame = self._video.read()
        if read_successful:
            self._process_frame()
        return read_successful

    def _process_frame(self):
        """
        Function that processes the frame in a way depending on
        :return:
        """
        for idx, color in enumerate(self._tracked_colors):
            hue, sat, val = color
            lower_bound = np.array([hue - 10, sat - 40, val - 40])
            upper_bound = np.array([hue + 10, sat + 40, val + 40])
            mask = cv2.inRange(cv2.cvtColor(self._frame, cv2.COLOR_BGR2HSV), lower_bound, upper_bound)
            # Erozja i dylatacja
            mask = cv2.erode(mask, None, iterations=5)
            mask = cv2.dilate(mask, None, iterations=5)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) > 100:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(self._frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(self._frame, f"Object_{idx+1}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    def get_frame(self) -> np.ndarray:
        """
        Get the copy of frame variable value.
        :return: np.ndarray - current frame.
        """
        if self._frame is None:
            raise ValueError('Attempted to get frame from uninitialized color.')
        return self._frame.copy()

    def get_processed_frame(self) -> np.ndarray:
        """
        Get the current processed frame.
        :return: np.ndarray - current from that is processed
        """
        if self._processed_frame is None:
            return self.get_frame()
        return self._processed_frame.copy()

