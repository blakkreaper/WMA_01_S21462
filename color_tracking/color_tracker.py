"""
This an example of object tracking (we are not expecting more than
one object on the same recording).
"""
from typing import Any

import cv2
import numpy as np


from .processing_type import ProcessingType


class ColorTracker:
    """
    Class that will handle color tracking.
    """

    def __init__(self, video_path: str) -> None:
        self._video = cv2.VideoCapture(video_path)
        if not self._video.isOpened():
            raise ValueError(f'Unable to open video at path {video_path}')
        self._frame: None | np.ndarray[Any, Any] = None
        self._tracked_colors: list[tuple[np.ndarray[Any, Any], np.ndarray[Any, Any], np.ndarray[Any, Any]]] = []
        self._processed_frame: None | np.ndarray[Any, Any] = None
        self._processing_type: ProcessingType = ProcessingType.RAW

    def _process_frame(self) -> None:
        """
        Function that processes the frame in a way depending on
        :return: None
        """
        if self._frame is None:
            return
        hsv_frame: np.ndarray[Any, Any]

        if self._processing_type == ProcessingType.TRACKER:
            self._frame = self._create_tracker_for_object(self._frame)
        elif self._processing_type == ProcessingType.HUE:
            hsv_frame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2HSV)
            self._frame = hsv_frame[:,:,0]
        elif self._processing_type == ProcessingType.SATURATION:
            hsv_frame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2HSV)
            self._frame = hsv_frame[:, :, 1]
        elif self._processing_type == ProcessingType.VALUE:
            hsv_frame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2HSV)
            self._frame = hsv_frame[:, :, 2]

    def _create_tracker_for_object(self, frame: np.ndarray[Any, Any]) -> np.ndarray[Any, Any]:
        """
        Creates tracker for all to be tracked colors on the list with rectangles.
        :param frame: np.ndarray - array of bytes representing frame
        :return: np.ndarray - frame after creation of masks.
        """
        # Definicja kernela
        kernel_size = (5, 5)  # Rozmiar kernela; można dostosować do potrzeb
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)

        for idx, color in enumerate(self._tracked_colors):
            # hue, saturation, value
            lower_bound = np.array([color[0] - 10, color[1] - 40, color[2] - 40])
            upper_bound = np.array([color[0] + 10, color[1] + 40, color[2] + 40])
            mask = cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), lower_bound, upper_bound)
            # Erozja i dylatacja
            mask = cv2.erode(mask, kernel, iterations=2)
            mask = cv2.dilate(mask, kernel, iterations=2)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) > 100:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f"Obiekt_{idx + 1}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (0, 255, 0), 2)
        return frame

    def update_frame(self) -> bool:
        """
        Function that updates the frame variable.
        :return: bool - info whether it was successful or not
        """
        read_successful, self._frame = self._video.read()
        if read_successful:
            self._process_frame()
        return read_successful

    def set_processing_type(self, p_type: ProcessingType) -> None:
        """
        Set processing type for the process to be done.
        :param p_type: Enum - processing type from class ProcessingType.
        :return: None
        """
        self._processing_type = p_type

    def set_reference_color_by_position(self, x: int, y: int) -> None:
        """
        Function that gets the color in RGB from the position on video and append it to list of
        tracked colors. If the list is overloaded it is cleared.
        :param x: int - X color coordinate
        :param y: int - Y color coordinate
        :return: None
        """
        if self._frame is None:
            return

        if len(self._tracked_colors) < 4:
            hsv_frame: np.ndarray[Any, Any] = cv2.cvtColor(self._frame, cv2.COLOR_BGR2HSV)
            self._tracked_colors.append((hsv_frame[y, x, 0],
                                         hsv_frame[y, x, 1],
                                         hsv_frame[y, x, 2])
                                        )
        else:
            self._tracked_colors.clear()

    def get_processing_type(self) -> ProcessingType:
        """
        Get processing type for the process to be done.
        :return: ProcessingType - enum class value.
        """
        return self._processing_type

    def get_frame(self) -> np.ndarray[Any, Any]:
        """
        Get the copy of frame variable value.
        :return: np.ndarray - current frame.
        """
        if self._frame is None:
            raise ValueError('Attempted to get frame from uninitialized color.')
        return self._frame.copy()

    def get_processed_frame(self) -> np.ndarray[Any, Any]:
        """
        Get the current processed frame.
        :return: np.ndarray - current from that is processed
        """

        if self._processed_frame is None:
            return self.get_frame()
        return self._processed_frame.copy()
