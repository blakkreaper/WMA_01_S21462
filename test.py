import cv2
import numpy as np
import argparse
from enum import Enum

class ProcessingType(Enum):
    RAW = 0
    TRACKER = 1
    HUE = 2
    SATURATION = 3
    VALUE = 4
    MASK = 5

class ColorTracker:
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)
        self.tracked_colors = []
        self.frame = None

    def update_frame(self):
        success, self.frame = self.video.read()
        if success:
            self.process_frame()
        return success

    def set_tracked_color_by_position(self, x, y):
        if len(self.tracked_colors) < 3:  # Limit to 3 tracked colors
            hsv_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            self.tracked_colors.append((hsv_frame[y, x, 0], hsv_frame[y, x, 1], hsv_frame[y, x, 2]))
        else:
            self.tracked_colors.clear()

    def process_frame(self):
        for idx, color in enumerate(self.tracked_colors):
            hue, sat, val = color
            lower_bound = np.array([hue - 10, sat - 40, val - 40])
            upper_bound = np.array([hue + 10, sat + 40, val + 40])
            mask = cv2.inRange(cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV), lower_bound, upper_bound)
            # Erozja i dylatacja
            mask = cv2.erode(mask, None, iterations=5)
            mask = cv2.dilate(mask, None, iterations=5)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) > 100:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(self.frame, f"Object_{idx+1}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    def get_frame(self):
        return self.frame if self.frame is not None else None

class Display:
    def __init__(self, window_name):
        cv2.namedWindow(window_name)
        self.window_name = window_name

    def update_display(self, image):
        cv2.imshow(self.window_name, image)


class EventHandler:
    def __init__(self, tracker, display, timeout):
        self.tracker = tracker
        self.display = display
        self.timeout = timeout
        cv2.setMouseCallback(self.display.window_name, self.handle_mouse)

    def handle_events(self):
        return cv2.waitKey(self.timeout) not in [ord('q'), 27]

    def handle_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.tracker.set_tracked_color_by_position(x, y)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Object Color Tracking")
    parser.add_argument('-v', '--video_path', type=str, required=True, help='Path to the video file.')
    return parser.parse_args()

def main():
    args = parse_arguments()
    tracker = ColorTracker(args.video_path)
    display = Display("Color Tracker")
    event_handler = EventHandler(tracker, display, 10)

    while True:
        if not tracker.update_frame() or not event_handler.handle_events():
            break
        display.update_display(tracker.get_frame())

if __name__ == '__main__':
    main()
