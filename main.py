"""
This an example of object tracking (we are not expecting more than
one object on the same recording).
"""


import argparse

from color_tracking.color_tracker import ColorTracker
from color_tracking.controler import EventHandler
from color_tracking.display import Display


def parse_arguments() -> argparse.Namespace:
    """
    Function parsing the arguments from the command.
    :return: argparse.Namespace - command arguments.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--video_path', type=str, required=True,
                        help='Path to video that will be processed.')
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    """
    The main function that executes the whole project.
    :param args: arguments passed within the command.
    :return: None
    """
    try:
        window_name = 'Color tracker'
        waitkey_timeout = 10
        tracker = ColorTracker(args.video_path)
        display = Display(window_name)
        event_handler = EventHandler(tracker, display, waitkey_timeout)
        while True:
            if not tracker.update_frame():
                break
            display.update_display(tracker.get_processed_frame())
            if not event_handler.handle_events():
                break

    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main(parse_arguments())
