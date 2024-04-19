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

    def __init__(self, video_path: str, tracked_color: None | tuple[int,int,int]= None) -> None:
        self._video = cv2.VideoCapture(video_path)
        if not self._video.isOpened():
            raise ValueError(f'Unable to open video at path {video_path}')
        self._frame: None | np.ndarray = None
        self._tracked_colors = tracked_color
        self._processed_frame: None | np.ndarray = None
        self._processing_type: ProcessingType = ProcessingType.RAW

    def set_processing_type(self, p_type: ProcessingType) -> None:
        self._processing_type = p_type

    def set_reference_color_by_position(self, x: int, y: int) -> None:
        hsv_frame: np.ndarray = cv2.cvtColor(self._frame, cv2.COLOR_RGB2HSV)
        self._tracked_color = hsv_frame[y, x, :]

    def update_frame(self) -> bool:
        """
        Function that updates the frame variable.
        :return: bool - info whether it was successful or not
        """
        read_successful, self._frame = self._video.read()
        if read_successful:
            self._process_frame()
        return read_successful

    def create_mask(self):
        if self._tracked_color is not None:
            # Zakładamy, że _tracked_color jest listą lub krotką trzech elementów HSV
            hue, saturation, value = self._tracked_color
            lower_bound = np.array([hue - 10, max(saturation - 40, 100), max(value - 40, 100)])
            upper_bound = np.array([hue + 10, min(saturation + 40, 255), min(value + 40, 255)])
            mask = cv2.inRange(cv2.cvtColor(self._frame, cv2.COLOR_BGR2HSV), lower_bound, upper_bound)
            return mask
        return None

    def _process_frame(self):
        if self._processing_type == ProcessingType.TRACKER:
            # Utwórz maskę dla wybranego koloru
            mask = self.create_mask()
            if mask is not None:
                # Znajdź kontury na masce
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    # Znajdź największy kontur i narysuj wokół niego prostokąt
                    largest_contour = max(contours, key=cv2.contourArea)
                    if cv2.contourArea(largest_contour) > 100:  # Próg wielkości konturu
                        x, y, w, h = cv2.boundingRect(largest_contour)
                        cv2.rectangle(self._frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(self._frame, "Sledzenie aktywne", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                    (0, 255, 0), 2)
                self._processed_frame = self._frame

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

