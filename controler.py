"""
Module for event handling.
"""

import cv2

from color_tracker import ColorTracker
from display import Display
from processing_type import ProcessingType


class EventHandler:
    """
    Class for handling the events like key click etc.
    """

    PROCESSING_TYPE_KEYMAP = {
        ord('h'): ProcessingType.HUE,
        ord('s'): ProcessingType.SATURATION,
        ord('v'): ProcessingType.VALUE,
        ord('r'): ProcessingType.RAW
    }

    def __init__(self, tracker: ColorTracker, display: Display, timeout: int) -> None:
        self._window_name = display.get_window_name()
        self._tracker = tracker
        self._timeout = timeout
        cv2.setMouseCallback(self._window_name, self._handle_mouse)

    def _handle_keys(self) -> bool:
        """
        Function for handling key mapping.
        :return: bool - info if the proper key has been used.
        """
        keycode = cv2.waitKey(self._timeout)
        if keycode == ord('q') or keycode == 27:
            return False
        elif keycode in EventHandler.PROCESSING_TYPE_KEYMAP.keys():
            self._tracker.set_processing_type(EventHandler.PROCESSING_TYPE_KEYMAP[keycode])
        return True

    def handle_events(self) -> bool:
        """
        Function for event handling.
        :return: bool - info if we used the proper key.
        """
        return self._handle_keys()

    def _handle_mouse(self, event, x, y, flags, param) -> None:
        if event == cv2.EVENT_LBUTTONDOWN:
            self._tracker.set_reference_color_by_position(x, y)


