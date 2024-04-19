"""
Module handling the displaying.
"""

import cv2 as cv
import numpy as np


class Display:
    """
    Display class.
    """

    def __init__(self, window_name: str) -> None:
        cv.namedWindow(window_name)
        self._window_name = window_name

    def update_display(self, image: np.ndarray) -> None:
        """
        Function updating the display with the image for display.

        :param image: np.ndarray - image to display
        :return: None
        """
        cv.imshow(self._window_name, image)

    def get_window_name(self) -> str:
        """
        Returns the name of window.
        :return: str - window name.
        """
        return self._window_name
