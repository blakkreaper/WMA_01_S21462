"""
This an example of object tracking (we are not expecting more than
one object on the same recording).
"""
from typing import Any

import cv2
import numpy as np


class Display:
    """
    Display class.
    """

    def __init__(self, window_name: str) -> None:
        cv2.namedWindow(window_name)
        self._window_name = window_name

    def update_display(self, image: np.ndarray[Any, Any]) -> None:
        """
        Function updating the display with the image for display.

        :param image: np.ndarray - image to display
        :return: None
        """
        cv2.imshow(self._window_name, image)

    def get_window_name(self) -> str:
        """
        Returns the name of window.
        :return: str - window name.
        """
        return self._window_name
