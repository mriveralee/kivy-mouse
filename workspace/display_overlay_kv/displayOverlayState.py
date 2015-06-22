from enum import Enum

class DisplayOverlayState(Enum):
    IDLE = 0                            # Mouse Idle
    DRAGGING = 1
    POINTING = 2                        # Mouse is moving around / tracking
    ANNOTATING = 3                      # User selected annotation option
