"""
This an example of object tracking (we are not expecting more than
one object on the same recording).
"""
from typing import Any

import cv2

from color_tracking.color_tracker import ColorTracker
from color_tracking.display import Display
from color_tracking.processing_type import ProcessingType


class EventHandler:
    """
    Class for handling the events like key click etc.
    """

    PROCESSING_TYPE_KEYMAP = {
        ord('h'): ProcessingType.HUE,
        ord('s'): ProcessingType.SATURATION,
        ord('v'): ProcessingType.VALUE,
        ord('r'): ProcessingType.RAW,
        ord('t'): ProcessingType.TRACKER
    }

    def __init__(self, tracker: ColorTracker, display: Display, timeout: int) -> None:
        self._window_name = display.get_window_name()
        self._tracker = tracker
        self._timeout = timeout
        cv2.setMouseCallback(self._window_name, self.handle_mouse)

    def _handle_keys(self) -> bool:
        """
        Function for handling key mapping.
        :return: bool - info if the proper key has been used.
        """
        keycode = cv2.waitKey(self._timeout)
        if keycode == ord('q') or keycode == 27:
            return False

        if keycode in EventHandler.PROCESSING_TYPE_KEYMAP.keys():
            self._tracker.set_processing_type(EventHandler.PROCESSING_TYPE_KEYMAP[keycode])
        return True

    def handle_events(self) -> bool:
        """
        Function for event handling.
        :return: bool - info if we used the proper key.
        """
        return self._handle_keys()

    def handle_mouse(self, event: int, x: int, y: int, flags: int, param: Any) -> None:
        """
        Handles mouse events, specifically left button clicks to set the reference color
        for tracking based on the mouse's position on the image.

        :param event: int - Integer representing the type of mouse event (e.g., cv2.EVENT_LBUTTONDOWN).
        :param x: int - The x-coordinate of the mouse event.
        :param y: int - The y-coordinate of the mouse event.
        :param flags: int - Special flags passed with the event.
        :param param: Any - Additional parameter passed through the callback.
        :return: None
        """
        if (event == cv2.EVENT_LBUTTONDOWN and
                self._tracker.get_processing_type() == ProcessingType.TRACKER):
            self._tracker.set_reference_color_by_position(x, y)
