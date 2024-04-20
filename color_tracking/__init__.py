"""
This an example of object tracking (we are not expecting more than
one object on the same recording). Whole module is responsible for
changing the video view (so you can set up if the frame should display in hue,
saturate or value from HSV color representation) or tracking the color selected by mouse.

Config key/mouse binding:
        'h' - display frame in HUE,
        's' - display frame in SATURATION,
        'v' - display frame in VALUE,
        'r' - show RAW frame,
        't' - turn on TRACKING mode

        LeftMouseClick - only available when you choose the object (color) to track.

        TO RESET TRACKING OBJECTS click till 4th object will be selected.


"""
